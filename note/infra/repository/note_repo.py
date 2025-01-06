from fastapi import HTTPException
from sqlalchemy.orm import joinedload
from note.domain.note import Note as NoteV0
from note.infra.db_models.note import Note, Tag
from note.domain.repository.note_repo import INoteRepository
from database import SessionLocal

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