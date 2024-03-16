from sqlalchemy import Float, ForeignKey, Integer, Column
from sqlalchemy.orm import relationship
from database import Base


class ProductSeller(Base):
    __tablename__ = "ProductSeller"

    id = Column(Integer, primary_key=True)
    id_product = Column(Integer, ForeignKey("Product.id"))
    id_seller = Column(Integer, ForeignKey("Seller.id"))
    quantity = Column(Integer, nullable=False)
    price = Column(Float, nullable=False)
    shipping_costs = Column(Float, nullable=False)

    product = relationship("Product", back_populates="product_sellers")
    in_wish_list = relationship("InWishList", back_populates="product_seller")
    in_shopping_cart = relationship("InShoppingCart", back_populates="product_seller")

    product_lines = relationship("ProductLine", back_populates="product_seller")

    def __repr__(self):
        return f"ProductSeller(id={self.id}, id_product={self.id_product}, id_seller={self.id_seller}, quantity={self.quantity}, price={self.price}, shipping_costs={self.shipping_costs})"
