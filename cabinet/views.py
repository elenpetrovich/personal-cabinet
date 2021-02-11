from django.contrib.auth.models import User
from rest_framework import serializers, viewsets, mixins, views, status
from rest_framework.decorators import api_view, action
from rest_framework.response import Response

from .models import Account
from .serializers import AccountSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = AccountSerializer

    @action(detail=False, methods=['post'], url_path="many")
    def create_many(self, request, *args, **kwargs):
        data = []
        for user in request.data.get("users"):
            serializer = self.get_serializer(data=user)
            if serializer.is_valid(raise_exception=False):
                self.perform_create(serializer)
                data.append(serializer.data)
        return Response(data, status=status.HTTP_201_CREATED)


@api_view(['GET', 'POST'])
def postData(request):
    print(request.data)
    data = request.data
    return Response(data=data)
