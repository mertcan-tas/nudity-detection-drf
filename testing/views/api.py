from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from drf_spectacular.utils import extend_schema

class NoAuthTokenView(APIView):
    @extend_schema(
        tags=['Testing'],
        methods=["POST"],
        description='Obtain JWT token pair for testing user authentication',
        responses={
            200: {
                "type": "object",
                "properties": {
                    "refresh": {"type": "string"},
                    "access": {"type": "string"}
                }
            }
        }
    )

    def get(self, request):
        user = get_user_model().objects.first()
        refresh = RefreshToken.for_user(user)
        
        return Response({
            "refresh": str(refresh),
            "access": str(refresh.access_token)
        })