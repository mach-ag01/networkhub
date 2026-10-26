from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from .models import Profile,Product,Service,Favorite,Enquiry,AnalyticsEvent
User=get_user_model()
class UserSerializer(serializers.ModelSerializer):
    role=serializers.SerializerMethodField()
    location=serializers.SerializerMethodField()
    def get_role(self,obj):
        return "admin" if obj.is_staff else getattr(getattr(obj,"profile",None),"role","buyer")
    def get_location(self,obj):
        return getattr(getattr(obj,"profile",None),"location","")
    class Meta: model=User; fields=["id","username","email","first_name","last_name","role","location","is_staff"]
class RegisterSerializer(serializers.ModelSerializer):
    password=serializers.CharField(write_only=True,validators=[validate_password])
    role=serializers.ChoiceField(choices=Profile.ROLES,default="buyer",write_only=True)
    location=serializers.CharField(max_length=120,required=False,allow_blank=True)
    phone=serializers.CharField(max_length=30,required=False,allow_blank=True)
    class Meta: model=User; fields=["username","email","password","first_name","last_name","role","location","phone"]
    def validate_email(self,v):
        if User.objects.filter(email__iexact=v).exists(): raise serializers.ValidationError("Email already registered.")
        return v
    def create(self,d):
        role=d.pop("role","buyer"); location=d.pop("location",""); phone=d.pop("phone",""); password=d.pop("password")
        user=User(**d); user.set_password(password); user.save(); Profile.objects.create(user=user,role=role,location=location,phone=phone); return user
class ProductSerializer(serializers.ModelSerializer):
    owner_name=serializers.CharField(source="owner.username",read_only=True)
    owner_id=serializers.IntegerField(source="owner.id",read_only=True)
    class Meta: model=Product; fields=["id","owner","owner_id","owner_name","title","description","category","condition","price_kes","location","image_url","stock","is_active","created_at"]; read_only_fields=["owner","is_active","created_at"]
class ServiceSerializer(serializers.ModelSerializer):
    owner_name=serializers.CharField(source="owner.username",read_only=True)
    owner_role=serializers.CharField(source="owner.profile.role",read_only=True)
    class Meta: model=Service; fields=["id","owner","owner_name","owner_role","title","description","category","location","price_from_kes","experience_years","is_active","created_at"]; read_only_fields=["owner","is_active","created_at"]
class FavoriteSerializer(serializers.ModelSerializer):
    product_detail=ProductSerializer(source="product",read_only=True)
    class Meta: model=Favorite; fields=["id","product","product_detail","created_at"]; read_only_fields=["created_at"]
class EnquirySerializer(serializers.ModelSerializer):
    sender_name=serializers.CharField(source="sender.username",read_only=True)
    recipient_name=serializers.CharField(source="recipient.username",read_only=True)
    product_title=serializers.CharField(source="product.title",read_only=True,allow_null=True)
    service_title=serializers.CharField(source="service.title",read_only=True,allow_null=True)
    class Meta: model=Enquiry; fields=["id","sender","sender_name","recipient","recipient_name","product","product_title","service","service_title","message","status","created_at"]; read_only_fields=["sender","recipient","status","created_at"]
    def validate(self,d):
        if bool(d.get("product"))==bool(d.get("service")): raise serializers.ValidationError("Choose exactly one product or service.")
        return d
class AnalyticsSerializer(serializers.ModelSerializer):
    class Meta: model=AnalyticsEvent; fields=["event_type","path","properties"]
    def validate_event_type(self,v):
        if v not in {"page_view","product_search","category_selected"}: raise serializers.ValidationError("Unsupported event.")
        return v
    def validate_properties(self,v):
        if not isinstance(v,dict): raise serializers.ValidationError("Expected object.")
        return {k:x for k,x in v.items() if k in {"query_length","category"}}
