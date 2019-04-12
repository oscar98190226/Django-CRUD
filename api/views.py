from django.contrib.auth.models import User
from .models import Entry
from .permissions import UserAccessPermission, EntryAccessPermission

from django.contrib.auth import authenticate, login
from django.shortcuts import get_object_or_404
from rest_framework_jwt.settings import api_settings
from rest_framework import permissions, generics, status, viewsets

from rest_framework.response import Response
from .serializers import TokenSerializer, UserSerializer, EntrySerializer, SignupSerializer

# from rest_framework import generics 
from django.db.models import Sum
from django.db.models.functions import ExtractYear, ExtractWeek
from rest_framework.decorators import api_view, permission_classes

# Get the JWT settings, add these lines after the import/from lines
jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

class LoginView(generics.CreateAPIView):
    """
    POST auth/login/
    """
    # This permission class will overide the global permission
    # class setting
    permission_classes = (permissions.AllowAny,)

    queryset = User.objects.all()

    def post(self, request, *args, **kwargs):
        username = request.data.get("username", "")
        password = request.data.get("password", "")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            # login saves the user’s ID in the session,
            # using Django’s session framework.
            login(request, user)

            return Response(data = {
                # using drf jwt utility functions to generate a token
                "token": jwt_encode_handler(
                    jwt_payload_handler(user)
                ),
                "id": user.id, 
                "username": user.username, 
                "email": user.email, 
                "role": user.profile.role
            })
        return Response(status=status.HTTP_401_UNAUTHORIZED)

class SignupView(generics.CreateAPIView):
    """
    POST auth/register/
    """
    permission_classes = (permissions.AllowAny,)
    serializer_class = SignupSerializer

class UserViewSet(viewsets.ModelViewSet):
    #User CRUD
    permission_classes = (permissions.IsAuthenticated, UserAccessPermission,)

    def get_queryset(self):
        obj = User.objects.all()
        self.check_object_permissions(self.request, obj)
        return obj

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return SignupSerializer
        return UserSerializer

class EntryViewSet(viewsets.ModelViewSet):
    # Entry CRUD

    serializer_class = EntrySerializer
    permission_classes = (permissions.IsAuthenticated, EntryAccessPermission,)

    def get_queryset(self):
        from_date = self.request.query_params.get('from', '1970-01-01')
        to_date = self.request.query_params.get('to', '2100-01-01')
        obj = self.request.user.entry.filter(date__gte=from_date, date__lte=to_date)
        if self.request.user.profile.role == 'ADMIN':
            obj = Entry.objects.filter(date__gte=from_date, date__lte=to_date)
        self.check_object_permissions(self.request, obj)
        return obj


@api_view(['GET'])
@permission_classes((permissions.IsAuthenticated, EntryAccessPermission,))
def WeeklyReport(request):
    report = Entry.objects \
                .annotate(year=ExtractYear('date')) \
                .annotate(week=ExtractWeek('date')) \
                .values('year', 'week') \
                .annotate(totalDistance=Sum('distance')) \
                .annotate(totalDuration=Sum('duration'))

    return Response(report)