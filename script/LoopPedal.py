from __future__ import with_statement
from typing import cast, List
import Live

from _Framework.ControlSurface import ControlSurface
from _Framework.ButtonElement import ButtonElement
from .consts import LOOPER_TRACK_IDENTIFIER

from .mappings import types, BUTTONCHANNEL

from .LoopTrack import LoopTrack


class LoopPedal(ControlSurface):
    __module__ = __name__
    __doc__ = "Looper Pedal"

    def __init__(self, c_instance):
        super().__init__(c_instance)
        with self.component_guard():
            live = cast(Live.Application, Live.Application.get_application())
            self._live_major_version = live.get_major_version()
            self._live_minor_version = live.get_minor_version()
            self._live_bugfix_version = live.get_bugfix_version()

            self.loop_tracks: List[Live.Track.Track] = []

            self._ctrl_map = []

            self._load_mappings()

    @property
    def song(self) -> Live.Song.Song:
        return super().song()

    @property
    def tracks(self) -> List[Live.Track.Track]:
        return cast(List[Live.Track.Track], self.song.tracks)

    def _find_loop_tracks(self) -> List[Live.Track.Track]:
        return [
            track
            for track in self.tracks
            if str(track.name).startswith(LOOPER_TRACK_IDENTIFIER)
        ]

    def init_loop_tracks(self) -> None:
        loop_tracks = self._find_loop_tracks()
        for track in loop_tracks:
            options = LoopTrack.parse_track_options(cast(str, track.name))
            LoopTrack(self.song, track, self._ctrl_map[int(options["note"])])
            self.loop_tracks.append(track)

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
