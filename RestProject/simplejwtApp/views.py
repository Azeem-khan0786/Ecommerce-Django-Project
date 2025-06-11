
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from simplejwtApp.serializers import UserSerializer


class HomeView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        user =request.user
        user_serializer = UserSerializer(user)
        data = {
            'message': 'Hello, World!',
            'user': user_serializer.data
        }
        return Response(data)

