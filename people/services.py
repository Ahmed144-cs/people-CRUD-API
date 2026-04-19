from typing import Optional
from datetime import date
from django.db import DatabaseError
from .models import Person
from .utils import calculate_age

# =========================
# GET (Filter)
# =========================
def get_people(
    id: Optional[int] = None,  # 👈 أضف هذا
    name: Optional[str] = None,
    min_age: Optional[int] = None,
    max_age: Optional[int] = None,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    is_married: Optional[bool] = None,
):
    queryset = Person.objects.all()

    if id is not None:
        queryset = queryset.filter(id=id)

    if name:
        queryset = queryset.filter(name__icontains=name)

    if min_age is not None:
        queryset = queryset.filter(age__gte=min_age)

    if max_age is not None:
        queryset = queryset.filter(age__lte=max_age)

    if start_date:
        queryset = queryset.filter(birth_date__gte=start_date)

    if end_date:
        queryset = queryset.filter(birth_date__lte=end_date)

    if is_married is not None:
        queryset = queryset.filter(is_married=is_married)

    return queryset


# =========================
# CREATE
# =========================
def create_person(name: str, birth_date: date, is_married: bool):
    age = calculate_age(birth_date)

    person = Person.objects.create(
        name=name,
        age=age,
        photo=f"https://i.pravatar.cc/200?img=1",
        birth_date=birth_date,
        is_married=is_married
    )

    return person


# =========================
# UPDATE
# =========================
def update_person(person_id: int, name: str, birth_date: date, is_married: bool):
    try:
        person = Person.objects.get(id=person_id)
    except Person.DoesNotExist:
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
    try:
        person = Person.objects.get(id=person_id)
        person.delete()
        return True

    except Person.DoesNotExist:
        return None

    except DatabaseError:
        raise