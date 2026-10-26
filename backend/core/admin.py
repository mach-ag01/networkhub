from django.contrib import admin
from .models import Profile,Product,Service,Favorite,Enquiry,AnalyticsEvent
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display=("user","role","location","is_verified"); list_filter=("role","is_verified"); search_fields=("user__username","user__email")
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display=("title","owner","category","price_kes","location","is_active"); list_filter=("category","condition","is_active"); search_fields=("title","owner__username")
admin.site.register(Service); admin.site.register(Favorite); admin.site.register(Enquiry); admin.site.register(AnalyticsEvent)
