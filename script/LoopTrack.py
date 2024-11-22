from typing import cast, Literal, Callable, Union
from _Framework.ButtonElement import ButtonElement
from datetime import datetime

from Live import Track


class LoopTrack:
    mode: Literal["record", "play", "overdub", "stop"]
    track: Track.Track
    button: ButtonElement
    long_press_duration: float
    _pressed_at: Union[float, None]

    def __init__(
        self, track: Track.Track, button: ButtonElement, long_press_duration: float
    ) -> None:
        self.mode = "stop"
        self.track = track
        self.button = button
        self.long_press_duration = long_press_duration

        self.button.add_value_listener(self.on_button_value)

    def arm(self) -> None:
        cast(Callable, self.track.arm)()

    def on_button_value(self, value: int) -> None:
        # press
        if value > 0:
            self._pressed_at = datetime.now().timestamp()
        # release
        else:
            if self._pressed_at is None:
                pass
            elif self._pressed_at > self.long_press_duration:
                self.on_button_long_press()
            else:
                self.on_button_press()

    def on_button_press(self) -> None:
        pass

    def on_button_long_press(self) -> None:
        pass
