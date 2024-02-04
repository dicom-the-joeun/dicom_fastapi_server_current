from sqlalchemy import Column, String, Integer, Text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class StudyViewTab(Base):
    __tablename__ = 'V_STUDYTAB'
    STUDYKEY = Column(Integer, primary_key=True)
    PID = Column(String)
    PNAME = Column(String)
    MODALITY = Column(String)
    STUDYDESC = Column(String)
    STUDYDATE = Column(String)
    REPORTSTATUS = Column(String)
    SERIESCNT = Column(Integer)
    IMAGECNT = Column(Integer)
    EXAMSTATUS = Column(String)

class User(Base):
    __tablename__ = 'V_USER'

    ID = Column(Text, primary_key=True)
    PASSWORD = Column(Text)

class SeriesTab(Base):
    __tablename__ = 'V_SERIESTAB'

    STUDYKEY = Column(Integer, primary_key=True)
    SERIESKEY = Column(Integer, primary_key=True)
    SERIESDESC = Column(Text)
    IMAGECNT = Column(Integer)
    PATH = Column(Text)
    FNAME = Column(Text)


class ImageViewTab(Base):
    __tablename__ = 'V_IMAGETAB'

    STUDYKEY = Column(Integer, primary_key=True)
    SERIESKEY = Column(Integer, primary_key=True)
    IMAGEKEY = Column(Integer)
    PATH = Column(Text)
    FNAME = Column(Text)
