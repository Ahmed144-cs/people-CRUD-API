from ninja import Schema
from typing import List, Optional


# =========================
# Person (Response)
# =========================
class PersonSchema(Schema):
    id: int
    name: str
    age: int
    photo: str
    birth_date: str
    is_married: bool


# =========================
# Create (POST)
# =========================
class CreatePersonSchema(Schema):
    name: str
    birth_date: str
    is_married: bool


# =========================
# Update (PATCH)
# =========================
class UpdatePersonSchema(Schema):
    name: Optional[str] = None
    birth_date: Optional[str] = None
    is_married: Optional[bool] = None


# =========================
# Pagination Response
# =========================
class PaginatedPeopleSchema(Schema):
    people: List[PersonSchema]
    page: int
    total_pages: int
    has_next: bool
    has_prev: bool