from ulid import ULID
from note.domain.note import Note
from note.domain.repository.note_repo import INoteRepository
from datetime import datetime
from note.domain.note import Tag
class NoteService:
    def __init__(
            self,
            note_repo : INoteRepository
    ):
        self.note_repo = note_repo
        self.ulid = ULID()

    def create_note(
            self,
            user_id:str,
            title:str,
            content:str,
            tag_names:list[str] = []
    ) -> Note:
        now = datetime.now()
        tags = [
            Tag(
                id = self.ulid.generate(),
                name=title,
                created_at=now,
                updated_at=now
            )
            for title in tag_names
        ]
        note = Note(
            id = self.ulid.generate(),
            user_id = user_id,
            title= title,
            content = content,
            tags=tags,
            created_at=now,
            updated_at=now
        )
        self.note_repo.create_note(user_id, note)

        return note
    
    def get_notes(self, user_id : str, page:int, item_per_page:int) -> tuple[int, list[Note]]:
        return self.note_repo.get_notes(user_id, page, item_per_page)