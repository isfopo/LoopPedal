from typing import cast, List, Union
from Live import Track, ClipSlot


def arm(track: Track.Track) -> bool:
    if track.can_be_armed:
        try:
            track.arm = True  # type: ignore
            return True
        except Exception:
            return False
    return False


def get_first_empty_clip_slot(track: Track.Track) -> Union[ClipSlot.ClipSlot, None]:
    for clip_slot in cast(List[ClipSlot.ClipSlot], track.clip_slots):
        if clip_slot.clip is not None:
            return clip_slot
