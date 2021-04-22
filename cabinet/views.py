from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import permissions

from .models import Account
from .serializers import AccountSerializer
from company.serializers import RoleSerializer


class UserViewSet(viewsets.GenericViewSet):
    queryset = Account.objects
    serializer_class = AccountSerializer
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request, *args, **kwargs):
        serializer = self.get_serializer(request.user)
        roles_data = []
        for role in request.user.get_roles():
            roles_data.append(RoleSerializer(role).data)
        return Response({
            "account": serializer.data,
            "roles": roles_data
        },
                        template_name="user.html")


@api_view(['GET', 'POST'])
def postData(request):
    print(request.data)
    data = request.data
    return Response(data=data)
