from faker import Faker
from typing import List, Optional
from datetime import date

from .utils import calculate_age, parse_date
from .schemas import PersonSchema

fake = Faker()


# =========================
# Fake Database
# =========================
people_data: List[PersonSchema] = []


# =========================
# Generate Fake Data
# =========================
def generate_people(n=100):
    global people_data

    people = []

    for i in range(n):
        birth_date = fake.date_of_birth(minimum_age=18, maximum_age=70)
        age = calculate_age(birth_date)

        person = PersonSchema(
            id=i + 1,
            name=fake.name(),
            age=age,
            photo=f"https://i.pravatar.cc/200?img={(i % 70) + 1}",
            birth_date=str(birth_date),
            is_married=fake.boolean()
        )

        people.append(person)

    people_data = people


# =========================
# GET (Filter)
# =========================
def get_people(
    name: Optional[str] = None,
    min_age: Optional[int] = None,
    max_age: Optional[int] = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    is_married: Optional[bool] = None,
):
    filtered = people_data

    if name:
        clean_name = name.strip().lower()
        filtered = [
            p for p in filtered
            if clean_name in p.name.lower()
        ]

    if min_age is not None:
        filtered = [p for p in filtered if p.age >= min_age]

    if max_age is not None:
        filtered = [p for p in filtered if p.age <= max_age]

    if start_date:
        start = parse_date(start_date)
        filtered = [
            p for p in filtered
            if parse_date(p.birth_date) >= start
        ]

    if end_date:
        end = parse_date(end_date)
        filtered = [
            p for p in filtered
            if parse_date(p.birth_date) <= end
        ]

    if is_married is not None:
        filtered = [
            p for p in filtered
            if p.is_married == is_married
        ]

    return filtered


# =========================
# CREATE
# =========================
def create_person(name: str, birth_date: str, is_married: bool):
    new_id = max([p.id for p in people_data], default=0) + 1

    birth_date_obj = parse_date(birth_date)
    age = calculate_age(birth_date_obj)

    person = PersonSchema(
        id=new_id,
        name=name,
        age=age,
        photo=f"https://i.pravatar.cc/200?img={new_id % 70 + 1}",
        birth_date=birth_date,
        is_married=is_married
    )

    people_data.append(person)
    return person


# =========================
# UPDATE
# =========================
def update_person(person_id: int, name: str, birth_date: str, is_married: bool):
    for i, p in enumerate(people_data):
        if p.id == person_id:
            birth_date_obj = parse_date(birth_date)
            age = calculate_age(birth_date_obj)

            updated = PersonSchema(
                id=person_id,
                name=name,
                age=age,
                photo=p.photo,
                birth_date=birth_date,
                is_married=is_married
            )

            people_data[i] = updated
            return updated

    return None


# =========================
# DELETE
# =========================
def delete_person(person_id: int):
    for i, p in enumerate(people_data):
        if p.id == person_id:
            return people_data.pop(i)
    return None

def get_person_by_id(person_id: int):
    for p in people_data:
        if p.id == person_id:
            return p
    return None

# =========================
# Initialize Fake Data
# =========================
people_data: List[PersonSchema] = []
generate_people()