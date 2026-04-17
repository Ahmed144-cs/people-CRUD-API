from ninja import NinjaAPI, Query
from typing import Optional

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
    generate_people,
    get_person_by_id,
    people_data
)

from .utils import paginate

api = NinjaAPI()


# =========================
# GET (Filter + Pagination)
# =========================
@api.get("/people", response=PaginatedPeopleSchema)
def list_people(
    request,
    name: Optional[str] = None,
    min_age: Optional[int] = None,
    max_age: Optional[int] = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    is_married: Optional[bool] = None,
    page: int = Query(1)
):
    data = get_people(
        name=name,
        min_age=min_age,
        max_age=max_age,
        start_date=start_date,
        end_date=end_date,
        is_married=is_married,
    )

    paginated = paginate(data, page)

    return {
        "people": paginated["items"],
        "page": paginated["page"],
        "total_pages": paginated["total_pages"],
        "has_next": paginated["has_next"],
        "has_prev": paginated["has_prev"],
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


@api.get("/people/search/{id}", response=PersonSchema)
def get_person(request, id: int):
    person = get_person_by_id(id)

    if not person:
        return api.create_response(
            request,
            {"detail": "Person not found"},
            status=404
        )

    return person

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
def delete_person_view(request, person_id: int):
    deleted = delete_person(person_id)

    if not deleted:
        return {"success": False, "message": "Person not found"}

    return {
        "success": True,
        "message": "Person deleted successfully",
        "deleted_id": deleted.id
    }