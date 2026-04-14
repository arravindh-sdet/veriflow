import requests

def login(base_url, endpoint, username, password):
    """
    Perform login and return access and refresh tokens
    """
    payload = {
        "userName": username,
        "password": password
    }

    response = requests.post(f"{base_url}{endpoint}", json=payload, timeout=10)
    response.raise_for_status()

    data = response.json()
    resp_obj = data.get("responseObject", {})

    return {
        "access_token": resp_obj.get("accessToken"),
        "refresh_token": resp_obj.get("refreshToken")
    }
