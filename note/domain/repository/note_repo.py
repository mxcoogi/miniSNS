from abc import ABCMeta, abstractmethod
from note.domain.note import Note

class INoteRepository(metaclass = ABCMeta):

    @abstractmethod
    def create_note(
        self,
        user_id : str,
        note : Note
    ) -> Note:
        raise NotImplementedError
    
    @abstractmethod
    def get_notes(
        self,
        user_id : str,
        page: int,
        item_per_page : int
    ) -> tuple[int, list[Note]]:
        raise NotImplementedError
    
