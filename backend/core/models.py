from django.conf import settings
from django.db import models
class Profile(models.Model):
    ROLES=[("buyer","Buyer"),("seller","Seller"),("technician","Technician")]
    user=models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name="profile")
    role=models.CharField(max_length=20,choices=ROLES,default="buyer")
    phone=models.CharField(max_length=30,blank=True)
    location=models.CharField(max_length=120,blank=True)
    bio=models.TextField(blank=True)
    is_verified=models.BooleanField(default=False)
    def __str__(self): return f"{self.user.username} ({self.role})"
class Product(models.Model):
    CATEGORIES=[("routers","Routers & Wi-Fi"),("switches","Switches & Hubs"),("cctv","CCTV & Security"),("fiber","Fiber & Accessories"),("servers","Servers & Storage"),("other","Other")]
    CONDITIONS=[("new","New"),("refurbished","Refurbished"),("used","Used")]
    owner=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name="products")
    title=models.CharField(max_length=180); description=models.TextField()
    category=models.CharField(max_length=30,choices=CATEGORIES,default="other")
    condition=models.CharField(max_length=20,choices=CONDITIONS,default="new")
    price_kes=models.DecimalField(max_digits=12,decimal_places=2)
    location=models.CharField(max_length=120,default="Nairobi")
    image_url=models.URLField(blank=True); stock=models.PositiveIntegerField(default=1)
    is_active=models.BooleanField(default=True); created_at=models.DateTimeField(auto_now_add=True); updated_at=models.DateTimeField(auto_now=True)
    class Meta: ordering=["-created_at"]
class Service(models.Model):
    owner=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name="services")
    title=models.CharField(max_length=180); description=models.TextField()
    category=models.CharField(max_length=100,default="Network installation"); location=models.CharField(max_length=120,default="Nairobi")
    price_from_kes=models.DecimalField(max_digits=12,decimal_places=2,default=0); experience_years=models.PositiveIntegerField(default=0)
    is_active=models.BooleanField(default=True); created_at=models.DateTimeField(auto_now_add=True)
    class Meta: ordering=["-created_at"]
class Favorite(models.Model):
    user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name="favorites")
    product=models.ForeignKey(Product,on_delete=models.CASCADE,related_name="favorites"); created_at=models.DateTimeField(auto_now_add=True)
    class Meta: constraints=[models.UniqueConstraint(fields=["user","product"],name="unique_user_favorite")]
class Enquiry(models.Model):
    STATUS=[("new","New"),("in_progress","In progress"),("closed","Closed")]
    sender=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name="sent_enquiries")
    recipient=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name="received_enquiries")
    product=models.ForeignKey(Product,null=True,blank=True,on_delete=models.SET_NULL)
    service=models.ForeignKey(Service,null=True,blank=True,on_delete=models.SET_NULL)
    message=models.TextField(max_length=3000); status=models.CharField(max_length=20,choices=STATUS,default="new"); created_at=models.DateTimeField(auto_now_add=True)
    class Meta: ordering=["-created_at"]
class AnalyticsEvent(models.Model):
    event_type=models.CharField(max_length=60); path=models.CharField(max_length=300,blank=True); properties=models.JSONField(default=dict,blank=True); created_at=models.DateTimeField(auto_now_add=True)
    class Meta: ordering=["-created_at"]
