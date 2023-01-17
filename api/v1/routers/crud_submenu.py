from .. import models, schema
from core.database import get_db
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, status, HTTPException

router = APIRouter()

# CRUD Submenu
@router.get(
    '/api/v1/menus/{target_menu_id}/submenus',
    tags=["submenu"]
)
def get_submenus(
    target_menu_id, 
    db: Session = Depends(get_db)
):
    submenu_list = []
    for submenu in db.query(models.Submenu).filter(
        models.Submenu.menu_id == target_menu_id
    ).all():
        submenu_list.append(submenu.get_response_body(db))
    return submenu_list
        

@router.get(
    '/api/v1/menus/{target_menu_id}/submenus/{target_submenu_id}',
    tags=["submenu"]
)
def get_target_submenu(
    target_menu_id, 
    target_submenu_id,
    db: Session = Depends(get_db)
):
    submenu = db.query(models.Submenu).where(models.Submenu.id == target_submenu_id and models.Submenu.menu_id == target_menu_id).first()
    if submenu is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="submenu not found")
    return submenu.get_response_body(db)

@router.post(
    '/api/v1/menus/{target_menu_id}/submenus',
    status_code=status.HTTP_201_CREATED,
    tags=["submenu"]
)
def create_submenu(
    target_menu_id,
    request: schema.Group, 
    db: Session = Depends(get_db)
):
    menu = db.query(models.Menu).filter(
        models.Menu.id == target_menu_id
    ).first()
    
    if menu is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="menu not found"
        )
    
    new_submenu = models.Submenu(
        menu_id = target_menu_id,
        title = request.title,
        description = request.description
    )
    db.add(new_submenu)
    db.commit()
    db.refresh(new_submenu)
    return new_submenu.get_response_body(db)

@router.patch(
    '/api/v1/menus/{target_menu_id}/submenus/{target_submenu_id}', 
    status_code=status.HTTP_200_OK,
    tags=["submenu"]
)
def update_target_submenu(
    target_menu_id,
    target_submenu_id,
    request: schema.Group,
    db: Session = Depends(get_db)
):
    submenu = db.query(models.Submenu).filter(
        models.Submenu.id == target_submenu_id,
        models.Submenu.menu_id == target_menu_id
    ).first()
    if submenu is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="submenu not found")
    submenu.title = request.title
    submenu.description = request.description
    db.add(submenu)
    db.commit()
    db.refresh(submenu)
    return submenu.get_response_body(db)

@router.delete(
    '/api/v1/menus/{target_menu_id}/submenus/{target_submenu_id}',
    tags=["submenu"]
)
def delete_target_submenu(
    target_menu_id,
    target_submenu_id,
    db: Session = Depends(get_db)
):
    submenu = db.query(models.Submenu).filter(
        models.Submenu.id == target_submenu_id,
        models.Submenu.menu_id == target_menu_id
    )
    if submenu.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Submenu not found")
    submenu.delete()
    db.commit()
