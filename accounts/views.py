from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.response import Response
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import status, generics, serializers
from .models import Profile
from .serializers import UserSignupSerializer

class SignupView(generics.CreateAPIView):
    serializer_class = UserSignupSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({"message": "User registered successfully"}, status=status.HTTP_201_CREATED)

class RoleBasedTokenObtainSerializer(TokenObtainPairSerializer):
    expected_role = None  # define in subclass

    def validate(self, attrs):
        data = super().validate(attrs)
        user = self.user  # serializer sets this correctly
        profile = getattr(user, 'profile', None)
        if not profile or profile.role != self.expected_role:
            raise serializers.ValidationError("Invalid role for this endpoint")
        return data


class AdminLoginView(TokenObtainPairView):
    serializer_class = type(
        'AdminSerializer',
        (RoleBasedTokenObtainSerializer,),
        {'expected_role': 'admin'}
    )


class LibrarianLoginView(TokenObtainPairView):
    serializer_class = type(
        'LibrarianSerializer',
        (RoleBasedTokenObtainSerializer,),
        {'expected_role': 'librarian'}
    )


class MemberLoginView(TokenObtainPairView):
    serializer_class = type(
        'MemberSerializer',
        (RoleBasedTokenObtainSerializer,),
        {'expected_role': 'member'}
    )