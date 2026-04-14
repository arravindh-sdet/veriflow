# utilities/payloads/auth/login_payload.py

class LoginPayload:

    @staticmethod
    def valid():
        return {
            "username": "valid_user",
            "password": "valid_password"
        }

    @staticmethod
    def invalid_username():
        return "invalid_username", {
            "username": "wrong_user",
            "password": "valid_password"
        }

    @staticmethod
    def invalid_password():
        return "invalid_password", {
            "username": "valid_user",
            "password": "wrong_password"
        }

    @staticmethod
    def empty_credentials():
        return [
            ("empty_username", {"username": "", "password": "password"}),
            ("empty_password", {"username": "user", "password": ""}),
            ("empty_both", {"username": "", "password": ""}),
        ]

    @staticmethod
    def malformed_payload():
        return [
            ("missing_username", {"password": "password"}),
            ("missing_password", {"username": "user"}),
            ("wrong_keys", {"user": "x", "pass": "y"}),
            ("empty_payload", {})
        ]

    @staticmethod
    def inactive_user():
        return "inactive_user", {
            "username": "inactive_user",
            "password": "password"
        }
