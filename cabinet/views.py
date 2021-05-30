from django.shortcuts import redirect
from rest_framework import serializers, viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import permissions

from .models import Account
from .serializers import AccountSerializer, RegistrationRequestSerializer
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


class StartPageView(viewsets.ViewSet):
    def get_client_ip(self):
        x_forwarded_for = self.request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            return x_forwarded_for.split(',')[0]
        elif self.request.META.get('HTTP_X_REAL_IP'):
            return self.request.META.get('HTTP_X_REAL_IP')
        else:
            return self.request.META.get('REMOTE_ADDR')

    def list(self, request, *args, **kwargs):
        return Response(template_name="start.html")

    def retrieve(self, request, *args, **kwargs):
        return Response({"pk": kwargs.get("pk")}, template_name="start.html")

    def create(self, request, *args, **kwargs):
        try:
            serializer = RegistrationRequestSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save(ip=self.get_client_ip())
            return redirect('start-detail', pk=serializer.data.get("id"))
        except Exception as e:
            print(e)
            return Response({'error': str(e)}, template_name="start.html")


@api_view(['GET', 'POST'])
def postData(request):
    print(request.data)
    data = request.data
    return Response(data=data)
