import django.db.models.deletion
from django.conf import settings
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [("commerce", "0001_initial")]
    operations = [
        migrations.CreateModel(name="Order", fields=[
            ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
            ("status", models.CharField(choices=[("pending", "Pending payment"), ("paid", "Paid"), ("failed", "Payment failed"), ("cancelled", "Cancelled")], default="pending", max_length=12)),
            ("total_amount", models.DecimalField(decimal_places=0, max_digits=14)),
            ("created_at", models.DateTimeField(auto_now_add=True)),
            ("updated_at", models.DateTimeField(auto_now=True)),
            ("user", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name="orders", to=settings.AUTH_USER_MODEL)),
        ], options={"ordering": ["-created_at"]}),
        migrations.CreateModel(name="OrderLine", fields=[
            ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
            ("product_name", models.CharField(max_length=180)),
            ("unit_price", models.DecimalField(decimal_places=0, max_digits=12)),
            ("quantity", models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(1)])),
            ("order", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="lines", to="commerce.order")),
            ("product", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name="order_lines", to="catalog.product")),
        ]),
    ]

