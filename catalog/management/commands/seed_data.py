from django.core.management.base import BaseCommand
from catalog.models import Category, Product


PRODUCTS = [
    ("Digital", "digital", "Keyboard", "keyboard", 2500000, 10),
    ("Digital", "digital", "Headphones", "headphones", 3200000, 8),
    ("Books", "books", "Django Book", "django-book", 450000, 15),
    ("Home", "home", "Desk Lamp", "desk-lamp", 900000, 6),
]


class Command(BaseCommand):
    help = "Create sample categories and products"

    def add_arguments(self, parser):
        parser.add_argument("--clear", action="store_true")

    def handle(self, *args, **options):
        if options["clear"]:
            Product.objects.all().delete()
            Category.objects.all().delete()

        for category_name, category_slug, name, slug, price, inventory in PRODUCTS:
            category, _ = Category.objects.get_or_create(
                slug=category_slug,
                defaults={"title": category_name},
            )
            Product.objects.update_or_create(
                slug=slug,
                defaults={
                    "category": category,
                    "name": name,
                    "unit_price": price,
                    "inventory": inventory,
                    "is_active": True,
                },
            )

        self.stdout.write(self.style.SUCCESS("Sample data created."))

