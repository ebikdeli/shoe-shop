"""
** It's highly recommended to override 'viewset' list or retreive method to send 'request' via the Serializer
'context' attribute to be able do somethings in Serializer body.

** When we use Serailizer inheritance, we can use in serializer class we want among parent or child
class.

** To change 'lookup_field' attribute. And of course we should change 'lookupfield' on 'url' field of the related serializer
IMPORTANT: But beware if change 'lookup_field' attribute, 'tests' must be written generics to support arbitrary 'lookup_field'.
"""
from django.shortcuts import render
from django.contrib.auth import get_user_model
from rest_framework.viewsets import ModelViewSet
from rest_framework import status
from rest_framework import permissions
from rest_framework import authentication
from rest_framework.response import Response
from django_filters import rest_framework as filters

from .models import Address
from .serializers import UserSerializer, AddressSerializer, UserNewSerializer
from .filters import UserFilterSet, AddressFilterSet
from .forms import AddressForm


class UserViewSet(ModelViewSet):
    """This ViewSet used for list, retreive, post and update User model"""
    queryset = get_user_model().objects.all()
    serializer_class = UserNewSerializer
    # In production we rather use 'permissions.IsAdminUser' but for dev we use 'AllowAny'
    # permission_classes = [permissions.IsAdminUser, ]
    permission_classes = [permissions.AllowAny, ]
    # authentication_classes = [authentication.TokenAuthentication, authentication.SessionAuthentication, ]
    filter_backends = (filters.DjangoFilterBackend, )
    filterset_class = UserFilterSet
    lookup_field = get_user_model().USERNAME_FIELD

    def get_queryset(self):
        """Override this method. Remember it's so much faster to use 'get_queryset' method instead of 'queryset' attribute"""
        if self.request.user.is_authenticated:
            if self.request.user.is_staff:
                queryset = get_user_model().objects.all()
            else:
                queryset = get_user_model().objects.filter(id=self.request.user.id)
        else:
            queryset = get_user_model().objects.none()
        return queryset

    def list(self, request, *args, **kwargs):
        """Override 'list' method to send 'request' object to serializer - although it's not needed for ModelSerializer"""
        queryset = get_user_model().objects.all()
        # queryset = self.get_queryset()
        # We can add new fields to any queryset without any problem
        for q in queryset:
            q.new_field = 'This is new field to send to the front'
        if queryset.exists():
            serializer = UserNewSerializer(instance=queryset, many=True, context={'request': request})
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        return Response(data='Error: User is not authenticated!', status=status.HTTP_200_OK)
    

class AddressViewSet(ModelViewSet):
    """This ViewSet used for list, retreive, post and update Address model"""
    queryset = Address.objects.all()
    serializer_class = AddressSerializer
    permission_classes = [permissions.IsAdminUser, ]
    authentication_classes = [authentication.TokenAuthentication, authentication.SessionAuthentication, ]
    filter_backends = (filters.DjangoFilterBackend, )
    filterset_class = AddressFilterSet

    def list(self, request, *args, **kwargs):
        """Override 'list' method to send 'request' object to serializer - although it's not needed for ModelSerializer"""
        queryset = Address.objects.all()
        serializer = AddressSerializer(instance=queryset, many=True, context={'request': request})
        return Response(data=serializer.data, status=status.HTTP_200_OK)


def address_add(request):
    """To demonstrate how to queryset data for a form"""
    address = request.user.address_set if request.user.is_authenticated else None
    if request.method == 'POST':
        address_form = AddressForm(data=request.POST, files=request.FILES, instance=address)
        
    else:
        address_form = AddressForm(instance=address)
        # If 'Address.user' field was '1t1', 'm2m' or 'ForeignKey', we could had changed queryset
        # for the field in the model form to something like this:
        # address_form.fields['user'].queryset = get_user_model().objects.filter(first_name__in='ehsan')
    return render(request, 'accounts/address_add.html', {'form': address_form})