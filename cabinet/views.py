from django.contrib.auth.models import User
from rest_framework import serializers, viewsets, mixins
from rest_framework.decorators import action
from rest_framework.decorators import api_view
from rest_framework.response import Response


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'is_staff']


# ViewSets define the view behavior.
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


data = {}


@api_view(['GET', 'POST'])
def postData(request):
    print(request.data)
    global data
    data = request.data
    return Response(data=data)


@api_view(['GET', 'POST'])
def getData(request):
    global data
    return Response(data=data)