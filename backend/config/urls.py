from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView
from core.views import RegisterView, LoginView, ProductViewSet, ServiceViewSet, FavoriteViewSet, EnquiryViewSet, AnalyticsView, HealthView, MeView, AdminOverviewView
router=DefaultRouter()
router.register("products",ProductViewSet,basename="product")
router.register("services",ServiceViewSet,basename="service")
router.register("favorites",FavoriteViewSet,basename="favorite")
router.register("enquiries",EnquiryViewSet,basename="enquiry")
urlpatterns=[path("admin/",admin.site.urls),path("health/",HealthView.as_view()),path("api/v1/auth/register/",RegisterView.as_view()),path("api/v1/auth/login/",LoginView.as_view()),path("api/v1/auth/refresh/",TokenRefreshView.as_view()),path("api/v1/auth/me/",MeView.as_view()),path("api/v1/analytics/events/",AnalyticsView.as_view()),path("api/v1/admin/overview/",AdminOverviewView.as_view()),path("api/v1/",include(router.urls))]
