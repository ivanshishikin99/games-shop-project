from datetime import date
from pydantic import BaseModel


class GameCreate(BaseModel):
    name: str
    price: int
    date_of_release: date
    age_censor: int
    developer: str
    rating: str
    genres: list[str] = []


class GameRead(BaseModel):
    name: str
    price: int
    date_of_release: date
    age_censor: int
    developer: str
    rating: str


class GameUpdatePartial(BaseModel):
    name: str | None = None
    price: int | None = None
    date_of_release: date | None = None
    age_censor: int | None = None
    developer: str | None = None
    rating: str | None = None
    genres: list[str] | None = None


class GameUpdateFull(BaseModel):
    name: str
    price: int
    date_of_release: date
    age_censor: int
    developer: str
    rating: str
    genres: list[str]
