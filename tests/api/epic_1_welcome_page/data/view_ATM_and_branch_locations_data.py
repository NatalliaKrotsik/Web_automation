VALID_CITY = "Warsaw"
INVALID_CITY = "InvalidCity"

VALID_LOCATION_TYPES = ["ATM", "BRANCH"]
INVALID_TYPES = ["INVALID", "atm", "branch", "123", ""]

VALID_STATUSES = ["OPEN", "CLOSED"]

VALID_PAGES = [1, 2]
INVALID_PAGES = [0, -1]
INVALID_PAGE_VALUES = ["abc", "1.5", " "]

REQUIRED_RESPONSE_FIELDS = [
    "items",
    "page",
    "size",
    "totalElements",
]

REQUIRED_LOCATION_FIELDS = [
    "id",
    "type",
    "city",
    "locationNumber",
    "name",
    "address",
    "latitude",
    "longitude",
    "workingHours",
    "todayHours",
    "weekendHours",
    "holidayHours",
    "status",
    "isOpen",
]
