from typing import Literal
from _Framework.ButtonElement import ButtonElement

from Live import Track


class LoopTrack:
    mode: Literal["record", "play", "overdub", "stop"]
    track: Track.Track
    button: ButtonElement

    def __init__(
        self,
        track: Track.Track,
        button: ButtonElement,
    ) -> None:
        self.mode = "stop"
        self.track = track
        self.button = button
