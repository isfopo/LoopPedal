from typing import cast, Literal, Union, List, Callable
from _Framework.ButtonElement import ButtonElement
from datetime import datetime

from Live import Song, Track, Clip
from .helpers.tracks import arm, duplicate_track, get_first_empty_clip_slot, unarm
from .consts import POST_RECORD_MODE


class LoopTrack:
    mode: Literal["record", "play", "overdub", "stop"]

    song: Song.Song
    original_track: Track.Track
    recording_track: Track.Track
    duplicate_tracks: List[Track.Track]
    active_clip: Union[Clip.Clip, None]

    button: ButtonElement
    long_press_duration: float
    _pressed_at: Union[float, None]

    def __init__(
        self,
        song: Song.Song,
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
        self.song = song
        self.original_track = track
        self.button = button
        self.long_press_duration = long_press_duration
        self.duplicate_tracks = []

        self.button.add_value_listener(self.on_button_value)

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
            self.mode = "record"
            # arm original track
            if arm(self.original_track):
                # fire first clip slot
                clip_slot = get_first_empty_clip_slot(self.original_track)
                if clip_slot is not None:
                    cast(Callable, clip_slot.fire)()
                    self.active_clip = clip_slot.clip

        elif self.mode == "record":
            self.mode = POST_RECORD_MODE
            # stop recording original track
            if self.active_clip is not None:
                unarm(self.original_track)
                cast(Callable, self.active_clip.fire)()
                # duplicate original track
                duplicated_track = duplicate_track(self.song, self.original_track)
                self.duplicate_tracks.append(duplicated_track)
                # arm duplicated track
                cast(Callable, duplicated_track.arm)()
                # fire clip on duplicated track
                clip_slot = get_first_empty_clip_slot(duplicated_track)
                if clip_slot is not None:
                    cast(Callable, clip_slot.fire)()
                    self.active_clip = cast(Clip.Clip, clip_slot.clip)

                    cast(Callable, self.active_clip.add_loop_end_listener)(
                        self._loop_end_listener
                    )

        elif self.mode == "play":
            self.mode = "overdub"

        elif self.mode == "overdub":
            self.mode = "play"

    def _loop_end_listener(self):
        if self.mode == "play":
            # continue looping clip
            pass

        elif self.mode == "overdub":
            # duplicate original track
            # arm duplicated track
            # call Live.Clip.Clip.remove_loop_end_listener() on previous clip
            # fire clip on duplicated track
            # add Live.Clip.Clip.add_loop_end_listener() to create a new track when loop ends
            pass

    def on_button_long_press(self) -> None:
        if self.mode != "stop":
            self.mode = "stop"
            self.reset()

    def reset(self) -> None:
        # consolidate recorded clips in scenes
        for track in self.duplicate_tracks:
            # self.song.delete_track(track)
            pass
        self.duplicate_tracks = []
