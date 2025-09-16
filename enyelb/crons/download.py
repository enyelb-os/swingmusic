from swingmusic.crons.cron import CronJob

from enyelb.services.download_service import DownloadService

donwload_service = DownloadService()

"""
CronJob to download tracks from downloads
"""
class DownloadTracks(CronJob):

    @property
    def is_valid(self):
        return True

    def __init__(self):
        super().__init__()

    def run(self):

        donwload_service.runDownloadTracksPendingThread()