from enum import Enum, IntEnum, StrEnum
from sqlalchemy import text

class ApprovalQuery(StrEnum):
    pass

class RoleName(StrEnum):
    ROLE_NAME = 'energy trader'

class ApprovalLevelId(IntEnum):
    REJECTED = 1
    RETURN_TO_SUBMITTER = 2
    SENIOR_ENERGY_TRADER = 3
    TEAM_LEADER = 4
    REGULATORY_OFFICER = 5
    VP_MOS  = 6
    CLOSED = 7
    
    @property
    def next_level(self):
        transitions = {
            ApprovalLevelId.SENIOR_ENERGY_TRADER: ApprovalLevelId.TEAM_LEADER,
            ApprovalLevelId.TEAM_LEADER: ApprovalLevelId.REGULATORY_OFFICER,
            ApprovalLevelId.REGULATORY_OFFICER: ApprovalLevelId.VP_MOS,
            ApprovalLevelId.VP_MOS: ApprovalLevelId.CLOSED,
            ApprovalLevelId.CLOSED: None
        }
        return transitions.get(self)
    
class ApprovalStatusId(IntEnum):
    NEW_STATUS = 1
    COMPLETED_STATUS = 2
    UPDATED_STATUS = 3
    REJECTED_STATUS = 4
    RETURN_TO_SUBMITTER_STATUS = 5

