from ninja import Schema
from typing import List, Optional
from datetime import date


# =========================
# Person (Response)
# =========================
class PersonSchema(Schema):
    id: int
    name: str
    age: int
    photo: str
    birth_date: date   # ✅ خليته date بدل string (أفضل مع DB)
    is_married: bool

    class Config:
        from_attributes = True   # 🔥 يحول Model → Schema تلقائياً


# =========================
# Create (POST)
# =========================
class CreatePersonSchema(Schema):
    name: str
    birth_date: date   # ✅ يستقبل Date مباشرة
    is_married: bool


# =========================
# Update (PATCH)
# =========================
class UpdatePersonSchema(Schema):
    name: Optional[str] = None
    birth_date: Optional[date] = None
    is_married: Optional[bool] = None


# =========================
# Pagination Response
# =========================
class PaginatedPeopleSchema(Schema):
    people: List[PersonSchema]
    current_page: int
    page_size: int
    total_items: int
    total_pages: int
    has_next: bool
    has_prev: bool
    next_page: Optional[int]
    prev_page: Optional[int]