from typing import Union
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.models.product import Product
from app.crud_repository import CRUDRepository
from app.models.book import Book
from app.models.game import Game
from app.models.electronics import Electronics
from app.models.clothes import Clothes
from app.models.food import Food
from app.models.house_utilities import HouseUtilities
from models.electrodomestics import Electrodomestics
from schemas.book import BookCreate, BookUpdate
from schemas.clothes import ClothesCreate, ClothesUpdate
from schemas.electrodomestics import ElectrodomesticsCreate, ElectrodomesticsUpdate
from schemas.electronics import ElectronicsCreate, ElectronicsUpdate
from schemas.food import FoodCreate, FoodUpdate
from schemas.game import GameCreate, GameUpdate
from schemas.house_utilities import HouseUtilitiesCreate, HouseUtilitiesUpdate
from schemas.product import ProductUpdate


class ProductService:
    def __init__(self, session: Session):
        self.session = session
        self.product_repo = CRUDRepository(session=session, model=Product)
        self.game_repo = CRUDRepository(session=session, model=Game)
        self.book_repo = CRUDRepository(session=session, model=Book)
        self.clothes_repo = CRUDRepository(session=session, model=Clothes)
        self.electronics_repo = CRUDRepository(session=session, model=Electronics)
        self.house_utilities_repo = CRUDRepository(session=session, model=HouseUtilities)
        self.food_repo = CRUDRepository(session=session, model=Food)
        self.electrodomestics_repo = CRUDRepository(session=session, model=Electrodomestics)
        self.product_factory=ProductFactory(service=self)
        

    def add(self, category:str, product_data: dict):
        return self.product_factory.create_product(category=category, product=product_data)

    def get_by_id(self, product_id):
        #if product := self.product_repo.get_by_id(product_id):
        #    return product
        if product := self.product_repo.get_by_id(product_id):
            return product

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with id {product_id} not found.",
        )

    def get_all(self) -> list[Product]:
        return self.product_factory.get_all()

    def update(self, product_id, new_data: dict):
        return self.product_factory.update_product(product_id, new_data)

    def delete_by_id(self, product_id):
        #self.product_repo.delete_by_id(product_id)
        self.product_repo.delete_by_id(id=product_id)

    def delete_all(self):
        self.product_repo.delete_all()

class ProductFactory:
    def __init__ (self, service:ProductService):
        self.service=service

    def create_product(self, category: str, product: dict):
        if category.lower() == 'book':
            book=BookCreate(**product)
            return self.service.book_repo.add(Book(**book.model_dump()))
        elif category.lower() == 'game':
            game=GameCreate(**product)
            return self.service.game_repo.add(Game(**game.model_dump()))
        elif category.lower() == 'clothes':
            clothes=ClothesCreate(**product)
            return self.service.clothes_repo.add(Clothes(**clothes.model_dump()))
        elif category.lower() == 'electronics':
            electronics=ElectronicsCreate(**product)
            return self.service.electronics_repo.add(Electronics(**electronics.model_dump()))
        elif category.lower() == 'houseutilities':
            house_utilities=HouseUtilitiesCreate(**product)
            return self.service.house_utilities_repo.add(HouseUtilities(**house_utilities.model_dump()))
        elif category.lower() == 'food':
            food=FoodCreate(**product)
            return self.service.food_repo.add(Food(**food.model_dump()))
        elif category.lower() == 'electrodomestics':
            electrodomestics=ElectrodomesticsCreate(**product)
            return self.service.electrodomestics_repo.add(Electrodomestics(**electrodomestics.model_dump()))
        else:
            raise ValueError("Invalid product category")
        
    def update_product(self, product_id:int, new_data:dict):
        product=self.service.get_by_id(product_id)
        # Extract common attributes from update_data
        # Extract common attributes from new_data
        common_attributes = {}
        for key in ["name", "description", "stock", "eco_points", "spec_sheet"]:
            if key in new_data:
                common_attributes[key] = new_data.pop(key)
        if(len(common_attributes)!=0):
            product_update=ProductUpdate(**common_attributes)
            product=self.service.product_repo.update(product,product_update)
        
        if(len(new_data)==0):
            return product
        
        if product.category.lower() == 'book':
            new_book_data=BookUpdate(**new_data)
            return self.service.book_repo.update(product, new_book_data)
        elif product.category.lower() == 'game':
            new_game_data=GameUpdate(**new_data)
            return self.service.game_repo.update(product, new_game_data)
        elif product.category.lower() == 'clothes':
            new_clothes_data=ClothesUpdate(**new_data)
            return self.service.clothes_repo.update(product, new_clothes_data)
        elif product.category.lower() == 'electronics':
            new_electronics_data=ElectronicsUpdate(**new_data)
            return self.service.electronics_repo.update(product, new_electronics_data)
        elif product.category.lower() == 'houseutilities':
            new_house_utilities_data=HouseUtilitiesUpdate(**new_data)
            return self.service.house_utilities_repo.update(product, new_house_utilities_data)
        elif product.category.lower() == 'food':
            new_food_data=FoodUpdate(**new_data)
            return self.service.food_repo.update(product, new_food_data)
        elif product.category.lower() == 'electrodomestics':
            new_electrodomestics_data=ElectrodomesticsUpdate(**new_data)
            return self.service.electrodomestics_repo.update(product, new_electrodomestics_data)

    def get_all(self):
        products=self.service.game_repo.get_all()
        products+=self.service.book_repo.get_all()
        products+=self.service.clothes_repo.get_all()
        products+=self.service.electronics_repo.get_all()
        products+=self.service.house_utilities_repo.get_all()
        products+=self.service.food_repo.get_all()
        products+=self.service.electrodomestics_repo.get_all()
        return products
    

