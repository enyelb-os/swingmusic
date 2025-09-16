import time
import schedule
from swingmusic.utils.threading import background

from enyelb.crons.download import DownloadTracks

@background
def start_cron_jobs():
    """
    This is the function that triggers the cron jobs.
    """
    
    # Initialize all CRON jobs here.
    DownloadTracks()

    # Run all CRON jobs on a loop.
    while True:
        schedule.run_pending()
        time.sleep(1)
