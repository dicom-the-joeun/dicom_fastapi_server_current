import logging
from app.models.db_model import User
from app.util.token_gen import verify_access_token

class UserService:
    @staticmethod
    def exisiting_user(ID, db):
        '''
            @params : `ID:str`
        '''
        return db.query(User).filter(User.ID == ID).first()
    
    @staticmethod
    def update_password(ID, password, new_password, db):
        user = db.query(User).filter(User.ID == ID).first()

        if user:
            if user.PASSWORD == password:
                user.PASSWORD = new_password
                db.commit()
                return True
            else:
                return False
        else:
            return False
        
    @staticmethod
    def get_id_from_token(credentials, db):
        try:
            id = verify_access_token(credentials)
            if not UserService.exisiting_user(id, db):
                raise logging.warning("침략경보")
            return id
        except Exception as e:
            print(f"{e}")
            raise