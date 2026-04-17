from django.core.management.base import BaseCommand
from faker import Faker

from people.models import Person
from people.utils import calculate_age  # 👈 استخدام الـ utility
from datetime import date

fake = Faker()


class Command(BaseCommand):
    help = "Seed database with fake people"

    def handle(self, *args, **kwargs):
        self.stdout.write("Deleting old data...")
        Person.objects.all().delete()

        people = []

        self.stdout.write("Generating fake people...")

        for i in range(100):
            birth_date = fake.date_of_birth(minimum_age=18, maximum_age=70)

            person = Person(
                name=fake.name(),
                birth_date=birth_date,
                age=calculate_age(birth_date),  # 👈 هنا التحسين الحقيقي
                photo=f"https://i.pravatar.cc/200?img={i % 70}",
                is_married=fake.boolean(),
            )

            people.append(person)

        Person.objects.bulk_create(people)  # 🚀 أسرع من create داخل loop

        self.stdout.write(
            self.style.SUCCESS("100 people created successfully 🚀")
        )