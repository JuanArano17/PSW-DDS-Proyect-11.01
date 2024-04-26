"""initial database schema

Revision ID: f423d6e6b40a
Revises:
Create Date: 2024-04-26 11:42:32.493767

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "f423d6e6b40a"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "Product",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("description", sa.String(length=255), nullable=True),
        sa.Column("spec_sheet", sa.String(length=255), nullable=False),
        sa.Column("stock", sa.Integer(), nullable=False),
        sa.Column("category", sa.String(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_Product_id"), "Product", ["id"], unique=False)
    op.create_table(
        "User",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("email", sa.String(length=50), nullable=False),
        sa.Column("name", sa.String(length=20), nullable=False),
        sa.Column("surname", sa.String(length=50), nullable=False),
        sa.Column("password", sa.String(length=255), nullable=False),
        sa.Column("type", sa.String(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("email"),
    )
    op.create_index(op.f("ix_User_id"), "User", ["id"], unique=False)
    op.create_table(
        "Admin",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["id"], ["User.id"], name="fk_admin_user_id", ondelete="CASCADE"
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_Admin_id"), "Admin", ["id"], unique=False)
    op.create_table(
        "Book",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("pages", sa.Integer(), nullable=False),
        sa.Column("author", sa.String(length=255), nullable=False),
        sa.ForeignKeyConstraint(
            ["id"], ["Product.id"], name="fk_product_id", ondelete="CASCADE"
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "Buyer",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("eco_points", sa.Float(), nullable=False),
        sa.Column("dni", sa.String(length=255), nullable=False),
        sa.Column("billing_address", sa.String(length=255), nullable=True),
        sa.Column("payment_method", sa.String(length=255), nullable=True),
        sa.ForeignKeyConstraint(
            ["id"], ["User.id"], name="fk_buyer_user_id", ondelete="CASCADE"
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("dni"),
    )
    op.create_index(op.f("ix_Buyer_id"), "Buyer", ["id"], unique=False)
    op.create_table(
        "Clothes",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("size", sa.String(length=255), nullable=False),
        sa.Column("materials", sa.String(length=255), nullable=False),
        sa.Column("type", sa.String(length=255), nullable=False),
        sa.ForeignKeyConstraint(
            ["id"], ["Product.id"], name="fk_product_id", ondelete="CASCADE"
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "Electrodomestics",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("brand", sa.String(length=255), nullable=False),
        sa.Column("type", sa.String(length=255), nullable=False),
        sa.Column("power_source", sa.String(length=255), nullable=False),
        sa.ForeignKeyConstraint(
            ["id"], ["Product.id"], name="fk_product_id", ondelete="CASCADE"
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "Electronics",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("brand", sa.String(length=255), nullable=False),
        sa.Column("type", sa.String(length=255), nullable=False),
        sa.Column("capacity", sa.String(length=255), nullable=False),
        sa.ForeignKeyConstraint(
            ["id"], ["Product.id"], name="fk_product_id", ondelete="CASCADE"
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "Food",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("brand", sa.String(length=255), nullable=False),
        sa.Column("type", sa.String(length=255), nullable=False),
        sa.Column("ingredients", sa.String(length=255), nullable=False),
        sa.ForeignKeyConstraint(
            ["id"], ["Product.id"], name="fk_product_id", ondelete="CASCADE"
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "Game",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("publisher", sa.String(length=255), nullable=False),
        sa.Column("platform", sa.String(length=255), nullable=False),
        sa.Column("size", sa.String(length=255), nullable=False),
        sa.ForeignKeyConstraint(
            ["id"], ["Product.id"], name="fk_product_id", ondelete="CASCADE"
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "HouseUtilities",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("brand", sa.String(length=255), nullable=False),
        sa.Column("type", sa.String(length=255), nullable=False),
        sa.ForeignKeyConstraint(
            ["id"], ["Product.id"], name="fk_product_id", ondelete="CASCADE"
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "Image",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("id_product", sa.Integer(), nullable=False),
        sa.Column("url", sa.String(), nullable=False),
        sa.ForeignKeyConstraint(
            ["id_product"],
            ["Product.id"],
            name="fk_image_product_id",
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_Image_id"), "Image", ["id"], unique=False)
    op.create_table(
        "Seller",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("cif", sa.String(length=255), nullable=False),
        sa.Column("bank_data", sa.String(length=255), nullable=False),
        sa.ForeignKeyConstraint(
            ["id"], ["User.id"], name="fk_seller_user_id", ondelete="CASCADE"
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("cif"),
    )
    op.create_index(op.f("ix_Seller_id"), "Seller", ["id"], unique=False)
    op.create_table(
        "Address",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("id_buyer", sa.Integer(), nullable=False),
        sa.Column("street", sa.String(), nullable=False),
        sa.Column("floor", sa.Integer(), nullable=True),
        sa.Column("door", sa.String(), nullable=False),
        sa.Column("adit_info", sa.String(), nullable=True),
        sa.Column("city", sa.String(), nullable=False),
        sa.Column("postal_code", sa.String(), nullable=False),
        sa.Column("country", sa.String(), nullable=False),
        sa.Column("default", sa.Boolean(), nullable=False),
        sa.ForeignKeyConstraint(
            ["id_buyer"], ["Buyer.id"], name="fk_address_buyer_id", ondelete="CASCADE"
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_Address_id"), "Address", ["id"], unique=False)
    op.create_table(
        "Card",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("id_buyer", sa.Integer(), nullable=False),
        sa.Column("card_number", sa.String(), nullable=False),
        sa.Column("card_name", sa.String(), nullable=False),
        sa.Column("card_security_num", sa.String(), nullable=False),
        sa.Column("card_exp_date", sa.Date(), nullable=False),
        sa.ForeignKeyConstraint(
            ["id_buyer"], ["Buyer.id"], name="fk_card_buyer_id", ondelete="CASCADE"
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_Card_id"), "Card", ["id"], unique=False)
    op.create_table(
        "SellerProduct",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("id_product", sa.Integer(), nullable=True),
        sa.Column("id_seller", sa.Integer(), nullable=True),
        sa.Column("quantity", sa.Integer(), nullable=False),
        sa.Column("price", sa.Float(), nullable=False),
        sa.Column("shipping_costs", sa.Float(), nullable=False),
        sa.Column("state", sa.String(), nullable=False),
        sa.Column("justification", sa.String(), nullable=True),
        sa.Column("eco_points", sa.Float(), nullable=False),
        sa.ForeignKeyConstraint(
            ["id_product"],
            ["Product.id"],
            name="fk_seller_product_product_id",
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["id_seller"],
            ["Seller.id"],
            name="fk_seller_product_seller_id",
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_SellerProduct_id"), "SellerProduct", ["id"], unique=False)
    op.create_table(
        "InShoppingCart",
        sa.Column("id_seller_product", sa.Integer(), nullable=False),
        sa.Column("id_buyer", sa.Integer(), nullable=False),
        sa.Column("quantity", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["id_buyer"], ["Buyer.id"], name="fk_cart_buyer_id", ondelete="CASCADE"
        ),
        sa.ForeignKeyConstraint(
            ["id_seller_product"],
            ["SellerProduct.id"],
            name="fk_cart_seller_product_id",
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id_seller_product", "id_buyer"),
    )
    op.create_index(
        op.f("ix_InShoppingCart_id_buyer"), "InShoppingCart", ["id_buyer"], unique=False
    )
    op.create_index(
        op.f("ix_InShoppingCart_id_seller_product"),
        "InShoppingCart",
        ["id_seller_product"],
        unique=False,
    )
    op.create_table(
        "InWishList",
        sa.Column("id_seller_product", sa.Integer(), nullable=False),
        sa.Column("id_buyer", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["id_buyer"], ["Buyer.id"], name="fk_wish_list_buyer_id", ondelete="CASCADE"
        ),
        sa.ForeignKeyConstraint(
            ["id_seller_product"],
            ["SellerProduct.id"],
            name="fk_wish_list_seller_product_id",
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id_seller_product", "id_buyer"),
    )
    op.create_index(
        op.f("ix_InWishList_id_buyer"), "InWishList", ["id_buyer"], unique=False
    )
    op.create_index(
        op.f("ix_InWishList_id_seller_product"),
        "InWishList",
        ["id_seller_product"],
        unique=False,
    )
    op.create_table(
        "Order",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("id_buyer", sa.Integer(), nullable=True),
        sa.Column("id_card", sa.Integer(), nullable=True),
        sa.Column("id_address", sa.Integer(), nullable=True),
        sa.Column("order_date", sa.Date(), nullable=False),
        sa.Column("total", sa.Float(), nullable=False),
        sa.ForeignKeyConstraint(
            ["id_address"], ["Address.id"], name="fk_order_address_id"
        ),
        sa.ForeignKeyConstraint(
            ["id_buyer"], ["Buyer.id"], name="fk_order_buyer_id", ondelete="CASCADE"
        ),
        sa.ForeignKeyConstraint(["id_card"], ["Card.id"], name="fk_order_card_id"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_Order_id"), "Order", ["id"], unique=False)
    op.create_table(
        "ProductLine",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("id_order", sa.Integer(), nullable=True),
        sa.Column("id_seller_product", sa.Integer(), nullable=True),
        sa.Column("quantity", sa.Integer(), nullable=False),
        sa.Column("subtotal", sa.Float(), nullable=False),
        sa.ForeignKeyConstraint(
            ["id_order"],
            ["Order.id"],
            name="fk_product_line_order_id",
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["id_seller_product"],
            ["SellerProduct.id"],
            name="fk_product_line_seller_product_id",
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_ProductLine_id"), "ProductLine", ["id"], unique=False)
    op.create_table(
        "RefundProduct",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("id_product_line", sa.Integer(), nullable=False),
        sa.Column("quantity", sa.Integer(), nullable=False),
        sa.Column("refund_date", sa.Date(), nullable=False),
        sa.ForeignKeyConstraint(
            ["id_product_line"],
            ["ProductLine.id"],
            name="fk_refund_product_product_line_id",
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_RefundProduct_id"), "RefundProduct", ["id"], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f("ix_RefundProduct_id"), table_name="RefundProduct")
    op.drop_table("RefundProduct")
    op.drop_index(op.f("ix_ProductLine_id"), table_name="ProductLine")
    op.drop_table("ProductLine")
    op.drop_index(op.f("ix_Order_id"), table_name="Order")
    op.drop_table("Order")
    op.drop_index(op.f("ix_InWishList_id_seller_product"), table_name="InWishList")
    op.drop_index(op.f("ix_InWishList_id_buyer"), table_name="InWishList")
    op.drop_table("InWishList")
    op.drop_index(
        op.f("ix_InShoppingCart_id_seller_product"), table_name="InShoppingCart"
    )
    op.drop_index(op.f("ix_InShoppingCart_id_buyer"), table_name="InShoppingCart")
    op.drop_table("InShoppingCart")
    op.drop_index(op.f("ix_SellerProduct_id"), table_name="SellerProduct")
    op.drop_table("SellerProduct")
    op.drop_index(op.f("ix_Card_id"), table_name="Card")
    op.drop_table("Card")
    op.drop_index(op.f("ix_Address_id"), table_name="Address")
    op.drop_table("Address")
    op.drop_index(op.f("ix_Seller_id"), table_name="Seller")
    op.drop_table("Seller")
    op.drop_index(op.f("ix_Image_id"), table_name="Image")
    op.drop_table("Image")
    op.drop_table("HouseUtilities")
    op.drop_table("Game")
    op.drop_table("Food")
    op.drop_table("Electronics")
    op.drop_table("Electrodomestics")
    op.drop_table("Clothes")
    op.drop_index(op.f("ix_Buyer_id"), table_name="Buyer")
    op.drop_table("Buyer")
    op.drop_table("Book")
    op.drop_index(op.f("ix_Admin_id"), table_name="Admin")
    op.drop_table("Admin")
    op.drop_index(op.f("ix_User_id"), table_name="User")
    op.drop_table("User")
    op.drop_index(op.f("ix_Product_id"), table_name="Product")
    op.drop_table("Product")
    # ### end Alembic commands ###
