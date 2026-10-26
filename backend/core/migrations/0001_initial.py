import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models

class Migration(migrations.Migration):
    initial = True
    dependencies = [migrations.swappable_dependency(settings.AUTH_USER_MODEL)]
    operations = [
        migrations.CreateModel(name="Profile", fields=[
            ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
            ("role", models.CharField(choices=[("buyer","Buyer"),("seller","Seller"),("technician","Technician")], default="buyer", max_length=20)),
            ("phone", models.CharField(blank=True, max_length=30)),
            ("location", models.CharField(blank=True, max_length=120)),
            ("bio", models.TextField(blank=True)),
            ("is_verified", models.BooleanField(default=False)),
            ("user", models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name="profile", to=settings.AUTH_USER_MODEL)),
        ]),
        migrations.CreateModel(name="Product", fields=[
            ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
            ("title", models.CharField(max_length=180)), ("description", models.TextField()),
            ("category", models.CharField(choices=[("routers","Routers & Wi-Fi"),("switches","Switches & Hubs"),("cctv","CCTV & Security"),("fiber","Fiber & Accessories"),("servers","Servers & Storage"),("other","Other")], default="other", max_length=30)),
            ("condition", models.CharField(choices=[("new","New"),("refurbished","Refurbished"),("used","Used")], default="new", max_length=20)),
            ("price_kes", models.DecimalField(decimal_places=2, max_digits=12)),
            ("location", models.CharField(default="Nairobi", max_length=120)), ("image_url", models.URLField(blank=True)),
            ("stock", models.PositiveIntegerField(default=1)), ("is_active", models.BooleanField(default=True)),
            ("created_at", models.DateTimeField(auto_now_add=True)), ("updated_at", models.DateTimeField(auto_now=True)),
            ("owner", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="products", to=settings.AUTH_USER_MODEL)),
        ], options={"ordering":["-created_at"]}),
        migrations.CreateModel(name="Service", fields=[
            ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
            ("title", models.CharField(max_length=180)), ("description", models.TextField()),
            ("category", models.CharField(default="Network installation", max_length=100)), ("location", models.CharField(default="Nairobi", max_length=120)),
            ("price_from_kes", models.DecimalField(decimal_places=2, default=0, max_digits=12)), ("experience_years", models.PositiveIntegerField(default=0)),
            ("is_active", models.BooleanField(default=True)), ("created_at", models.DateTimeField(auto_now_add=True)),
            ("owner", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="services", to=settings.AUTH_USER_MODEL)),
        ], options={"ordering":["-created_at"]}),
        migrations.CreateModel(name="AnalyticsEvent", fields=[
            ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
            ("event_type", models.CharField(max_length=60)), ("path", models.CharField(blank=True, max_length=300)),
            ("properties", models.JSONField(blank=True, default=dict)), ("created_at", models.DateTimeField(auto_now_add=True)),
        ], options={"ordering":["-created_at"]}),
        migrations.CreateModel(name="Favorite", fields=[
            ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
            ("created_at", models.DateTimeField(auto_now_add=True)),
            ("product", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="favorites", to="core.product")),
            ("user", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="favorites", to=settings.AUTH_USER_MODEL)),
        ]),
        migrations.AddConstraint(model_name="favorite", constraint=models.UniqueConstraint(fields=("user","product"), name="unique_user_favorite")),
        migrations.CreateModel(name="Enquiry", fields=[
            ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
            ("message", models.TextField(max_length=3000)), ("status", models.CharField(choices=[("new","New"),("in_progress","In progress"),("closed","Closed")], default="new", max_length=20)),
            ("created_at", models.DateTimeField(auto_now_add=True)),
            ("product", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to="core.product")),
            ("recipient", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="received_enquiries", to=settings.AUTH_USER_MODEL)),
            ("sender", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="sent_enquiries", to=settings.AUTH_USER_MODEL)),
            ("service", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to="core.service")),
        ], options={"ordering":["-created_at"]}),
    ]
