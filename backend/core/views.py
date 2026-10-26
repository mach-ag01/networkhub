from django.contrib.auth import authenticate,get_user_model
from django.db.models import Count
from rest_framework import generics,permissions,viewsets,status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.throttling import AnonRateThrottle,UserRateThrottle,ScopedRateThrottle
from rest_framework.exceptions import ValidationError,PermissionDenied
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Profile,Product,Service,Favorite,Enquiry,AnalyticsEvent
from .serializers import RegisterSerializer,UserSerializer,ProductSerializer,ServiceSerializer,FavoriteSerializer,EnquirySerializer,AnalyticsSerializer
User=get_user_model()
class LoginThrottle(AnonRateThrottle): scope="login"
class RegisterThrottle(AnonRateThrottle): scope="register"
class ContactThrottle(UserRateThrottle): scope="contact"
class RegisterView(generics.CreateAPIView):
    serializer_class=RegisterSerializer; permission_classes=[permissions.AllowAny]; throttle_classes=[RegisterThrottle]
    def create(self,request,*a,**kw):
        s=self.get_serializer(data=request.data); s.is_valid(raise_exception=True); u=s.save(); r=RefreshToken.for_user(u)
        return Response({"user":UserSerializer(u).data,"refresh":str(r),"access":str(r.access_token)},status=201)
class LoginView(APIView):
    permission_classes=[permissions.AllowAny]; throttle_classes=[LoginThrottle]
    def post(self,request):
        identifier=str(request.data.get("username","")).strip(); password=request.data.get("password","")
        u=authenticate(request,username=identifier,password=password)
        if u is None and identifier:
            try: u=authenticate(request,username=User.objects.get(email__iexact=identifier).username,password=password)
            except User.DoesNotExist: u=None
        if u is None: return Response({"detail":"Invalid username/email or password."},status=400)
        r=RefreshToken.for_user(u); return Response({"user":UserSerializer(u).data,"refresh":str(r),"access":str(r.access_token)})
class MeView(generics.RetrieveAPIView):
    serializer_class=UserSerializer; permission_classes=[permissions.IsAuthenticated]
    def get_object(self): return self.request.user
class HealthView(APIView):
    authentication_classes=[]; permission_classes=[permissions.AllowAny]
    def get(self,request): return Response({"status":"ok"})
class ProductViewSet(viewsets.ModelViewSet):
    serializer_class=ProductSerializer; filterset_fields=["category","condition","location"]; search_fields=["title","description","location","owner__username"]; ordering_fields=["price_kes","created_at","title"]
    def get_queryset(self):
        qs=Product.objects.select_related("owner").filter(is_active=True)
        if self.request.user.is_authenticated and self.request.user.is_staff and self.request.query_params.get("include_inactive")=="true": qs=Product.objects.select_related("owner").all()
        if self.action in ("update","partial_update","destroy") and self.request.user.is_authenticated: return Product.objects.filter(owner=self.request.user) if not self.request.user.is_staff else Product.objects.all()
        if self.request.query_params.get("price_min"): qs=qs.filter(price_kes__gte=self.request.query_params["price_min"])
        if self.request.query_params.get("price_max"): qs=qs.filter(price_kes__lte=self.request.query_params["price_max"])
        return qs
    def get_permissions(self):
        if self.action in ("create","update","partial_update","destroy"): return [permissions.IsAuthenticated(),IsSeller()]
        return [permissions.AllowAny()]
    def perform_create(self,s): s.save(owner=self.request.user)
class IsSeller(permissions.BasePermission):
    def has_permission(self,request,view):
        return bool(request.user and request.user.is_authenticated and (request.user.is_staff or getattr(getattr(request.user,"profile",None),"role","")=="seller"))
    def has_object_permission(self,request,view,obj): return request.user.is_staff or obj.owner_id==request.user.id
class ServiceViewSet(viewsets.ModelViewSet):
    serializer_class=ServiceSerializer; filterset_fields=["category","location"]; search_fields=["title","description","location","owner__username"]; ordering_fields=["price_from_kes","experience_years","created_at"]
    def get_queryset(self):
        if self.action in ("update","partial_update","destroy") and self.request.user.is_authenticated: return Service.objects.filter(owner=self.request.user) if not self.request.user.is_staff else Service.objects.all()
        return Service.objects.select_related("owner","owner__profile").filter(is_active=True)
    def get_permissions(self):
        return [permissions.IsAuthenticated()] if self.action in ("create","update","partial_update","destroy") else [permissions.AllowAny()]
    def perform_create(self,s):
        if not self.request.user.is_staff and getattr(self.request.user.profile,"role","")!="technician": raise PermissionDenied("Only technician accounts can publish services.")
        s.save(owner=self.request.user)
class FavoriteViewSet(viewsets.ModelViewSet):
    serializer_class=FavoriteSerializer; permission_classes=[permissions.IsAuthenticated]; http_method_names=["get","post","delete","head","options"]
    def get_queryset(self): return Favorite.objects.filter(user=self.request.user).select_related("product","product__owner")
    def perform_create(self,s):
        if Favorite.objects.filter(user=self.request.user,product=s.validated_data["product"]).exists(): raise ValidationError({"product":"Already saved."})
        s.save(user=self.request.user)
class EnquiryViewSet(viewsets.ModelViewSet):
    serializer_class=EnquirySerializer; permission_classes=[permissions.IsAuthenticated]; http_method_names=["get","post","patch","head","options"]; throttle_classes=[ContactThrottle]
    def get_queryset(self): return Enquiry.objects.filter(sender=self.request.user)|Enquiry.objects.filter(recipient=self.request.user)
    def perform_create(self,s):
        d=s.validated_data; target=d["product"].owner if d.get("product") else d["service"].owner
        if target==self.request.user: raise ValidationError("You cannot enquire about your own listing.")
        s.save(sender=self.request.user,recipient=target)
    def partial_update(self,request,*a,**kw):
        obj=self.get_object()
        if obj.recipient_id!=request.user.id and not request.user.is_staff: raise PermissionDenied("Only the recipient can update status.")
        if set(request.data)-{"status"}: raise ValidationError("Only status can be changed.")
        return super().partial_update(request,*a,**kw)
class AnalyticsView(generics.CreateAPIView):
    serializer_class=AnalyticsSerializer; permission_classes=[permissions.AllowAny]; throttle_classes=[ScopedRateThrottle]; throttle_scope="analytics"
    def create(self,request,*a,**kw):
        s=self.get_serializer(data=request.data); s.is_valid(raise_exception=True); s.save()
        return Response({"accepted":True},status=201)
class AdminOverviewView(APIView):
    permission_classes=[permissions.IsAdminUser]
    def get(self,request):
        return Response({"users":User.objects.count(),"products":Product.objects.count(),"active_products":Product.objects.filter(is_active=True).count(),"services":Service.objects.count(),"pending_approvals":Product.objects.filter(is_active=False).count(),"enquiries":Enquiry.objects.count(),"users_by_role":list(Profile.objects.values("role").annotate(total=Count("id")))})
