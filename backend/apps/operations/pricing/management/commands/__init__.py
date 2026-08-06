from datetime import date

from django.core.management.base import BaseCommand

from apps.operations.booking.models import Property
from apps.operations.pricing.models import Season


class Command(BaseCommand):

    help = "Create Sukhavasam pricing seasons"


    def handle(self, *args, **kwargs):

        property = Property.objects.get(
            slug="sukhavasam-beach-resort"
        )


        seasons = [

            {
                "slug": "summer-peak-season",

                "name": "Summer Peak Season",

                "description":
                    "High demand beach holiday season.",

                "season_type":
                    Season.SeasonType.PEAK,

                "start_date":
                    date(2026, 4, 1),

                "end_date":
                    date(2026, 6, 30),

                "priority": 10,

                "recurring": True,

                "conditions": {
                    "expected_demand": "high"
                },

                "metadata": {
                    "campaign": "Summer Vacation"
                }
            },


            {
                "slug": "monsoon-season",

                "name": "Monsoon Season",

                "description":
                    "Low season period for Konkan tourism.",

                "season_type":
                    Season.SeasonType.MONSOON,

                "start_date":
                    date(2026, 7, 1),

                "end_date":
                    date(2026, 9, 30),

                "priority": 50,

                "recurring": True,

                "metadata": {
                    "note":
                        "Lower occupancy season"
                }
            },


            {
                "slug": "diwali-holiday-season",

                "name":
                    "Diwali Holiday Season",

                "season_type":
                    Season.SeasonType.FESTIVE,

                "start_date":
                    date(2026, 10, 15),

                "end_date":
                    date(2026, 11, 5),

                "priority": 5,

                "metadata": {
                    "festival":
                        "Diwali"
                }
            }

        ]


        for data in seasons:

            season, created = Season.objects.get_or_create(

                property=property,

                slug=data["slug"],

                defaults=data

            )


            if created:

                self.stdout.write(
                    self.style.SUCCESS(
                        f"Created: {season.name}"
                    )
                )

            else:

                self.stdout.write(
                    self.style.WARNING(
                        f"Exists: {season.name}"
                    )
                )