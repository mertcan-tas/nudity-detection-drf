from rest_framework.generics import RetrieveAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticated

from account.serializers import UserSerializer

from drf_spectacular.utils import extend_schema

@extend_schema(
    tags=['User'],
    methods=["GET"],
    description='Get User Info',
    responses={200: UserSerializer()},
)
class UserDetailView(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user