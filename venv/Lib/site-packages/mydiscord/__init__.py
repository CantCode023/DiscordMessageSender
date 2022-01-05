__author__ = "mydiscord"
__copyright__ = "Copyright 2021-present CantCode"
__version__ = "1.1.0"

import logging
from typing import NamedTuple

try:
    from typing import Literal
except ImportError:
    from typing_extensions import Literal

from .mydiscord import Client

class VersionInfo(NamedTuple):
    """
    Represents the package's version info.
    """
    major: int
    minor: int
    micro: int
    releaselevel: Literal["alpha", "beta", "candidate", "final"]
    serial: int


version_info: VersionInfo = VersionInfo(
    major=2,
    minor=0,
    micro=0,
    releaselevel="release",
    serial=0
)

logging.getLogger(__name__).addHandler(logging.NullHandler())