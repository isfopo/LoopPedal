from __future__ import with_statement
from typing import cast, List
import Live

from _Framework.ControlSurface import ControlSurface
from _Framework.SliderElement import SliderElement
from _Framework.ButtonElement import ButtonElement

from .mappings import types, BUTTONCHANNEL, SLIDERCHANNEL

from LoopTrack import LoopTrack


class LoopPedal(ControlSurface):
    __module__ = __name__
    __doc__ = "Simple Starter Script"

    def __init__(self, c_instance):
        ControlSurface.__init__(self, c_instance)
        with self.component_guard():
            live = cast(Live.Application, Live.Application.get_application())
            self._live_major_version = live.get_major_version()
            self._live_minor_version = live.get_minor_version()
            self._live_bugfix_version = live.get_bugfix_version()

            self.loop_tracks: List[Live.Track.Track] = []

            self._note_map = []
            self._ctrl_map = []

            self._load_mappings()

    @property
    def song(self) -> Live.Song.Song:
        return super().song()

    @property
    def tracks(self) -> List[Live.Track.Track]:
        return cast(List[Live.Track.Track], self.song.tracks)

    def _find_loop_tracks(self) -> List[Live.Track.Track]:
        return [track for track in self.tracks if str(track.name).startswith("Looper")]

    def init_loop_tracks(self) -> None:
        loop_tracks = self._find_loop_tracks()
        for i, track in enumerate(loop_tracks):
            LoopTrack(self.song, track, self._note_map[i])

    def _load_mappings(self):
        momentary = True

        for ctrl in range(128):
            control = ButtonElement(momentary, types.CC, BUTTONCHANNEL, ctrl)
            control.name = "Ctrl_" + str(control)
            self._ctrl_map.append(control)

    def disconnect(self):
        """clean up on disconnect"""
        ControlSurface.disconnect(self)
        return None
