from enum import Enum


class Intent(Enum):
    REGISTRATION = "Registration"
    STAFF_LOOKUP = "StaffLookup"
    POLICY_FAQ = "PolicyFAQ"
    COURSE = "Course"
    UNKNOWN = "Unknown"

