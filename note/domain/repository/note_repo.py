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