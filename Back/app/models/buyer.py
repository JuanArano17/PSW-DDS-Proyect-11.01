from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import relationship
from database import Base


class Buyer(Base):
    __tablename__ = "Buyer"

    id = Column(Integer, primary_key=True)
    email = Column(String(255), nullable=False, unique=True)
    name = Column(String(255), nullable=False)
    surname = Column(String(255), nullable=False)
    eco_points = Column(Float, nullable=False)
    password = Column(String(255), nullable=False)
    dni = Column(String(255), nullable=False, unique=True)
    billing_address = Column(String(255))
    payment_method = Column(String(255))

    addresses = relationship("Address", back_populates="buyer")
    in_shopping_cart = relationship("InShoppingCart", back_populates="buyer")
    in_wish_list = relationship("InWishList", back_populates="buyer")
    buyer_owns_cards = relationship("BuyerOwnsCard", back_populates="buyer")
    orders = relationship("Order", back_populates="buyer")

    def __repr__(self):
        return f"Buyer(id={self.id}, email='{self.email}', name='{self.name}', surname='{self.surname}', eco_points={self.eco_points}, password='{self.password}', dni='{self.dni}', billing_address='{self.billing_address}', payment_method='{self.payment_method}')"