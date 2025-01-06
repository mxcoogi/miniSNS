from fastapi import HTTPException
from sqlalchemy.orm import joinedload
from note.domain.note import Note as NoteV0
from note.infra.db_models.note import Note, Tag
from note.domain.repository.note_repo import INoteRepository
from database import SessionLocal
from utils.db_utils import row_to_dict

class NoteRepository(INoteRepository):
    def create_note(self, user_id : str,
        note_v0 : NoteV0) -> Note:
        with SessionLocal() as db:
            tags : list[Tag] = []
            for tag in note_v0.tags:
                existing_tag = db.query(Tag).filter(Tag.name == tag.name).first()
                if existing_tag:
                    tags.append(existing_tag)
                else:
                    tags.append(
                        Tag(
                            id=tag.id,
                            name = tag.name,
                            created_at = tag.created_at,
                            updated_at = tag.updated_at
                        )
                    )
            new_note = Note(
                id = note_v0.id,
                user_id = user_id,
                title = note_v0.title,
                content = note_v0.content,
                created_at = note_v0.created_at,
                updated_at = note_v0.updated_at,
                tags = tags
            )
            db.add(new_note)
            db.commit()

    def get_notes(self, user_id : str, page:int, item_per_page : int) -> tuple[int, list[NoteV0]]:
        with SessionLocal() as db:
            query = db.query(Note).options(joinedload(Note.tags)).filter(Note.user_id == user_id)
            total_count = query.count()
            notes = query.offset((page - 1) * item_per_page).limit(item_per_page).all()

        notes = [NoteV0(**row_to_dict(note)) for note in notes]
        return total_count, notes
            

    