import django.db.models.deletion
from django.conf import settings
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True
    dependencies = [migrations.swappable_dependency(settings.AUTH_USER_MODEL), ("catalog", "0001_initial")]
    operations = [
        migrations.CreateModel(name="Basket", fields=[
            ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
            ("updated_at", models.DateTimeField(auto_now=True)),
            ("user", models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name="basket", to=settings.AUTH_USER_MODEL)),
        ]),
        migrations.CreateModel(name="BasketItem", fields=[
            ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
            ("quantity", models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(1)])),
            ("basket", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="items", to="commerce.basket")),
            ("product", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="basket_items", to="catalog.product")),
        ]),
        migrations.AddConstraint(model_name="basketitem", constraint=models.UniqueConstraint(fields=("basket", "product"), name="unique_product_per_basket")),
    ]

