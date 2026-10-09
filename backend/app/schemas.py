from pydantic import BaseModel, Field


class BodyProfileCreate(BaseModel):

    name: str = Field(
        min_length=2,
        max_length=100
    )

    height: float = Field(
        gt=100,
        lt=250
    )

    weight: float = Field(
        gt=30,
        lt=300
    )

    chest: float = Field(
        gt=50,
        lt=200
    )

    waist: float = Field(
        gt=40,
        lt=200
    )

    hip: float = Field(
        gt=50,
        lt=200
    )

    shoulders: float = Field(
        gt=20,
        lt=100
    )

    skin_tone: str


class BodyProfileResponse(BaseModel):

    id: int
    name: str
    height: float
    weight: float
    chest: float
    waist: float
    hip: float
    shoulders: float
    skin_tone: str

    class Config:
        from_attributes = True
