from abc import ABCMeta, abstractmethod
from user.domain.user import User

class IUserRepository(metaclass = ABCMeta):
    @abstractmethod
    def save(self, user : User):
        raise NotImplementedError
    
    @abstractmethod
    def find_by_email(self, email : str) -> User:
        """
        이메일로 유저 검색 없을경우 422에러
        """
        raise NotImplementedError