import os

from dataclasses import asdict
from typing import List

from spotdl import Spotdl
from spotdl.types.song import Song
from spotdl.types.options import DownloaderOptions

path = os.getenv('OUTPUT_PATH', default='/home/enyelb/Música/downloads')

if not os.path.exists(path):
    os.makedirs(path)

DOWNLOADER_OPTIONS: DownloaderOptions = {
    'output': os.getenv(
        'OUTPUT_PATH', default=path + '/{artist}/{album}/{track-number} - {title}.{output-ext}'
    ),
    'ffmpeg': 'ffmpeg',
    'bitrate': '320k',
    'lyrics_providers': ['musixmatch', 'genius'],  # Excluir azlyrics
    'user_agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36',
    'simple_tui': True,
}

"""
Downloader service to manage spotdl instance
"""
class DownloaderService:

    """
    Singleton instance of DownloaderService
    """
    _instance = None

    """
    Instance of Spotdl
    """
    _spotdl = None

    """
    Flag to indicate if a download is in progress
    """
    _isDownloading = None

    """
    Create a new instance of DownloaderService if one does not exist.
    """
    def __new__(cls):
        if not cls._instance:
            cls._instance = super(DownloaderService, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    """
     Initialize the DownloaderService with a Spotdl instance.
    """
    def __init__(self, loop = None):
        if not self._spotdl:
            self._spotdl = Spotdl(
                client_id=os.getenv('CLIENT_ID', default='5f573c9620494bae87890c0f08a60293'),
                client_secret=os.getenv('CLIENT_SECRET', default='212476d9b0f3472eaa762d90b19b0ba8'),
                downloader_settings=DOWNLOADER_OPTIONS,
                loop=loop,
            )

    """
    Create a new directory if it does not exist.
    """
    def makedirs(self, song: any):
        if not os.path.exists(path):
            os.makedirs(path)
        
        if not os.path.exists(path + '/' + song.album_artist):
            os.makedirs(path + '/' + song.album_artist)
        
        if not os.path.exists(path + '/' + song.album_artist + '/' + song.album_name):
            os.makedirs(path + '/' + song.album_artist + '/' + song.album_name)

    
    """
    search for a track on spotify
    """
    def search(self, url: str):
        try:
            return self._spotdl.search([url])
        except Exception:
            return None
    
    """
    transform a track into a download track
    """
    def toDownloadTrack(self, track):
        return {
            "track_id": track.song_id,
            "url": None,
            "status": "pending",
            "song": asdict(track),
            "user_id": None
        }
    
    """
    download tracks
    """
    def downloadTracks(self, songs: List[Song]):
        self._isDownloading = True

        if len(songs) > 0:
            for song in songs:
                self.makedirs(song)
            result = self._spotdl.download_songs(songs)
            self._isDownloading = False
            return result
    
        self._isDownloading = False
        return []

    """
    is downloading
    """
    def isDownloading(self):
        return self._isDownloading
            
        

        
