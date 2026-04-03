from django.urls import include, path
from rest_framework import routers
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from accounts.views.viewsets import UserViewSet, GroupViewSet
from accounts.views.tokens import CustomTokenView, RefreshView
from accounts.views.auth import RegisterView, LoginView, LogoutView


router = routers.DefaultRouter()
router.register(r"users", UserViewSet)
router.register(r"groups", GroupViewSet)

urlpatterns = [
	path("", include(router.urls)),
	path("register/", RegisterView.as_view(), name="register"),
	path("login/", LoginView.as_view(), name="login_manual"),
	path("logout/", LogoutView.as_view(), name="logout"),
	path("refresh/", RefreshView.as_view(), name="token_refresh_cookie"),
]
