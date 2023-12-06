from enum import Enum


class ReqAllocAlgo(Enum):
    EARLIEST_KILLED = 1000
    LATEST_KILLED = 1001
    RANDOM = 1002


class ConPlaceAlgo(Enum):
    FIRST_FIT = 2000
    MIN_VEC_DIST = 2001


class ConConsAlgo(Enum):
    MIN_PM_NUM = 3000


class PopQueueAlgo(Enum):
    FCFS = 4000
    SJF = 4001
    HRRN = 4002


class ContainerState(Enum):
    COLD_START = 100
    RUN = 101
    SPARE = 102
    KILL = 103


class Task(Enum):
    HANDLE_REQ = 200
    CON_COLD_START = 201
    CON_RUN = 202
    CON_SPARE = 203
    CON_KILL = 204
    CONSOLIDATION = 205
    SYS_LOG = 206
