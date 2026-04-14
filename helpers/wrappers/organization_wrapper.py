class ResponseWrapper:
    def __init__(self, data):
        self.status = data.get("status")
        self.svcName = data.get("svcName")
        self.svcEndpoint = data.get("svcEndpoint")
        self.infoID = data.get("infoID")
        self.responseObject = ResponseObject(data.get("responseObject", {}))

class ResponseObject:
    def __init__(self, data):
        self.organizationId = data.get("organizationId")
        self.name = data.get("name")
        self.description = data.get("description")
        self.isDefault = data.get("isDefault")
        self.organizationNumber = data.get("organizationNumber")
        self.address = Address(data.get("address", {}))

class Address:
    def __init__(self, data):
        self.street = data.get("street")
        self.city = data.get("city")
        self.state = data.get("state")
        self.postalCode = data.get("postalCode")
        self.country = data.get("country")




