# accounts/urls.py
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import AdminLoginView, LibrarianLoginView, MemberLoginView,SignupView

urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('login/admin/', AdminLoginView.as_view(), name='admin_login'),
    path('login/librarian/', LibrarianLoginView.as_view(), name='librarian_login'),
    path('login/member/', MemberLoginView.as_view(), name='member_login'),
]
