class OrgPaginationResponseWrapper:
    def __init__(self, data):
        self.status = data.get("status")
        self.svcName = data.get("svcName")
        self.svcEndpoint = data.get("svcEndpoint")
        self.infoID = data.get("infoID")
        self.responseObject = ResponseObject(data.get("responseObject", {}))

class ResponseObject:
    def __init__(self, data):
        self.totalElements = data.get("totalElements")
        self.totalPages = data.get("totalPages")
        self.size = data.get("size")
        self.number = data.get("number")
        self.sort = data.get("sort")
        self.first = data.get("first")
        self.last = data.get("last")
        self.numberOfElements = data.get("numberOfElements")
        self.pageable = data.get("pageable")
        self.empty = data.get("empty")
        self.content = [Organization(item) for item in data.get("content", [])]

class Organization:
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









