from enum import Enum


class PhaseStatus(Enum):
    ACCEPTED = "accepted"
    PENDING = "pending"
    REJECTED = "rejected"