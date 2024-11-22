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
        self,
        track: Track.Track,
        button: ButtonElement,
        long_press_duration: float = 1000,
    ) -> None:
        """
        Initializes a new instance of the LoopTrack class.

        Parameters:
        track (Track.Track): The track associated with this loop track instance.
        button (ButtonElement): The button element that will trigger actions on this loop track.
        long_press_duration (float): The duration (in milliseconds) to consider a button press as a long press.
                                      Defaults to 1000 milliseconds.

        This constructor sets the initial mode of the track to "stop", assigns the provided track,
        button, and long press duration. It also adds a listener to the button to handle button value changes.
        """
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
        if self.mode == "stop":
            pass
        elif self.mode == "record":
            pass
        elif self.mode == "play":
            pass
        elif self.mode == "overdub":
            pass

    def on_button_long_press(self) -> None:
        pass
