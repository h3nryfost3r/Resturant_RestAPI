from fastapi import FastAPI
from core.database import engine
from . import models
from .routers import crud_menu, crud_submenu, crud_dish

api = FastAPI(debug=True)

# models.Base.metadata.create_all(bind=engine)

api.include_router(crud_menu.router)
api.include_router(crud_submenu.router)
api.include_router(crud_dish.router)