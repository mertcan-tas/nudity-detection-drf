from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from authentication.serializers import UserSerializer

def generate_user_tokens(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token)
    }

class RegisterEmailView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        #tokens = generate_user_tokens(user)
        return Response({"message": "User register successfully"}, status=status.HTTP_201_CREATED)
