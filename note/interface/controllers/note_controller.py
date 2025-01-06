from datetime import datetime
from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field
from dependency_injector.wiring import inject, Provide
from typing import Annotated
from common.auth import get_current_user, CurrentUser
from note.application.note_service import NoteService
from containers import Container
from dataclasses import asdict
router = APIRouter(prefix="/notes")


class CreateNoteBody(BaseModel):
    title : str = Field(min_length=1, max_length=64)
    content : str = Field(min_length=1)
    tags : list[str] | None = Field(
        default=None, min_length=1, max_length=32
    )

class NoteResponse(BaseModel):
    id:str
    user_id:str
    title:str
    content:str
    tags:list[str]
    created_at : datetime
    updated_at : datetime

@router.post("/create", status_code=201, response_model=NoteResponse)
@inject
def create_note(
    current_user:Annotated[CurrentUser, Depends(get_current_user)],
    body:CreateNoteBody,
    note_service : NoteService = Depends(Provide[Container.note_service])
):
    note = note_service.create_note(
        user_id = current_user.id,
        title=body.title,
        content = body.content,
        tag_names=body.tags if body.tags else []
    )
    response = asdict(note)
    response.update({"tags" : [tag.name for tag in note.tags]})
    return response

class GetNoteResponse(BaseModel):
    total_count : int
    page:int
    notes : list[NoteResponse]

@router.get("", response_model=GetNoteResponse)
@inject
def get_notes(page : int = 2, item_per_page : int = 10, 
              current_user:CurrentUser = Depends(get_current_user), note_service : NoteService = Depends(Provide[Container.note_repo])):
    total_count, notes = note_service.get_notes(
        user_id=current_user.id,
        page=page,
        item_per_page=item_per_page
    )
    
    res = []
    for note in notes:
        note_dict = asdict(note)
        note_dict.update({"tags" : [tag.name for tag in note.tags]})
        res.append(note_dict)

    return {
        "total_count" : total_count,
        "page" : page,
        "notes" : res
    }