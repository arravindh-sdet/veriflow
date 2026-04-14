import json
import logging

import allure
import pytest

from utilities.payloads.organization.org_endpoints import Endpoints
from utilities.payloads.organization.organization_payloads import OrganizationPayload
from utilities.organization_schema import ORGANIZATION_SCHEMA
from helpers.wrappers.organization_wrapper import ResponseWrapper
from helpers.validators.schema_validator import validate_schema

logger = logging.getLogger(__name__)

@pytest.fixture(scope="module", autouse=True)
def test_create_org_valid(api_client):
    response = api_client.post(
        Endpoints.org_create(),
        json=OrganizationPayload.valid()
    )
    validate_schema(response.json(), ORGANIZATION_SCHEMA)
    actual = response.status_code
    expected = 200
    print(f"✔️ {actual} == {expected}" if actual == expected else f"❌ {actual} != {expected}")
    assert actual == expected

    print(ResponseWrapper(response.json()).responseObject.organizationId)
    return ResponseWrapper(response.json()).responseObject.organizationId


# @pytest.mark.parametrize(
#     "case_name,payload",
#     list(OrganizationPayload.empty_root_fields())
# )
# def test_org_null_root_fields(api_client, case_name, payload):
#     logger.info(f"\n{case_name}\nPayload:\n{json.dumps(payload, indent=2)}")
#     response = api_client.post(Endpoints.org_create(), json=payload)
#     actual = response.status_code
#     expected = 400
#     print(f"✔️ {actual} == {expected}" if actual == expected else f"❌ {actual} != {expected}")
#     assert actual == expected

@allure.feature("Organization")
@allure.story("Create")
@pytest.mark.parametrize(
    "case_name,payload",
    list(OrganizationPayload.missing_root_fields())
)
def test_org_missing_root_fields(api_client, case_name, payload):
    logger.info(f"\n{case_name}\nPayload:\n{json.dumps(payload, indent=2)}")
    response = api_client.post(Endpoints.org_create(), json=payload)
    # validate_schema(response.json(), ORGANIZATION_SCHEMA)
    actual = response.status_code
    expected = 400
    print(f"✔️ {actual} == {expected}" if actual == expected else f"❌ {actual} != {expected}")
    assert actual == expected


@allure.feature("Organization")
@allure.story("Create")
@pytest.mark.parametrize(
    "case_name,payload",
    list(OrganizationPayload.missing_address_fields())
)
def test_org_missing_address_fields(api_client, case_name, payload):
    logger.info(f"\n{case_name}\nPayload:\n{json.dumps(payload, indent=2)}")
    response = api_client.post(Endpoints.org_create(), json=payload)
    # validate_schema(response.json(), ORGANIZATION_SCHEMA)
    actual = response.status_code
    expected = 400
    print(f"✔️ {actual} == {expected}" if actual == expected else f"❌ {actual} != {expected}")
    assert actual == expected

@allure.feature("Organization")
@allure.story("Create")
@pytest.mark.parametrize(
    "case_name,payload",
    list(OrganizationPayload.missing_payment_fields())
)
def test_org_missing_payment_fields(api_client, case_name, payload):
    logger.info(f"\n{case_name}\nPayload:\n{json.dumps(payload, indent=2)}")
    response = api_client.post(Endpoints.org_create(), json=payload)
    # validate_schema(response.json(), ORGANIZATION_SCHEMA)
    # assert response.status_code == 400
    actual = response.status_code
    expected = 400
    print(f"✔️ {actual} == {expected}" if actual == expected else f"❌ {actual} != {expected}")
    assert actual == expected

@allure.feature("Organization")
@allure.story("Create")
@pytest.mark.parametrize(
    "case_name,payload",
    list(OrganizationPayload.null_root_fields())
)
def test_org_null_root_fields(api_client, case_name, payload):
    logger.info(f"\n{case_name}\nPayload:\n{json.dumps(payload, indent=2)}")
    response = api_client.post(Endpoints.org_create(), json=payload)
    actual = response.status_code
    expected = 400
    print(f"✔️ {actual} == {expected}" if actual == expected else f"❌ {actual} != {expected}")
    assert actual == expected

@allure.feature("Organization")
@allure.story("Create")
@pytest.mark.parametrize(
    "case_name,payload",
    list(OrganizationPayload.null_address_fields())
)
def test_org_null_address_fields(api_client, case_name, payload):
    logger.info(f"\n{case_name}\nPayload:\n{json.dumps(payload, indent=2)}")
    response = api_client.post(Endpoints.org_create(), json=payload)
    # validate_schema(response.json(), ORGANIZATION_SCHEMA)
    actual = response.status_code
    expected = 400
    print(f"✔️ {actual} == {expected}" if actual == expected else f"❌ {actual} != {expected}")
    assert actual == expected

@allure.feature("Organization")
@allure.story("Create")
@pytest.mark.parametrize(
    "case_name,payload",
    list(OrganizationPayload.null_payment_fields())
)
def test_org_null_payments_fields(api_client, case_name, payload):
    logger.info(f"\n{case_name}\nPayload:\n{json.dumps(payload, indent=2)}")
    response = api_client.post(Endpoints.org_create(), json=payload)
    # validate_schema(response.json(), ORGANIZATION_SCHEMA)
    actual = response.status_code
    expected = 400
    print(f"✔️ {actual} == {expected}" if actual == expected else f"❌ {actual} != {expected}")
    assert actual == expected


@allure.feature("Organization")
@allure.story("Create")
@pytest.mark.parametrize(
    "case_name,payload",
    list(OrganizationPayload.empty_root_fields())
)
def test_org_empty_root_fields(api_client, case_name, payload):
    logger.info(f"\n{case_name}\nPayload:\n{json.dumps(payload, indent=2)}")
    response = api_client.post(Endpoints.org_create(), json=payload)
    actual = response.status_code
    expected = 400
    print(f"✔️ {actual} == {expected}" if actual == expected else f"❌ {actual} != {expected}")
    assert actual == expected


@allure.feature("Organization")
@allure.story("Create")
@pytest.mark.parametrize(
    "case_name,payload",
    list(OrganizationPayload.empty_address_fields())
)
def test_org_empty_address_fields(api_client, case_name, payload):
    logger.info(f"\n{case_name}\nPayload:\n{json.dumps(payload, indent=2)}")
    response = api_client.post(Endpoints.org_create(), json=payload)
    # validate_schema(response.json(), ORGANIZATION_SCHEMA)
    actual = response.status_code
    expected = 400
    print(f"✔️ {actual} == {expected}" if actual == expected else f"❌ {actual} != {expected}")
    assert actual == expected

@allure.feature("Organization")
@allure.story("Create")
@pytest.mark.parametrize(
    "case_name,payload",
    list(OrganizationPayload.empty_payment_fields())
)
def test_org_empty_payments_fields(api_client, case_name, payload):
    logger.info(f"\n{case_name}\nPayload:\n{json.dumps(payload, indent=2)}")
    response = api_client.post(Endpoints.org_create(), json=payload)
    # validate_schema(response.json(), ORGANIZATION_SCHEMA)
    actual = response.status_code
    expected = 400
    print(f"✔️ {actual} == {expected}" if actual == expected else f"❌ {actual} != {expected}")
    assert actual == expected

@allure.feature("Organization")
@allure.story("Create")
@pytest.mark.parametrize(
    "case_name,payload",
    [OrganizationPayload.extra_fields()]
)
def test_org_extra_fields(api_client, case_name, payload):
    logger.info(f"\n{case_name}\nPayload:\n{json.dumps(payload, indent=2)}")
    response = api_client.post(Endpoints.org_create(), json=payload)
    # validate_schema(response.json(), ORGANIZATION_SCHEMA)
    actual = response.status_code
    expected = 200
    print(f"✔️ {actual} == {expected}" if actual == expected else f"❌ {actual} != {expected}")
    assert actual == expected
    if actual == 200:
        org_id = ResponseWrapper(response.json()).responseObject.organizationId
        response1 = api_client.patch(Endpoints.org_delete(org_id))
        assert response1.status_code == 200

@allure.feature("Organization")
@allure.story("Create")
@pytest.mark.parametrize("case_name, payload", [
    # OrganizationPayload.missing_required_field(),
    OrganizationPayload.invalid_datatype(),
    OrganizationPayload.empty_payload(),
    OrganizationPayload.update_invalid(),
    OrganizationPayload.update_partial(),
    # *list(OrganizationPayload.invalid_root_types()),
    # *list(OrganizationPayload.invalid_nested_types())
])
def test_create_org_negative(api_client, case_name, payload):
    logger.info(f"\n{case_name}\nPayload:\n{json.dumps(payload, indent=2)}")
    response = api_client.post(Endpoints.org_create(), json=payload)
    assert response.status_code == 400



@allure.feature("Organization")
@allure.story("Create")
@pytest.mark.parametrize(
    "case_name,payload,expected",
    [
        *OrganizationPayload.invalid_root_types(),
        *OrganizationPayload.invalid_nested_types(),
    ]
)
def test_org_invalid_root_types(api_client, case_name, payload, expected):
    logger.info(f"\n{case_name}\nPayload:\n{json.dumps(payload, indent=2)}")

    response = api_client.post(Endpoints.org_create(), json=payload)
    actual = response.status_code

    print(f"✔️ {actual} == {expected}" if actual == expected else f"❌ {actual} != {expected}")
    assert actual == expected

    if actual == 200:
        org_id = ResponseWrapper(response.json()).responseObject.organizationId
        response1 = api_client.patch(Endpoints.org_delete(org_id))
        assert response1.status_code == 200



# ========================Get Operations =========================
@allure.feature("Organization")
@allure.story("Get Details")
def test_get_all_organizations(api_client):
    response = api_client.get(Endpoints.org_fetch_all())
    assert response.status_code == 200

@allure.feature("Organization")
@allure.story("Get Details")
def test_get_org_valid_id(api_client, test_create_org_valid):
    response = api_client.get(Endpoints.org_view_by_id(test_create_org_valid))
    assert response.status_code == 200
    assert ResponseWrapper(response.json()).responseObject.organizationId == test_create_org_valid
    print(test_create_org_valid)

@allure.feature("Organization")
@allure.story("Get Details")
@pytest.mark.parametrize(
    "case_name,org_id",
    [
        *list(OrganizationPayload.invalid_id()),
        *list(OrganizationPayload.malformed_id()),
    ]
)
def test_get_org_invalid_id(api_client, case_name, org_id):
    response = api_client.get(Endpoints.org_view_by_id(org_id))
    assert response.status_code == 404


# ========================Update Operations =========================

@allure.feature("Organization")
@allure.story("Update")
@pytest.mark.parametrize(
    "case_name,payload",
    list(OrganizationPayload.update_valid())
)
def test_update_org_valid(api_client, case_name, payload, test_create_org_valid):
    print(test_create_org_valid)
    logger.info(f"\n{case_name}\nPayload:\n{json.dumps(payload, indent=2)}")
    response = api_client.patch(Endpoints.org_update(test_create_org_valid), json=payload)
    assert response.status_code == 200


# @pytest.mark.parametrize("case_name,payload", OrganizationPayload.invalid_id())
# def test_update_org_invalid_id(api_client, case_name, payload):
#     response = api_client.put(fEndpoints.org_create(), json=payload)
#     assert response.status_code == 404

@allure.feature("Organization")
@allure.story("Update")
@pytest.mark.parametrize(
    "case_name,payload",
    [
        OrganizationPayload.update_empty_payload(),
        OrganizationPayload.update_partial_payload(),
        OrganizationPayload.update_invalid_datatype(),
    ]
)
def test_update_org_negative(api_client, case_name, payload):
    logger.info(f"\n{case_name}\nPayload:\n{json.dumps(payload, indent=2)}")
    response = api_client.post(Endpoints.org_create(), json=payload)
    assert response.status_code == 400


# ========================Delete Operations =========================

@allure.feature("Organization")
@allure.story("Delete")
def test_delete_org_valid(api_client, test_create_org_valid):
    response = api_client.patch(Endpoints.org_delete(test_create_org_valid))
    print(str(test_get_org_valid_id))
    assert response.status_code == 200


@allure.feature("Organization")
@allure.story("Delete")
@pytest.mark.parametrize(
    "case_name,org_id",
    list(OrganizationPayload.invalid_id())
)
def test_delete_org_invalid_id(api_client, case_name, org_id):
    print(f"\nCase: {case_name}" + "\n" + f"\nOrg ID: {org_id}" )
    response = api_client.patch(Endpoints.org_delete(org_id))
    assert response.status_code == 404


# @pytest.mark.parametrize("case_name,org_id", [("linked_org", "ID_OF_LINKED_ORG")])
# def test_delete_org_linked(api_client, case_name, org_id):
#     response = api_client.delete(f"/api/v1/organizations/{org_id}")
#     assert response.status_code == 409  # conflict


@allure.feature("Organization")
@allure.story("Delete")
def test_delete_org_twice(api_client, test_create_org_valid):
    second_delete = api_client.patch(Endpoints.org_delete(test_create_org_valid))

    # assert first.status_code == 200
    assert second_delete.status_code == 400
