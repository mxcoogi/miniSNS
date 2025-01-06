from fastapi import FastAPI
from user.interface.controllers.user_controller import router as user_routers
from note.interface.controllers.note_controller import router as note_routers
from containers import Container
app = FastAPI()
app.container = Container()
app.include_router(user_routers)
app.include_router(note_routers)


