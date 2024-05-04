from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.schemas.products.seller_product import ProductState
from app.schemas.products.seller_product import (
    SellerProductCreate,
    SellerProductRead,
    SellerProductUpdate,
)
from app.service.users.types.seller import SellerService
from app.models.products.seller_product import SellerProduct
from app.crud_repository import CRUDRepository
from app.service.products.product import ProductService
from abc import ABC, abstractmethod

from app.models.products.categories.variations.size import Size
from app.schemas.products.categories.variations.size import SizeCreate

class SellerProductState(ABC):
    @abstractmethod
    def handle(self, new_data):
        pass

class PendingState(SellerProductState):
    def handle(self, new_data):
        if new_data.state == ProductState.Rejected:
            if not new_data.justification or len(new_data.justification) < 1:
                raise HTTPException(
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    detail="Rejected products require a justification",
                )
        elif new_data.state == ProductState.Approved:
            new_data.justification = ""
            if new_data.eco_points is None:
                raise HTTPException(
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    detail="Eco-points must be assigned to approved products",
                )
            if new_data.age_restricted is None:
                raise HTTPException(
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    detail="Age restriction must be specified for approved products",
                )
            
class ApprovedState(SellerProductState):
    def handle(self, new_data):
        if new_data.state == ProductState.Rejected:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Approved products cannot be rejected",
            )

class RejectedState(SellerProductState):
    def handle(self, new_data):
        if new_data.state == ProductState.Approved:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Rejected products cannot be approved",
            )

class SellerProductRepository(CRUDRepository):
    def _init_(self, session: Session):
        super()._init_(session=session, model=SellerProduct)
        self._model = SellerProduct

    def get_by_id_product(self, id_product) -> list[SellerProduct]:
        return (
            self._db.query(self._model)
            .filter(self._model.id_product == id_product)
            .all()
        )
    
    def get_by_id_seller(self, id_seller) -> list[SellerProduct]:
        return (
            self._db.query(self._model)
            .filter(self._model.id_seller == id_seller)
            .all()
        )

    def delete_by_id_product(self, id_product):
        self._db.query(self._model).filter(
            self._model.id_product == id_product
        ).delete()  # type: ignore
        self._db.commit()


class SellerProductService:
    def _init_(
        self,
        session: Session,
        seller_service: SellerService,
        product_service: ProductService,
    ):
        self.session = session
        self.seller_product_repo = SellerProductRepository(session=session)
        self.size_repo = CRUDRepository(session=session,model=Size)
        self.seller_service = seller_service
        self.product_service = product_service

    def add(self, id_seller, seller_product: SellerProductCreate) -> SellerProduct:
        self.seller_service.get_by_id(id_seller)
        product = self.product_service.get_by_id(seller_product.id_product)

        if self.seller_product_repo.get_where(
            SellerProduct.id_seller == id_seller,
            SellerProduct.id_product == seller_product.id_product,
        ):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Seller already has a product with id {seller_product.id_product}",
            )

        if (product._class.name_=="Clothes"):
            if seller_product.sizes == []:
                raise HTTPException(
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    detail="Clothing products must have at least one size specified.",
                )
            seller_product.quantity=0
            for size in seller_product.sizes:
                seller_product.quantity+=size.quantity
            
            total_size=0
            used_sizes=[]
            for size_data in seller_product.sizes:
                total_size+=size_data.quantity
                if size_data.size in used_sizes:
                    raise HTTPException(
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    detail="There can't be repeat sizes for the same clothing item"
                ) 
                used_sizes.append(size_data.size)
            
            product.stock += seller_product.quantity  # type: ignore

            seller_product_obj = SellerProduct(
                **seller_product.model_dump(exclude="sizes"), id_seller=id_seller, state=ProductState.Pending, eco_points=0, age_restricted=False
            )
            seller_product_obj = self.seller_product_repo.add(seller_product_obj)

            for size_data in seller_product.sizes:
                self.size_repo.add(Size(**size_data.model_dump(), seller_product_id=seller_product_obj.id))
            return seller_product_obj
        else:
            if seller_product.sizes!=[]:
                raise HTTPException(
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    detail="This category of product cannot have sizes",
                )
            
            if not seller_product.quantity:
                raise HTTPException(
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    detail="This category of product must have a quantity",
                )

            product.stock += seller_product.quantity  # type: ignore

            seller_product_obj = SellerProduct(
                **seller_product.model_dump(exclude="sizes"), id_seller=id_seller, state=ProductState.Pending, eco_points=0, age_restricted=False
            )
            seller_product_obj = self.seller_product_repo.add(seller_product_obj)
            return seller_product_obj
        
    
    def get_current_state(self, state: str) -> SellerProductState:
        if state == ProductState.Pending:
            return PendingState()
        elif state == ProductState.Approved:
            return ApprovedState()
        elif state == ProductState.Rejected:
            return RejectedState()
        else:
            raise ValueError("Invalid state value")

    def map_seller_product_to_read_schema(
        self, seller_product: SellerProduct
    ) -> SellerProductRead:
        product = self.product_service.get_by_id(seller_product.id_product)
        sizes=seller_product.sizes
        if(product.category!="Clothes"):
            sizes=None
        return SellerProductRead(
            quantity=seller_product.quantity,
            price=seller_product.price,
            shipping_costs=seller_product.shipping_costs,
            id=seller_product.id,
            id_product=product.id,
            id_seller=seller_product.id_seller,
            category=product.category,
            state=seller_product.state,
            name=product.name,
            description=product.description,
            age_restricted=seller_product.age_restricted,
            eco_points=seller_product.eco_points,
            spec_sheet=product.spec_sheet,
            justification=seller_product.justification,
            stock=product.stock,
            images=[image.url for image in product.images],
            author=product.author if hasattr(product, "author") else None,
            pages=product.pages if hasattr(product, "pages") else None,
            materials=product.materials if hasattr(product, "materials") else None,
            type=product.type if hasattr(product, "type") else None,
            brand=product.brand if hasattr(product, "brand") else None,
            size=product.size if hasattr(product, "size") else None,
            capacity=product.capacity if hasattr(product, "capacity") else None,
            power_source=product.power_source
            if hasattr(product, "power_source")
            else None,
            ingredients=product.ingredients
            if hasattr(product, "ingredients")
            else None,
            publisher=product.publisher if hasattr(product, "publisher") else None,
            platform=product.platform if hasattr(product, "platform") else None,
            sizes=sizes
        )
    
    def map_seller_products(self, seller_products):
        complete_seller_products = []
        for seller_product in seller_products:
            seller_product_info = self.map_seller_product_to_read_schema(seller_product)
            complete_seller_products.append(seller_product_info)
        return complete_seller_products

    def get_by_id(self, seller_product_id) -> SellerProduct:
        if seller_product := self.seller_product_repo.get_by_id(seller_product_id):
            return seller_product

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Seller product with id {seller_product_id} not found.",
        )

    def get_by_id_full(self, seller_product_id) -> SellerProductRead:
        seller_product = self.get_by_id(seller_product_id)
        return self.map_seller_product_to_read_schema(seller_product)

    def get_all(self) -> list[SellerProductRead]:
        seller_products = self.seller_product_repo.get_all()
        return self.map_seller_products
    
    def get_all_by_state(self,state) -> list[SellerProductRead]:
        seller_products = self.seller_product_repo.get_all()
        complete_seller_products = []
        for seller_product in seller_products:
            if(seller_product.state==state):
                seller_product_info = self.map_seller_product_to_read_schema(seller_product)
                complete_seller_products.append(seller_product_info)
        return complete_seller_products

    def update(self, seller_product_id, new_data: SellerProductUpdate) -> SellerProduct:
        seller_product = self.get_by_id(seller_product_id)
        current_state = self.get_current_state(seller_product.state) 
        product=self.product_service.get_by_id(seller_product.id_product)
        current_state.handle(new_data)
        if(new_data.sizes and product._class.name_!="Clothes"):
            raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Seller products of this category cannot have sizes",
                )
        
        if(new_data.quantity and product._class.name_=="Clothes"):
            raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Only update size quantities for clothing objects",
                )
        


        if(product._class.name_=="Clothes"):
            used_sizes=[]
            for size_data in new_data.sizes:
                if size_data.size in used_sizes:
                    raise HTTPException(
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    detail="There can't be repeat sizes for the same clothing item"
                ) 
                used_sizes.append(size_data.size)

            new_data.quantity=seller_product.quantity
            if new_data.sizes:
                for size_data in new_data.sizes:
                    size = self.size_repo.get_where(Size.size==size_data.size,Size.seller_product_id==seller_product_id)
                    if size:
                        new_data.quantity=new_data.quantity-size[0].quantity+size_data.quantity
                        self.size_repo.update(size[0], size_data)
                    else:
                        new_data.quantity=new_data.quantity+size_data.quantity
                        size_data=SizeCreate(**size_data.model_dump())
                        self.size_repo.add(Size(**size_data.model_dump(), seller_product_id=seller_product_id))

        if(new_data.quantity):
            product.stock = product.stock + new_data.quantity - seller_product.quantity
            seller_product.notify_observers(new_data.quantity)

        #new_data.sizes=[]
        modified_data=SellerProductUpdate(**new_data.model_dump(exclude="sizes"))
        if(self.are_all_fields_none_except_sizes(modified_data)):
            return seller_product
        return self.seller_product_repo.update(seller_product, modified_data)
        


    def are_all_fields_none_except_sizes(self, new_data):
        for field_name, field_value in new_data:
            if field_name != 'sizes' and field_value is not None:
                return False
        return True

    def delete_by_id(self, seller_product_id):
        seller_product = self.get_by_id(seller_product_id)
        product = self.product_service.get_by_id(seller_product.id_product)
        product.stock -= seller_product.quantity  # type: ignore
        self.seller_product_repo.delete_by_id(seller_product_id)

    def delete_all(self):
        seller_products = self.get_all()
        for seller_product in seller_products:
            product = self.product_service.get_by_id(seller_product.id_product)
            product.stock -= seller_product.quantity  # type: ignore
        self.seller_product_repo.delete_all()

    def get_by_id_product(self, id_product) -> list[SellerProductRead]:
        seller_products = self.seller_product_repo.get_by_id_product(
            id_product=id_product
        )
        return self.map_seller_products(seller_products)
    
    def get_by_id_seller(self, id_seller) -> list[SellerProductRead]:
        seller_products = self.seller_product_repo.get_by_id_seller(
            id_seller=id_seller
        )
        return self.map_seller_products(seller_products)

    def delete_by_id_product(self, id_product):
        return self.seller_product_repo.delete_by_id_product(id_product=id_product)