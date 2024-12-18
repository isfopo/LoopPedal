from typing import cast, List, Union, Callable
from Live import Track, ClipSlot, Song, Clip


def arm(track: Track.Track) -> bool:
    if track.can_be_armed:
        try:
            track.arm = True  # type: ignore
            return True
        except Exception:
            return False
    return False


def unarm(track: Track.Track) -> None:
    track.arm = False  # type: ignore


def get_first_empty_clip_slot(track: Track.Track) -> Union[ClipSlot.ClipSlot, None]:
    for clip_slot in cast(List[ClipSlot.ClipSlot], track.clip_slots):
        if clip_slot.clip is not None:
            return clip_slot


def duplicate_track(song: Song.Song, track: Track.Track) -> Track.Track:
    """
    Duplicates a specified track within a given song.

    This function takes a Song object and a Track object as parameters,
    identifies the index of the track in the song's track list,
    and creates a duplicate of that track.

    Parameters:
        song (Song.Song): The Song object containing the track to be duplicated.
        track (Track.Track): The Track object to be duplicated.

    Returns:
        Track.Track: The duplicated Track object.
    """
    track_index = list(cast(List[Track.Track], song.tracks)).index(track)
    song.duplicate_track(track_index, None)
    return cast(Callable, cast(Song.Song.View, song.view).selected_track)()


def get_track_of_clip(clip: Clip.Clip) -> Track.Track:
    """
    Retrieves the track associated with a given clip.

    This function takes a Clip object as a parameter and traverses its
    parent hierarchy to obtain the Track object that contains the clip.
    It assumes that the clip is part of a ClipSlot, which in turn is
    part of a Track.

    Parameters:
        clip (Clip.Clip): The Clip object whose associated Track is to be retrieved.
    Returns:
        Track.Track: The Track object that contains the specified clip.
    """
    return cast(
        Track.Track, cast(ClipSlot.ClipSlot, clip.canonical_parent).canonical_parent
    )
