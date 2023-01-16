from sqlalchemy import Column, Float, String, ForeignKey
from sqlalchemy.orm import Session
from core.database import Base
from uuid import uuid4

TITLE_VARCHAR_LENGTH = 50
DESCRIPTION_VARCHAR_LENGTH = 300

def gen_uuid():
    return str(uuid4())

class Menu(Base):
    __tablename__ = 'menu'
    
    id = Column(String, primary_key=True, index=True, default=gen_uuid)
    title = Column(String(TITLE_VARCHAR_LENGTH), nullable=False)
    description = Column(String(DESCRIPTION_VARCHAR_LENGTH), nullable=False)
    
    # submenus = relationship('Submenu', backref="menu", passive_deletes=True)
    
    def get_response_body(self, db: Session):
        submenus_count: int
        dishes_count: int
        
        submenus_count = db.query(Submenu).filter(
            self.id == Submenu.menu_id
        ).count()
        
        submenu = db.query(Submenu).filter(
            self.id == Submenu.menu_id
        ).first()
        if submenu is None:
            dishes_count = 0
        else:
            dishes_count: int = db.query(Dish).filter(
                submenu.id == Dish.submenu_id
            ).count()

        return {
            "id": self.id,
            "title": self.title,
            "description": self.title,
            "submenus_count": submenus_count,
            "dishes_count": dishes_count
        }

class Submenu (Base):
    __tablename__ = 'submenu'
    
    id = Column(String, primary_key=True, index=True, default=gen_uuid)
    menu_id = Column(String, ForeignKey("menu.id", ondelete='CASCADE'))
    title = Column(String(TITLE_VARCHAR_LENGTH), nullable=False)
    description = Column(String(DESCRIPTION_VARCHAR_LENGTH), nullable=False)
    
    # menu = relationship('Menu', backref=backref("submenus", cascade="all, delete"))
    # dishes = relationship('Dish', backref="submenus", passive_deletes=True)
    
    def get_response_body(self, db: Session):
        dishes_count: int
        
        dishes_count: int = db.query(Dish).filter(
            self.id == Dish.submenu_id
        ).count()

        return {
            "id": self.id,
            "title": self.title,
            "description": self.title,
            "dishes_count": dishes_count
        }

class Dish (Base):
    __tablename__ = 'dish'
    
    id = Column(String, primary_key=True, index=True, default=gen_uuid)
    submenu_id = Column(String, ForeignKey("submenu.id", ondelete='CASCADE'))
    title = Column(String(TITLE_VARCHAR_LENGTH), nullable=False)
    description = Column(String(DESCRIPTION_VARCHAR_LENGTH), nullable=False)
    price = Column(Float(precision=2), nullable=False, default=.0)
    
    # submenus = relationship('Submenu', backref=backref("dishes", cascade="all, delete"))
    
    def get_response_body(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.title,
            "price": str(self.price)
        }
    



