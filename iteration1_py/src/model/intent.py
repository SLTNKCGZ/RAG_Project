from enum import Enum


class Intent(Enum):
    """
    Enumeration of user intents.
    Represents different types of user queries.
    """
    REGISTRATION = "Registration"
    STAFF_LOOKUP = "StaffLookup"
    POLICY_FAQ = "PolicyFAQ"
    COURSE = "Course"
    UNKNOWN = "Unknown"
    
    def __str__(self) -> str:
        return self.value
    
    def __repr__(self) -> str:
        return f"Intent.{self.name}"
