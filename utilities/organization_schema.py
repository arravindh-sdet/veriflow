import json

ORGANIZATION_SCHEMA = json.loads(""" 
    {
    "type": "object",
    "required": ["status", "svcName", "svcEndpoint", "infoID", "responseObject"],
    "properties": {
        "status": {"type": "string"},
        "svcName": {"type": "string"},
        "svcEndpoint": {"type": "string"},
        "infoID": {"type": "string"},
        "responseObject": {
            "type": "object",
            "required": ["organizationId", "name", "description", "address", "isActive"],
            "properties": {
                "organizationId": {"type": "string"},
                "name": {"type": "string"},
                "description": {"type": "string"},
                "isActive": {"type": "boolean"},
                "address": {
                    "type": "object",
                    "required": ["street", "city", "state", "postalCode", "country"],
                    "properties": {
                        "street": {"type": "string"},
                        "city": {"type": "string"},
                        "state": {"type": "string"},
                        "postalCode": {"type": "number"},
                        "country": {"type": "string"}
                    }
                }
            }
        }
    }
}
""")