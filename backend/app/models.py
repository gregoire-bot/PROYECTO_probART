from sqlalchemy import String, Float, Integer
from sqlalchemy.orm import Mapped, mapped_column

from .database import Base


class BodyProfile(Base):
    __tablename__ = "body_profiles"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    height: Mapped[float] = mapped_column(
        Float,
        nullable=False
    )

    weight: Mapped[float] = mapped_column(
        Float,
        nullable=False
    )

    chest: Mapped[float] = mapped_column(
        Float,
        nullable=False
    )

    waist: Mapped[float] = mapped_column(
        Float,
        nullable=False
    )

    hip: Mapped[float] = mapped_column(
        Float,
        nullable=False
    )

    shoulders: Mapped[float] = mapped_column(
        Float,
        nullable=False
    )

    skin_tone: Mapped[str] = mapped_column(
        String(50),
        nullable=False
    )


class Clothing(Base):
    __tablename__ = "clothing"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    category: Mapped[str] = mapped_column(
        String(50),
        nullable=False
    )

    brand: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    price: Mapped[float] = mapped_column(
        Float,
        nullable=False
    )

    color: Mapped[str] = mapped_column(
        String(50),
        nullable=False
    )

    size: Mapped[str] = mapped_column(
        String(10),
        nullable=False
    )

    model_path: Mapped[str] = mapped_column(
        String(255),
        nullable=True
    )
