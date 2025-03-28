from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from authentication.serializers import UserSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from drf_spectacular.utils import extend_schema

def generate_user_tokens(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token)
    }

class RegisterAPIView(APIView):
    @extend_schema(
        tags=['Authentication'],
        methods=["POST"],
        description='User Register',
        responses={200: {"message": "User register successfully"}},
    )

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        #tokens = generate_user_tokens(user)
        return Response({"message": "User register successfully"}, status=status.HTTP_201_CREATED)


class LoginAPIView(TokenObtainPairView):
    @extend_schema(
        tags=['Authentication'],
        methods=["POST"],
        description='User Login with Email',
        responses={200: TokenObtainPairSerializer()},
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)