from typing import Any, List

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import (
    ForeignKey,
    Integer,
    String,
    JSON,
    delete,
    insert,
    select,
    update,   
)

from swingmusic.db import Base

from enyelb.utils.auth import get_current_userid
from enyelb.models.download import Download

"""
Table for managing user download tracks
"""
class DownloadTable(Base):
    """
    Table name in the database.
    """
    __tablename__ = "download"

    """
    Primary key ID of the download track record.
    """
    id: Mapped[int] = mapped_column(primary_key=True)
    """
    Album Artist of the download track.
    """
    #album_artist: Mapped[str] = mapped_column(String(), nullable=True)
    """
    Album ID of the download track.
    """
    #album_id: Mapped[str] = mapped_column(String(), nullable=True)
    """
    Album Name of the download track.
    """
    #album_name: Mapped[str] = mapped_column(String(), nullable=True)
    """
    Album Type of the download track.
    """
    #album_type: Mapped[str] = mapped_column(String(), index=True, nullable=True)
    """
    Artist of the download track.
    """
    #artist: Mapped[str] = mapped_column(String(), nullable=True)
    """
    Artist ID of the download track.
    """
    #artist_id: Mapped[str] = mapped_column(String(), nullable=True)
    """
    Track Number of the download track.
    """
    #track_number: Mapped[int] = mapped_column(Integer(), nullable=True)
    """
    Track ID of the download track.
    """
    track_id: Mapped[str] = mapped_column(String(), index=True, nullable=True)
    """
    Title of the download track.
    """
    #title: Mapped[str] = mapped_column(String(), nullable=True)
    """
    Date of the download track.
    """
    #date: Mapped[int] = mapped_column(Integer(), default=0)
    """
    Duration of the download track.
    """
    #duration: Mapped[int] = mapped_column(Integer(), default=0)
    """
    File path of the download track.
    """
    url: Mapped[str] = mapped_column(String(), nullable=True, default=None)
    """
    Status of the download (e.g., pending, completed).
    """
    status: Mapped[str] = mapped_column(String(), index=True, default="pending")
    """
    
    """
    song: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
    """
    User ID of the download track.
    """
    user_id: Mapped[int] = mapped_column(
        Integer(), ForeignKey("user.id", ondelete="cascade"), default=1, index=True
    )

    """
    Retrieve all download tracks for the current user.
    """
    @classmethod
    def get_all(cls, userid: bool = True) -> List[Download]:

        if userid:
            result = cls.execute(
                select(cls).where((cls.user_id == get_current_userid()))
            )
        else:
            result = cls.execute(select(cls))

        downloads: List[Download] = []
        for i in next(result).scalars():
            downloads.append(Download.toDonwload(i))

        return downloads

    """
    Retrieve all download tracks for the current user.
    """
    @classmethod
    def get_all_by_pending(cls, userid: bool = True) -> List[Download]:

        if userid:
            result = cls.execute(
                select(cls).where((cls.user_id == get_current_userid())).where(cls.status.in_(['pending', 'url'])).limit(40)
            )
        else:
            result = cls.execute(select(cls).where(cls.status.in_(['pending', 'url'])).limit(40))

        downloads: List[Download] = []
        for i in next(result).scalars():
            downloads.append(Download.toDonwload(i))
        
        return downloads
    
    """
    Retrieve a download track by its ID.
    """
    @classmethod
    def get_by_track_id(cls, id: int):
        """"""
        result = cls.execute(select(cls).where(cls.track_id == id))
        res = next(result).scalar()

        if res:
            return Download.toDonwload(res)
        
    """
    Retrieve a download track by its ID.
    """
    @classmethod
    def get_by_id(cls, id: int):
        """"""
        result = cls.execute(select(cls).where(cls.id == id))
        result = next(result).scalar()

        if result:
            return Download.toDonwload(result)
        
    """
    Insert a new download record.
    """
    @classmethod
    def insert_one(cls, values: dict[str, Any]):

        if values.get("user_id") is None:
            values["user_id"] = get_current_userid()

        result = cls.execute(insert(cls).values(values), commit=True)
        id = next(result).lastrowid

        return cls.get_by_id(id)
    
    """
    Update an existing download track record.
    """
    @classmethod
    def update_one(cls, id: int, values: dict[str, Any]):

        download = cls.get_by_id(id)
        
        if not download:
            return None
        
        if values.get("status") is None:
            values["status"] = download.status
        
        if values.get("url") is None:
            values["url"] = download.url
        
        if values.get("user_id") is None:
            values["user_id"] = download.user_id

        if values.get("track_id") is None:
            values["track_id"] = download.track_id
        
        if values.get("song") is None:
            values["song"] = download.song
        
        result = cls.execute(update(cls).where(cls.id == id).values(values), commit=True)
        result = next(result)

        return cls.get_by_id(id)
    
    """
    Delete a download track record by its ID.
    """
    @classmethod
    def delete_one(cls, id: int):
        return next(
            cls.execute(delete(cls).where(cls.id == id), commit=True)
        ).rowcount > 0