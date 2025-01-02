from user.domain.repository.user_repo import IUserRepository
from database import SessionLocal
from user.domain.user import User as UserV0
from user.infra.db_models.user import User
from fastapi import HTTPException
from utils.db_utils import row_to_dict

class UserRepository(IUserRepository):
    def save(self, user : UserV0):
        new_user = User(
            id = user.id,
            email = user.email,
            name = user.name,
            password = user.password,
            created_at = user.created_at,
            updated_at = user.updated_at,
            memo = user.memo
        )
        with SessionLocal() as db:
            try:
                db = SessionLocal()
                db.add(new_user)
                db.commit()
            finally:
                db.close()


    def find_by_email(self, email : str) -> User:
        with SessionLocal() as db:
            user = db.query(User).filter(User.email == email).first()

            if not user:
                raise HTTPException(status_code=422)
            
            return UserV0(**row_to_dict(user))
    
    def find_by_id(self, id: str):
        with SessionLocal() as db:
            user = db.query(User).filter(User.id == id).first()
        
        if not user:
            raise HTTPException(status_code=422)
        
        return UserV0(**row_to_dict(user))
    
    def update(self, user_v0 : UserV0):
        with SessionLocal() as db:
            user = db.query(User).filter(User.id == user_v0.id).first()
        
            if not user:
                raise HTTPException(status_code=422)
            user.name = user_v0.name
            user.password = user_v0.password
            db.add(user)
            db.commit()
        return user
        


