import copy
import json
import time
import uuid
from datetime import datetime


class OrganizationPayload:


    @staticmethod
    def _generate_name():
        ts = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        return f"Automation_{ts}"

    @staticmethod
    def _generate_name_for_invalid():
        return f"Automation_{time.time_ns()}"


    @staticmethod
    def valid():
        payload = json.loads("""
                {
                    "name": "",
                    "description": "Automation in Progress",
                    "isActive": true,
                    "address": {
                        "street": "14 Near Phoenix mall",
                        "city": "Velachery",
                        "country": "India",
                        "postalCode": "606701",
                        "state": "Tamil nadu"
                    },
                    "paymentInfo": {
                        "cardNumber": "4445566781234",
                        "securityCode": "123",
                        "expirationDate": "09/25"
                    }
                }
                """)

        payload["name"] = OrganizationPayload._generate_name()
        return payload

    # ---------- AUTO VARIATIONS ---------- #

    @staticmethod
    def missing_root_fields():
        payload = OrganizationPayload.valid()
        for field in payload.keys():
            # if field == "isDefault":  # skip this field only
            #     continue
            temp = copy.deepcopy(payload)
            temp.pop(field)
            yield f"missing_{field}", temp
            # yield (f"missing_{field}-{temp}", temp)

    @staticmethod
    def missing_address_fields():
        # fields = OrganizationPayload.valid()["address"].keys()
        payload = OrganizationPayload.valid()
        for field in payload["address"].keys():
            # temp = OrganizationPayload.valid()
            temp = copy.deepcopy(payload)
            temp["address"].pop(field)
            yield f"missing_address_{field}", temp

    @staticmethod
    def missing_payment_fields():
        fields = OrganizationPayload.valid()["paymentInfo"].keys()
        for field in fields:
            temp = OrganizationPayload.valid()
            temp["paymentInfo"].pop(field)
            yield f"missing_payment_{field}", temp


    @staticmethod
    def invalid_root_types():
        variations = json.loads("""{
            "name": 123,
            "isActive": "true",
            "description": false
        }""")

        for field, bad_val in variations.items():
            temp = OrganizationPayload.valid()
            temp[field] = bad_val
            temp["name"] = OrganizationPayload._generate_name_for_invalid()
            yield f"invalid_type_{field}", temp, 200

    @staticmethod
    def invalid_nested_types():
        # Address type errors
        temp1 = OrganizationPayload.valid()
        temp1["name"] = OrganizationPayload._generate_name_for_invalid()
        temp1["address"]["postalCode"] = "000000"
        yield "invalid_postalCode_type", temp1, 200

        # Payment type errors
        temp2 = OrganizationPayload.valid()
        temp2["name"] = OrganizationPayload._generate_name_for_invalid()
        temp2["paymentInfo"]["expirationDate"] = "09-2025"
        yield "invalid_expiration_format", temp2, 400

    @staticmethod
    def extra_fields():
        temp = OrganizationPayload.valid()
        temp["name"] = OrganizationPayload._generate_name_for_invalid()
        temp["unexpectedKey"] = "extraValue"
        temp["address"]["extraAddressKey"] = "extra"
        return "extra_fields", temp

    @staticmethod
    def empty_payload():
        return "empty", {}

    @staticmethod
    def update_invalid():
        return "update_invalid", {
            "isDefault": "no"
        }

    @staticmethod
    def update_partial():
        return "update_partial", {
            "description": "Partial update only"
        }

    @staticmethod
    def missing_required_field():
        payload = OrganizationPayload.valid()
        payload.pop("name")
        return "missing_required_field", payload

    @staticmethod
    def invalid_datatype():
        payload = OrganizationPayload.valid()
        payload["isActive"] = "yes"  # should be boolean
        return "invalid_datatype", payload

    @staticmethod
    def update_valid_full():
        return OrganizationPayload.valid()

    # ------------------------------------------------------------------
    # GET OPERATIONS — ID GENERATORS
    # ------------------------------------------------------------------

    @staticmethod
    def valid_id():
        """Use a correct format ID (caller must replace with real ID from DB)."""
        return [("valid_id", "668a8d6a43055a2f78401fb7")]

    @staticmethod
    def invalid_id():
        """Non-existent but valid-format ID"""
        return [("invalid_id", "fff123@321")]

    @staticmethod
    def malformed_id():
        """IDs that are not valid ObjectId format"""
        return [("malformed_id", "ABC@!@#$%123INVALIDID")]

    # ------------------------------------------------------------------
    # UPDATE PAYLOAD VARIATIONS
    # ------------------------------------------------------------------

    @staticmethod
    def update_valid():
        # temp = copy.deepcopy(OrganizationPayload.valid())
        temp = OrganizationPayload.valid()
        temp.pop("name")
        temp["description"] = "Updated Description"
        yield "update_valid", temp

    @staticmethod
    def update_invalid_datatype():
        temp = OrganizationPayload.valid()
        temp["isActive"] = "NOT_BOOLEAN"
        return "update_invalid_datatype", temp

    @staticmethod
    def update_partial_payload():
        temp = {"description": "Partial update only"}
        return "update_partial_payload", temp

    @staticmethod
    def update_empty_payload():
        return "update_empty_payload", {}

    # ------------------------------------------------------------------
    # DELETE OPERATIONS
    # ------------------------------------------------------------------

    # @staticmethod
    # def missing_required_field():
    #     payload = OrganizationPayload.valid()
    #     payload.pop("name")
    #     return payload
    #
    # @staticmethod
    # def invalid_datatype():
    #     payload = OrganizationPayload.valid()
    #     payload["isDefault"] = "yes"  # should be boolean
    #     return payload
    #
    # @staticmethod
    # def extra_fields():
    #     payload = OrganizationPayload.valid()
    #     payload["unexpectedKey"] = "extraValue"
    #     return payload
    #
    # @staticmethod
    # def empty():
    #     return {}
    #
    # @staticmethod
    # def update_valid():
    #     return {
    #         "name": "Updated Organization",
    #         "description": "Updated desc",
    #         "isDefault": True,
    #         "address": {
    #             "street": "14 Near Phoenix mall",
    #             "city": "Velachery",
    #             "country": "4567",
    #             "postalCode": "606701",
    #             "District": "Chennai",
    #             "state": "Tamil nadu"
    #         },
    #         "paymentInfo": {
    #             "cardNumber": "444556678",
    #             "securityCode": "123",
    #             "expirationDate": "2025-09"
    #         }
    #     }
    #
    # @staticmethod
    # def update_invalid():
    #     return {
    #         "isDefault": "no"
    #     }
    #
    # @staticmethod
    # def update_partial():
    #     return {
    #         "description": "Partial update only"
    #     }

    @staticmethod
    def null_root_fields():
        payload = OrganizationPayload.valid()

        # ---------- ROOT LEVEL NULLS ----------
        for field in payload.keys():
            # skip boolean or non-nullable fields
            # if field in ["isDefault"]:
            #     continue

            temp = copy.deepcopy(payload)
            temp[field] = None
            yield f"null_root_{field}", temp

    @staticmethod
    def null_address_fields():
        payload = OrganizationPayload.valid()

        for field in payload["address"].keys():
            temp = copy.deepcopy(payload)
            temp["address"][field] = None
            yield f"null_address_{field}", temp

    @staticmethod
    def null_payment_fields():
        payload = OrganizationPayload.valid()

        for field in payload["paymentInfo"].keys():
            temp = copy.deepcopy(payload)
            temp["paymentInfo"][field] = None
            yield f"null_payment_{field}", temp

    @staticmethod
    def empty_root_fields():
        payload = OrganizationPayload.valid()

        # ---------- ROOT LEVEL NULLS ----------
        for field in payload.keys():
            # optional: skip boolean or non-nullable fields
            # if field in ["isDefault"]:
            #     continue

            temp = copy.deepcopy(payload)
            temp[field] = ""
            yield f"empty_root_{field}", temp

    @staticmethod
    def empty_address_fields():
        payload = OrganizationPayload.valid()

        for field in payload["address"].keys():
            temp = copy.deepcopy(payload)
            temp["address"][field] = ""
            yield f"empty_address_{field}", temp

    @staticmethod
    def empty_payment_fields():
        payload = OrganizationPayload.valid()

        for field in payload["paymentInfo"].keys():
            temp = copy.deepcopy(payload)
            temp["paymentInfo"][field] = ""
            yield f"empty_payment_{field}", temp
