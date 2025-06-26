from pydantic import BaseModel, Field


class ReviewCreate(BaseModel):
    rating: int
    description: str = Field(max_length=1000)
    game_id: int
    user_id: int


class ReviewRead(BaseModel):
    rating: int
    description: str
    game_id: int
    user_id: int

class ReviewUpdateFull(BaseModel):
    rating: int
    description: str

class ReviewUpdatePartial(BaseModel):
    rating: int | None
    description: str | None