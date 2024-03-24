from pydantic import BaseModel, ConfigDict, Field, PositiveInt
from typing import Optional
from pydantic_extra_types.country import CountryAlpha3


class AddressBase(BaseModel):
    street: str = Field(min_length=5, max_length=35)
    floor: Optional[PositiveInt] = Field(le=200)
    door: str = Field(min_length=1, max_length=6)
    adit_info: Optional[str] = Field(max_length=70)
    city: str = Field(min_length=1, max_length=28)
    postal_code: str = Field(min_length=5, max_length=8)
    country: CountryAlpha3
    default: bool


class AddressCreate(AddressBase):
    pass


class Address(AddressBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    id_buyer: int
