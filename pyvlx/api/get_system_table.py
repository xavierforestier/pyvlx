"""Module for retrieving system table from API."""
from typing import TYPE_CHECKING, List

from pyvlx.actuator import Actuator
from pyvlx.log import PYVLXLOG

from .api_event import ApiEvent
from .frames import (
    FrameBase, FrameGetSystemTableConfirmation,
    FrameGetSystemTableNotification, FrameGetSystemTableRequest)

if TYPE_CHECKING:
    from pyvlx import PyVLX


class GetSystemTable(ApiEvent):
    """Class for retrieving scene list from API."""

    def __init__(self, pyvlx: "PyVLX"):
        """Initialize system table class."""
        super().__init__(pyvlx=pyvlx)
        self.success = False
        self.count: int = 0
        self.actuators: List[Actuator] = []

    async def handle_frame(self, frame: FrameBase) -> bool:
        """Handle incoming API frame, return True if this was the expected frame."""
        if isinstance(frame, FrameGetSystemTableConfirmation):
            return False
        if isinstance(frame, FrameGetSystemTableNotification):
            self.count += len(frame.actuators)
            self.actuators.extend(frame.actuators)
            return frame.remaining_objects == 0
        if self.count != len(self.actuators):
            PYVLXLOG.warning("Warning: number of received system objects does not match expected number")
        self.success = True
        return True

    def request_frame(self) -> FrameGetSystemTableRequest:
        """Construct initiating frame."""
        return FrameGetSystemTableRequest()
