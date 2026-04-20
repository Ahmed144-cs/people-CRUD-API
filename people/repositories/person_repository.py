from typing import Optional
from datetime import date
from django.db import DatabaseError
from ..models import Person


class PersonRepository:

    # =========================
    # GET
    # =========================
    def get_people(
            self,
            id: Optional[int] = None,
            name: Optional[str] = None,
            min_age: Optional[int] = None,
            max_age: Optional[int] = None,
            start_date: Optional[date] = None,
            end_date: Optional[date] = None,
            is_married: Optional[bool] = None,
            order_by: Optional[str] = None,  # 👈 أضف هذا
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

        if order_by:
            queryset = queryset.order_by(order_by)

        return queryset

    # =========================
    # CREATE
    # =========================
    def create(self, **data):
        return Person.objects.create(**data)

    # =========================
    # GET BY ID
    # =========================
    def get_by_id(self, person_id: int):
        try:
            return Person.objects.get(id=person_id)
        except Person.DoesNotExist:
            return None

    # =========================
    # DELETE
    # =========================
    def delete(self, person_id: int):
        try:
            person = Person.objects.get(id=person_id)
            person.delete()
            return True
        except Person.DoesNotExist:
            return None
        except DatabaseError:
            raise