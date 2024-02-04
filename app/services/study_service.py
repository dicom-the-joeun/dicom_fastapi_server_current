from app.models.api_model import SelectStudyViewTab
from app.models.db_model import StudyViewTab

from typing import List

class StudyService:
    @staticmethod
    def select_study_all(db) -> List[SelectStudyViewTab]:
        studies = db.query(StudyViewTab).all()
        return studies  
