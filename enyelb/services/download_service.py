import threading
import time

from typing import List

from spotdl.types.song import Song

from swingmusic.db.libdata import TrackTable
from swingmusic.lib.index import index_everything

from enyelb.db.download_table import DownloadTable

from enyelb.models.download import Download

from enyelb.spotdl import DownloaderService


""" 
Service layer for download-related operations. 
"""
class DownloadService:
    """
    Thread for downloading tracks
    """
    _thread = None
    """
    Singleton instance of DownloadService
    """
    _instance = None
    """
    Downloader service instance
    """
    _downloader = None
    """
    time sleep downloads in secund
    """
    _delay = 60
    """
    Create a new instance of DownloadService if one does not exist.
    """
    def __new__(cls):
        if not cls._instance:
            cls._instance = super(DownloadService, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    """
    Initialize the DownloadService with a DownloaderService instance.
    """
    def downloader(self):
        if not self._downloader:
            self._downloader = DownloaderService()
        return self._downloader

    """
    Find all downloads for the current user.
    """
    def findAll(self, userid: bool = True):
        return DownloadTable.get_all(userid=userid)
    
    """
    Find all tracks for the current user.
    """
    def findAllSwingTrack(self):
        return list(TrackTable.get_all())
    
    """
    Find a download by its ID.
    """
    def findById(self, download_id):
        return DownloadTable.get_by_id(download_id)
    
    """
    Find all downloads with 'pending' status.
    """
    def findByPending(self):
        return DownloadTable.get_by_pending()
    
    """
    Find all downloads tracks for the current user.
    """
    def findAllDownloadTracks(self, userid: bool = True):
        return DownloadTable.get_all(userid=userid)

    """
    Find all downloads tracks for the current user.
    """
    def findAllDownloadTracksByPending(self, userid: bool = True) -> List[Song]:
        downloads = DownloadTable.get_all_by_pending(userid=userid)
        result: List[Song] = [download.toSong() for download in downloads]
        return result
    
    """
    Find all downloads tracks for the current user.
    """
    def existsDownloadTrackById(self, id: str) -> List[Song]:
        return DownloadTable.get_by_track_id(id)
    
    """
    Create a new download.
    """
    def create(self, url: str):
        downloader = self.downloader()
        # search tracks
        tracks = downloader.search(url)
        #validate if tracks found
        if not tracks:
            return None

        downloads = []
        for track in tracks:
            if not self.existsDownloadTrackById(track.song_id):
                download = DownloadTable.insert_one(downloader.toDownloadTrack(track))
                downloads.append(download)

        return downloads
    
    """
    Update an existing download track.
    """
    def update(self, id: int, values: dict):
        if values.get("status") == "completed":
            return DownloadTable.delete_one(id)
        else:
            return DownloadTable.update_one(id, values)
    
    """
    Delete a download by its ID.
    """
    def delete(self, download_id: int):
        download = DownloadTable.get_by_id(download_id)
        if not download:
            return None
        
        DownloadTable.delete_one(download_id)
        
        return download
    
    """
    Check if a download exists by its ID.
    """
    def runDownloadTracksPendingThread(self):
        """
        
        """
        if self._thread and self._thread.is_alive():
            return {"message": "Download already in progress"}
        
        self._thread = threading.Thread(
            target=self.runDownloadTracksPendingInBackground,
            name="DownloadBackgroundThread",
            daemon=True
        )
        self._thread.start()

    """
    update exists track in downloads
    """
    def completedExistsTracks(self):

        tracks = self.findAllSwingTrack()

        tracks_ids = {f"{track.album}|{track.albumartists[0]['name']}|{track.title}" for track in tracks}

        download_tracks = self.findAllDownloadTracks(userid=False)
        completed_tracks = [dt for dt in download_tracks if f"{dt.album_name}|{dt.album_artist}|{dt.title}" in tracks_ids]

        for track in completed_tracks:
            self.update(track.id, {"status": "completed"})
    
    """
    Get pending downloads
    """
    def completedDownloadSongs(self, songs: list[Song]):

        songs_ids = [f"{song.album_name}|{song.album_artist}|{song.name}" for song in songs]
        download_tracks = self.findAllDownloadTracks(userid=False)
                
        completed_tracks = [dt for dt in download_tracks if f"{dt.album_name}|{dt.album_artist}|{dt.title}" in songs_ids]

        for track in completed_tracks:
            self.update(track.id, {"status": "completed"})

    """
    Get pending downloads
    """
    def errorsDownloadSongs(self, songs: list[Song]):

        songs_ids = [f"{song.album_name}|{song.album_artist}|{song.name}" for song in songs]
        download_tracks = self.findAllDownloadTracks(userid=False)
                
        errors_tracks = [dt for dt in download_tracks if f"{dt.album_name}|{dt.album_artist}|{dt.title}" in songs_ids]

        for track in errors_tracks:
            self.update(track.id, {"status": "error"})
    
    """
    Run download tracks in background
    """
    def runDownloadTracksPendingInBackground(self):
        while True:
            
            downloader = self.downloader()
            """
            Método que se ejecuta en el hilo background
            Maneja todo el proceso de descarga
            """
            try:

                """
                
                """
                if downloader.isDownloading():
                    print("Ya hay una descarga en progreso")
                    self.sleep()
                    continue

                """
                
                """
                self.completedExistsTracks()
                """
                
                """
                pendings = self.findAllDownloadTracksByPending()
                """

                """
                if len(pendings) == 0:
                    print("No hay canciones pendientes para descargar")
                    self.sleep()
                    continue
                """
                
                """
                print(f"Descargando {len(pendings)} canciones...")
                """

                """
                results = downloader.downloadTracks(pendings)
                """
                
                """
                downloads = [result[0] for result in results if result[1] is not None]
                """

                """
                if len(downloads) > 0:
                    print(f"Descarga completada. {len(downloads)} canciones descargadas")
                    self.completedDownloadSongs(downloads)
                    index_everything()
                """
                
                """
                errors = [result[0] for result in results if result[1] is None]
                """
                
                """
                if len(errors) > 0:
                    print(f"Errores: {len(errors)} canciones con errores")
                    self.errorsDownloadSongs(errors)

                self.sleep()
            except Exception as e:
                print(f"Error en la descarga: {e}")
                self.sleep()

    """
    sleep
    """
    def sleep(self):
        time.sleep(self._delay)
