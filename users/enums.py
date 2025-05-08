from enum import Enum


class Role(Enum):
    """
    Enum for user roles.
    """
    ADMIN = "admin"
    SUPPORT_AGENT = "support-agent"