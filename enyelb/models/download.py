
from typing import Optional, Dict, Any
from dataclasses import dataclass

from spotdl.types.song import Song

from swingmusic.utils.auth import get_current_userid

@dataclass(slots=True)
class Download:
    """Creates download objects"""

    song: Optional[Dict]

    id: int | str
    track_id: int | None
    url: str | None
    status: str = "pending"
    user_id: int | None = None

    album_artist: Optional[str] = None
    album_id: Optional[str] = None
    album_name: Optional[str] = None
    album_type: Optional[str] = None
    artist: Optional[str] = None
    artist_id: Optional[str] = None
    track_number: Optional[str] = None
    title: Optional[str] = None
    date: Optional[int] = None
    duration: Optional[int] = None
    
    def __post_init__(self):

        track = self.toSong()

        if self.album_name is None:
            self.album_name = track.album_name

        if self.album_id is None:
            self.album_id = track.album_id
            
        if self.album_type is None:
            self.album_type = track.album_type

        if self.album_artist is None:
            self.album_artist = track.album_artist

        if self.artist is None:
            self.artist = track.artist

        if self.artist_id is None:
            self.artist_id = track.artist_id

        if self.track_number is None:
            self.track_number = track.track_number

        if self.track_id is None:
            self.track_id = track.song_id

        if self.title is None:
            self.title = track.name

        if self.date is None:
            self.date = track.date

        if self.duration is None:
            self.duration = track.duration
        
        if self.user_id is None:
            self.user_id = get_current_userid()


    def toSong(self) -> Song:
        song: Song = Song.from_dict(self.song)
        
        if song.download_url is None:
            song.download_url = self.url
        
        return song

    @staticmethod
    def row_to_dict(row: Any):
        d = row.__dict__
        del d["_sa_instance_state"]
        return d

    @staticmethod
    def toDonwload(entry: Any):
        entry_dict = Download.row_to_dict(entry)
        return Download(**entry_dict)
