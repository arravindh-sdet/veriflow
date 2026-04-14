# core/api_client.py
import requests
import json
from typing import Optional, Callable, Dict
import allure

class APIClient:
    def __init__(
        self,
        base_url: str,
        access_token: Optional[str] = None,
        refresh_token: Optional[str] = None,
        refresh_endpoint: str = "/api/v1/user/create/refreshToken",
        login_func: Optional[Callable[[], Dict[str, str]]] = None,
    ):
        self.base_url = base_url
        self.token_store = {
            "access_token": access_token,
            "refresh_token": refresh_token,
        }
        self.refresh_endpoint = refresh_endpoint
        self.login_func = login_func

    # -----------------------------
    # Headers & Logging
    # -----------------------------
    def _prepare_headers(self, headers: Optional[dict] = None) -> dict:
        headers = headers.copy() if headers else {}
        token = self.token_store.get("access_token")
        if token:
            headers["Authorization"] = f"Bearer {token}"
        headers.setdefault("Content-Type", "application/json")
        return headers

    def _pretty_json(self, data):
        try:
            return json.dumps(data, indent=2)
        except Exception:
            return str(data)

    def _log_request_response(self, method, url, headers, payload, response):
        request_info = {"method": method, "url": url, "headers": headers}
        if payload not in (None, {}, []):
            request_info["payload"] = payload

        allure.attach(
            self._pretty_json(request_info),
            name="Request",
            attachment_type=allure.attachment_type.JSON
        )

        content_type = response.headers.get("Content-Type", "")
        try:
            if "application/json" in content_type:
                resp_json = response.json()
                allure.attach(
                    self._pretty_json(resp_json),
                    name=f"Response ({response.status_code})",
                    attachment_type=allure.attachment_type.JSON
                )
            else:
                if response.text.strip():
                    allure.attach(
                        response.text,
                        name=f"Response ({response.status_code})",
                        attachment_type=allure.attachment_type.TEXT
                    )
        except Exception:
            if response.text.strip():
                allure.attach(
                    response.text,
                    name=f"Response ({response.status_code})",
                    attachment_type=allure.attachment_type.TEXT
                )

    # -----------------------------
    # Login & Refresh
    # -----------------------------
    def _login(self) -> bool:
        if not self.login_func:
            return False
        try:
            tokens = self.login_func()
            access = tokens.get("access_token")
            refresh = tokens.get("refresh_token")
            if not access:
                return False
            self.token_store["access_token"] = access
            self.token_store["refresh_token"] = refresh
            return True
        except Exception:
            return False

    def _refresh_access_token(self) -> bool:
        refresh_token = self.token_store.get("refresh_token")
        if not refresh_token:
            return False
        url = f"{self.base_url}{self.refresh_endpoint}"
        try:
            resp = requests.post(url, json={"refreshToken": refresh_token}, timeout=10)
            if resp.status_code != 200:
                return False
            data = resp.json()
            resp_obj = data.get("responseObject", {})
            new_access = resp_obj.get("accessToken")
            new_refresh = resp_obj.get("refreshToken", refresh_token)
            if not new_access:
                return False
            self.token_store["access_token"] = new_access
            self.token_store["refresh_token"] = new_refresh
            return True
        except Exception as e:
            print("Refresh failed:", e)
            return False

    # -----------------------------
    # Core Request Handler
    # -----------------------------
    def _send_request(self, method, endpoint, auth_required=True, retry=True, **kwargs):
        url = f"{self.base_url}{endpoint}"
        headers = self._prepare_headers(kwargs.pop("headers", None))
        payload = kwargs.get("json") or kwargs.get("data")

        response = requests.request(method, url, headers=headers, **kwargs)

        # Retry on 401 with refresh token
        if auth_required and response.status_code == 401 and retry:
            if self._refresh_access_token() or self._login():
                headers = self._prepare_headers(kwargs.get("headers"))
                response = requests.request(method, url, headers=headers, **kwargs)

        self._log_request_response(method, url, headers, payload, response)
        return response

    # -----------------------------
    # Public HTTP Methods
    # -----------------------------
    def get(self, endpoint, params=None, headers=None):
        return self._send_request("GET", endpoint, headers=headers, params=params)

    def post(self, endpoint, json=None, headers=None, auth_required=True):
        return self._send_request("POST", endpoint, json=json, headers=headers, auth_required=auth_required)

    def put(self, endpoint, json=None, headers=None):
        return self._send_request("PUT", endpoint, json=json, headers=headers)

    def patch(self, endpoint, json=None, headers=None):
        return self._send_request("PATCH", endpoint, json=json, headers=headers)

    def delete(self, endpoint, headers=None):
        return self._send_request("DELETE", endpoint, headers=headers)
