"""
All download-related routes.
"""

from pydantic import BaseModel, Field

from flask_openapi3 import APIBlueprint, Tag

from enyelb.services.download_service import DownloadService

tag = Tag(name="Downloads", description="Get and manage downloads")
api = APIBlueprint("downloads", __name__, url_prefix="/downloads", abp_tags=[tag])

"""
"""
download_service = DownloadService()

""" 
Helper functions for custom downloads 
"""
@api.get("")
def send_all_downloads():
    """
    Gets all the downloads.
    """
    downloads = download_service.findAll()
    """
    Format last_updated to time passed
    """
    return {"data": downloads}

"""
Custom downloads
"""
class CreateDownloadBody(BaseModel):
    url: str = Field(..., description="The name of the download")

"""
Create a new download
"""
@api.post("/new")
def create_download(body: CreateDownloadBody):
    """
    New download

    Creates a new download. Accepts POST method with a JSON body.
    """
    downloads = download_service.create(body.url)
    
    if downloads is None:
        return {"error": "Download could not be created"}, 500

    return {"downloads": downloads}, 201

"""
Custom downloads
"""
class UpdateDownloadBody(BaseModel):
    id: str | int = Field(..., description="The ID of the download")
    url: str = Field(..., description="The name of the download")
                     
"""
Create a new download
"""
@api.post("/update")
def update_download(body: UpdateDownloadBody):
    """
    New download

    Creates a new download. Accepts POST method with a JSON body.
    """
    download = download_service.update(body.id, { 
        "url": body.url,
        "status": "url"
    })
    
    if download is None:
        return {"error": "Download could not be update"}, 500

    return {"download": download}, 200

"""
Helper functions to get trackhashes from different item types"""
class DownloadIDPath(BaseModel):
    id: str | int = Field(..., description="The ID of the download")

"""
Delete by id download
"""
@api.post("/delete")
def delete_download(body: DownloadIDPath):
    """
    New download

    Creates a new download. Accepts POST method with a JSON body.
    """
    download = download_service.delete(body.id)
    
    if download is None:
        return {"error": "Download could not be created"}, 500

    return {"download": download }, 200

"""
Get download by id
"""
@api.get("/<downloadid>")
def get_download(path: DownloadIDPath):
    """
    Get download by id
    """
    download = download_service.findById(int(path.downloadid))

    if download is None:
        return {"msg": "Download not found"}, 404
    
    tracks = download_service.findAllTracksByDownloadId(int(path.downloadid))

    download_service.runDownloadTracksPendingThread()
    return {
        "download": download,
        "tracks": list(tracks),
    }