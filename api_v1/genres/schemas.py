from pydantic import BaseModel


class GenreCreate(BaseModel):
    genre_name: str

class GenreRead(GenreCreate):
    pass

class GenreUpdate(GenreCreate):
    pass