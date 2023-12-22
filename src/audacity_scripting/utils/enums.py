# enums.py
from enum import Enum


class AudacityCommandStatus(Enum):
    SUCCESS = 'BatchCommand finished: OK'
    FAIL = 'BatchCommand finished: Failed!'


class AudacityClipCommands(Enum):
    GETINFO = 'GetInfo: Type=Clips'
