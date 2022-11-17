from enum import Enum


class Status(Enum):
    FAILED = "failed"
    FINISHED = "finished"
    IN_PROGRESS = "in-progress"
    QUEUED = "queued"
