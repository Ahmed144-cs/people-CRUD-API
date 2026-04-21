from django.http import HttpResponse
from ninja import NinjaAPI, Query
from typing import Optional
from datetime import date
from ninja.errors import HttpError

from .schemas import (
    PersonSchema,
    PaginatedPeopleSchema,
    CreatePersonSchema
)

from .services import (
    get_people,
    create_person,
    update_person,
    delete_person,
    get_people_paginated,
)

api = NinjaAPI()


# =========================
# GET (Filter + Pagination)
# =========================
@api.get("/people", response=PaginatedPeopleSchema)
def list_people(
    request,
    id: Optional[int] = None,
    name: Optional[str] = None,
    min_age: Optional[int] = None,
    max_age: Optional[int] = None,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    is_married: Optional[bool] = None,
    page: int = Query(1, ge=1),
    page_size: int = Query(10, le=100),
    order_by: Optional[str] = None,
):
    result = get_people_paginated(
        id=id,
        name=name,
        min_age=min_age,
        max_age=max_age,
        start_date=start_date,
        end_date=end_date,
        is_married=is_married,
        order_by=order_by,
        page=page,
        page_size=page_size,
    )

    return {
        "people": result["items"],
        "current_page": result["page"],
        "page_size": result["page_size"],
        "total_items": result["total_items"],
        "total_pages": result["total_pages"],
        "has_next": result["has_next"],
        "has_prev": result["has_prev"],
        "next_page": result["next_page"],
        "prev_page": result["prev_page"],
    }


# =========================
# CREATE
# =========================
@api.post("/people", response=PersonSchema)
def create_person_view(request, payload: CreatePersonSchema):
    return create_person(
        name=payload.name,
        birth_date=payload.birth_date,
        is_married=payload.is_married
    )


# =========================
# UPDATE
# =========================
@api.put("/people/{person_id}", response=PersonSchema)
def update_person_view(request, person_id: int, payload: CreatePersonSchema):
    updated = update_person(
        person_id=person_id,
        name=payload.name,
        birth_date=payload.birth_date,
        is_married=payload.is_married
    )

    if not updated:
        raise HttpError(404, "Person not found")

    return updated


# =========================
# DELETE
# =========================
@api.delete("/people/{person_id}")
def delete_person_api(request, person_id: int):
    result = delete_person(person_id)

    if result is None:
        raise HttpError(404, "Person not found")

    # 👇 REST Best Practice
    return HttpResponse(status=204)