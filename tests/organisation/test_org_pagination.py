import allure

from helpers.validators.pagination_validator import validate_pagination
from helpers.wrappers.organization_pagination_wrapper import OrgPaginationResponseWrapper

@allure.feature("Organization")
@allure.story("Pagination")
def test_org_pagination(api_client):
    response = api_client.get("/api/v1/organizations/view/fetchAll")
    assert response.status_code == 200

@allure.feature("Organization")
@allure.story("Pagination")
# @pytest.mark.parametrize("page", list(range(0, 9)))  # pages 0..8
def test_organizations_pagination_all_pages(api_client):
    size = 5

    resp = api_client.get(f"/api/v1/organizations/view/fetchAll?page=0&size={size}").json()
    total_pages = OrgPaginationResponseWrapper(resp).responseObject.totalPages

    for page in range(total_pages):
        response = api_client.get(
            f"/api/v1/organizations/view/fetchAll?page={page}&size={size}"
        )
        assert response.status_code == 200
        validate_pagination(response.json(), page, size)




@allure.feature("Organization")
@allure.story("Pagination")
def test_pagination_invalid_page_number(api_client):
    response = api_client.get("/api/v1/organizations/view/fetchAll?page=-1&size=5")

    assert response.status_code in [400, 422, 404]  # depends on API behavior

@allure.feature("Organization")
@allure.story("Pagination")
def test_pagination_page_number_too_large(api_client):
    response = api_client.get("/api/v1/organizations/view/fetchAll?page=9999&size=5")
    assert response.status_code == 200


@allure.feature("Organization")
@allure.story("Pagination")
def test_pagination_invalid_size(api_client):
    response = api_client.get("/api/v1/organizations/view/fetchAll?page=0&size=0")
    assert response.status_code in [400, 422, 404]

@allure.feature("Organization")
@allure.story("Pagination")
def test_pagination_non_integer_values(api_client):
    response = api_client.get("/api/v1/organizations/view/fetchAll?page=abc&size=xyz")
    assert response.status_code in [400, 422, 500]

@allure.feature("Organization")
@allure.story("Pagination")
def test_pagination_total_elements_consistency(api_client):
    size = 5
    collected_ids = set()

    # Get total pages
    resp = api_client.get(f"/api/v1/organizations/view/fetchAll?page=0&size={size}").json()
    total_pages = OrgPaginationResponseWrapper(resp).responseObject.totalPages

    for page in range(total_pages):
        data = api_client.get(f"/api/v1/organizations/view/fetchAll?page={page}&size={size}").json()
        content = OrgPaginationResponseWrapper(data).responseObject.content

        for item in content:
            collected_ids.add(item.organizationId)

    assert len(collected_ids) == resp["responseObject"]["totalElements"]
