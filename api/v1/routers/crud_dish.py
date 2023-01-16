
from .. import models, schema
from core.database import get_db
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, status, HTTPException

from typing import List

router = APIRouter()

# CRUD Dish
@router.get(
    '/api/v1/menus/{target_menu_id}/submenus/{target_submenu_id}/dishes',
    response_model=List[schema.Item]
    )
def get_dishes(
    target_menu_id, 
    target_submenu_id, 
    db: Session = Depends(get_db)
):
    dishes_list: list = []
    submenu = db.query(models.Submenu).filter(
        models.Submenu.id == target_submenu_id,
        models.Submenu.menu_id == target_menu_id
    ).first()
    if submenu is not None:
        for dish in db.query(models.Dish).filter(
            submenu.id == models.Dish.submenu_id
        ).all():
            dishes_list.append(dish.get_response_body())
    return dishes_list

@router.get(
    '/api/v1/menus/{target_menu_id}/submenus/{target_submenu_id}/dishes/{target_dish_id}'
)
def get_target_dish(
    target_menu_id, 
    target_submenu_id,
    target_dish_id,
    db: Session = Depends(get_db)
):
    submenu = db.query(models.Submenu).filter(
        models.Submenu.id == target_submenu_id,
        models.Submenu.menu_id == target_menu_id
    ).first()
    dish = db.query(models.Dish).filter(
        submenu.id == models.Dish.submenu_id,
        models.Dish.id == target_dish_id
    ).first()
    if dish is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="dish not found")
    return dish.get_response_body()

@router.post(
    '/api/v1/menus/{target_menu_id}/submenus/{target_submenu_id}/dishes', 
    status_code=status.HTTP_201_CREATED
)
def create_dish(
    target_menu_id, 
    target_submenu_id,
    request: schema.Item,
    db: Session = Depends(get_db)
):
    submenu = db.query(models.Submenu).filter(
        models.Submenu.id == target_submenu_id,
        models.Submenu.menu_id == target_menu_id
    ).first()
    
    if submenu is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="submenu not found"
        )
    
    new_dish = models.Dish(
        submenu_id = target_submenu_id,
        title = request.title,
        description = request.description,
        price = request.price
    )
    
    db.add(new_dish)
    db.commit()
    db.refresh(new_dish)
    return new_dish.get_response_body()

@router.patch(
    '/api/v1/menus/{target_menu_id}/submenus/{target_submenu_id}/dishes/{target_dish_id}'
)
def update_target_dish(
    target_menu_id, 
    target_submenu_id,
    target_dish_id,
    request: schema.Item,
    db: Session = Depends(get_db)):
    submenu = db.query(models.Submenu).filter(
        models.Submenu.id == target_submenu_id,
        models.Submenu.menu_id == target_menu_id
    ).first()
    dish = db.query(models.Dish).filter(
        submenu.id == models.Dish.submenu_id,
        models.Dish.id == target_dish_id
    ).first()
    if dish is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="dish not found")
    dish.title = request.title
    dish.description = request.description
    dish.price = request.price
    db.add(dish)
    db.commit()
    db.refresh(dish)
    return dish.get_response_body()

@router.delete(
    '/api/v1/menus/{target_menu_id}/submenus/{target_submenu_id}/dishes/{target_dish_id}'
)
def delete_target_dish(
    target_menu_id, 
    target_submenu_id,
    target_dish_id,
    db: Session = Depends(get_db)):
    submenu = db.query(models.Submenu).filter(
        models.Submenu.id == target_submenu_id,
        models.Submenu.menu_id == target_menu_id
    ).first()
    dishes = db.query(models.Dish).filter(
        submenu.id == models.Dish.submenu_id,
        models.Dish.id == target_dish_id
    )
    if dishes.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="dish not found")
    dishes.delete()
    db.commit()
