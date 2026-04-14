class Endpoints:
    ORGANIZATIONS_BASE = "/api/v1/organizations"

    @staticmethod
    def org_create() -> str:
        return f"{Endpoints.ORGANIZATIONS_BASE}/create"

    @staticmethod
    def org_update(org_id: str) -> str:
        return f"{Endpoints.ORGANIZATIONS_BASE}/update/{org_id}"

    @staticmethod
    def org_process() -> str:
        return f"{Endpoints.ORGANIZATIONS_BASE}/process"

    @staticmethod
    def org_fetch_all() -> str:
        return f"{Endpoints.ORGANIZATIONS_BASE}/view/fetchAll"

    @staticmethod
    def org_view_by_id(org_id: str) -> str:
        return f"{Endpoints.ORGANIZATIONS_BASE}/view/id/{org_id}"

    @staticmethod
    def org_delete(org_id: str) -> str:
        return f"{Endpoints.ORGANIZATIONS_BASE}/deactivate/{org_id}"
