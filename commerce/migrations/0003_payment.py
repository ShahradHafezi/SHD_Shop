import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [("commerce", "0002_order_orderline")]
    operations = [migrations.CreateModel(name="Payment", fields=[
        ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
        ("authority", models.CharField(max_length=64, unique=True)),
        ("amount_rial", models.PositiveBigIntegerField()),
        ("status", models.CharField(choices=[("requested", "Requested"), ("verified", "Verified"), ("failed", "Failed")], default="requested", max_length=12)),
        ("reference_id", models.CharField(blank=True, max_length=80)),
        ("created_at", models.DateTimeField(auto_now_add=True)),
        ("verified_at", models.DateTimeField(blank=True, null=True)),
        ("order", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name="payments", to="commerce.order")),
    ])]

