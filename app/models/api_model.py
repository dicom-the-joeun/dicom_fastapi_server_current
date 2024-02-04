

from typing import Optional
from pydantic import BaseModel

class SelectStudyViewTab(BaseModel):
    STUDYKEY : int
    PID : str
    PNAME : str
    MODALITY : str
    STUDYDESC : Optional[str] = ""
    STUDYDATE : int
    REPORTSTATUS : int
    SERIESCNT : int
    IMAGECNT : int
    EXAMSTATUS : int

class SelectThumbnail(BaseModel):
    SERIESKEY : int
    SERIESDESC : Optional[str] = "N\A"
    BASE64IMAGE : str

class SelectThumbnail(BaseModel):
    SERIESKEY : int
    SERIESDESC : Optional[str] = None
    SCORE : Optional[str] = None
    IMAGECNT : int
    PATH : str
    FNAME : str
    HEADERS : str

class SelectSereies(BaseModel):
    IMAGEKEY : int
    PATH : str
    FNAME : str