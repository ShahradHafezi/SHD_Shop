import django.db.models.deletion
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True
    dependencies = []
    operations = [
        migrations.CreateModel(name="Category", fields=[
            ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
            ("title", models.CharField(max_length=120, unique=True)),
            ("slug", models.SlugField(max_length=140, unique=True)),
            ("description", models.TextField(blank=True)),
        ], options={"ordering": ["title"], "verbose_name_plural": "categories"}),
        migrations.CreateModel(name="Product", fields=[
            ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
            ("name", models.CharField(max_length=180)),
            ("slug", models.SlugField(max_length=200, unique=True)),
            ("description", models.TextField(blank=True)),
            ("unit_price", models.DecimalField(decimal_places=0, max_digits=12, validators=[django.core.validators.MinValueValidator(0)])),
            ("inventory", models.PositiveIntegerField(default=0)),
            ("is_active", models.BooleanField(default=True)),
            ("created_at", models.DateTimeField(auto_now_add=True)),
            ("updated_at", models.DateTimeField(auto_now=True)),
            ("category", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name="products", to="catalog.category")),
        ], options={"ordering": ["-created_at"]}),
        migrations.AddIndex(model_name="product", index=models.Index(fields=["is_active", "category"], name="catalog_product_active_cat_idx")),
        migrations.AddIndex(model_name="product", index=models.Index(fields=["unit_price"], name="catalog_product_price_idx")),
    ]

