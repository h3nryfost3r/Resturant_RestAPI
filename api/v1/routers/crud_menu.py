from .. import models, schema
from core.database import get_db
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, status, HTTPException

router = APIRouter()

# CRUD Menu
@router.get(
    '/api/v1/menus'
)
def get_menus(
    db: Session = Depends(get_db)
):
    menus = []
    for menu in db.query(models.Menu).all():
        menus.append(menu.get_response_body(db))
    return menus

@router.get(
    '/api/v1/menus/{target_menu_id}'
)
def get_target_menu(
    target_menu_id, 
    db: Session = Depends(get_db)
):
    menu = db.query(models.Menu).where(
        models.Menu.id == target_menu_id
    ).first()
     
    if menu is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"menu not found")
    
    return menu.get_response_body(db)

@router.post(
    '/api/v1/menus', 
    status_code=status.HTTP_201_CREATED
)
def create_menu(
    request: schema.Group, 
    db: Session = Depends(get_db)
):
    new_menu = models.Menu(
        title = request.title,
        description = request.description
    )
    db.add(new_menu)
    db.commit()
    db.refresh(new_menu)
    return new_menu.get_response_body(db)

@router.patch(
    '/api/v1/menus/{target_menu_id}'
)
def update_target_menu(
    target_menu_id, 
    request: schema.Group, 
    db: Session = Depends(get_db)
):
    menu = db.query(models.Menu).filter(models.Menu.id == target_menu_id).first()
    if menu is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Menu with {target_menu_id} not found")
    menu.title = request.title
    menu.description = request.description
    db.add(menu)
    db.commit()
    db.refresh(menu)
    return menu.get_response_body(db)

@router.delete(
    '/api/v1/menus/{target_menu_id}'
)
def delete_target_menu(
    target_menu_id,
    db: Session = Depends(get_db)
):
    db.query(models.Menu).filter(
        models.Menu.id == target_menu_id
    ).delete()
    db.commit()
