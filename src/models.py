from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, ForeignKey, Integer, BigInteger, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
import enum

db = SQLAlchemy()


class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(
        String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False)

    favorite_planet_id: Mapped[int] = mapped_column(
        ForeignKey("planets.id"), nullable=True)
    favorite_character_id: Mapped[int] = mapped_column(
        ForeignKey("characters.id"), nullable=True)

    favorite_planet: Mapped["Planet"] = relationship(
        "Planet", foreign_keys=[favorite_planet_id])
    favorite_character: Mapped["Character"] = relationship(
        "Character", foreign_keys=[favorite_character_id])

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "favorite_planet": self.favorite_planet.nombre if self.favorite_planet else None,
            "favorite_character": self.favorite_character.nombre if self.favorite_character else None
        }


class Planet(db.Model):
    __tablename__ = "planets"

    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(String(120), nullable=False)
    clima: Mapped[str] = mapped_column(String(120))
    terreno: Mapped[str] = mapped_column(String(120))
    poblacion: Mapped[int] = mapped_column(BigInteger)

    characters: Mapped[list["Character"]] = relationship(
        "Character", back_populates="planeta_origen")

    def __str__(self):
        return self.nombre

    def serialize(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "clima": self.clima,
            "terreno": self.terreno,
            "poblacion": self.poblacion,
        }


class Character(db.Model):
    __tablename__ = "characters"

    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(String(120), nullable=False)
    genero: Mapped[str] = mapped_column(
        Enum("male", "female", "n/a", "unknown", name="genero_enum"), nullable=False)
    raza: Mapped[str] = mapped_column(String(80))

    planeta_origen_id: Mapped[int] = mapped_column(
        ForeignKey("planets.id"), nullable=True)
    planeta_origen: Mapped["Planet"] = relationship(
        "Planet", back_populates="characters")

    def __str__(self):
        return self.nombre

    def serialize(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "genero": self.genero,
            "raza": self.raza,
            "planeta_origen_nombre": self.planeta_origen.nombre if self.planeta_origen else None
        }
