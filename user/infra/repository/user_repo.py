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
            updated_at = user.updated_at
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