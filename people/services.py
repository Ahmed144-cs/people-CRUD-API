from typing import Optional
from datetime import date
from django.db import DatabaseError
from .models import Person
from .utils import calculate_age
from .repositories.person_repository import PersonRepository
from .utils import paginate_queryset

repo = PersonRepository()

# =========================
# GET (Filter)
# =========================
def get_people(
    id: Optional[int] = None,
    name: Optional[str] = None,
    min_age: Optional[int] = None,
    max_age: Optional[int] = None,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    is_married: Optional[bool] = None,
    order_by: Optional[str] = None,
):
    return repo.get_people(
        id=id,
        name=name,
        min_age=min_age,
        max_age=max_age,
        start_date=start_date,
        end_date=end_date,
        is_married=is_married,
        order_by=order_by,
    )


def get_people_paginated(
    id=None,
    name=None,
    min_age=None,
    max_age=None,
    start_date=None,
    end_date=None,
    is_married=None,
    order_by=None,
    page=1,
    page_size=10,
):
    queryset = get_people(
        id=id,
        name=name,
        min_age=min_age,
        max_age=max_age,
        start_date=start_date,
        end_date=end_date,
        is_married=is_married,
        order_by=order_by,
    )

    # 1️⃣ حالة id أولاً (مهم جداً)
    if id is not None:
        person = queryset.first()
        if not person:
            return empty_response(1)

        return {
            "items": [person],
            "current_page": 1,
            "page_size": 1,
            "total_items": 1,
            "total_pages": 1,
            "has_next": False,
            "has_prev": False,
            "next_page": None,
            "prev_page": None,
        }

    # 2️⃣ حالة no results بعد الفلترة
    if not queryset.exists():
        return empty_response(page_size)
    # 3️⃣ pagination الطبيعي
    return paginate_queryset(queryset, page, page_size)

def empty_response(page_size):
    return {
        "items": [],
        "current_page": 0,
        "page_size": page_size,
        "total_items": 0,
        "total_pages": 0,
        "has_next": False,
        "has_prev": False,
        "next_page": None,
        "prev_page": None,
    }

# =========================
# CREATE
# =========================
def create_person(name: str, birth_date: date, is_married: bool):
    age = calculate_age(birth_date)

    return repo.create(
        name=name,
        age=age,
        photo="https://i.pravatar.cc/200?img=1",
        birth_date=birth_date,
        is_married=is_married
    )


# =========================
# UPDATE
# =========================
def update_person(person_id: int, name: str, birth_date: date, is_married: bool):
    person = repo.get_by_id(person_id)

    if not person:
        return None

    person.name = name
    person.birth_date = birth_date
    person.age = calculate_age(birth_date)
    person.is_married = is_married

    person.save()
    return person


# =========================
# DELETE
# =========================
def delete_person(person_id: int):
    return repo.delete(person_id)