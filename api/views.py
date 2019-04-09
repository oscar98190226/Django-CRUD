from django.contrib.auth.models import User
from .models import Entry
from .permissions import UserAccessPermission, EntryAccessPermission

from django.contrib.auth import authenticate, login
from django.shortcuts import get_object_or_404
from rest_framework_jwt.settings import api_settings
from rest_framework import permissions, generics, status, viewsets

from rest_framework.response import Response
from .serializers import TokenSerializer, UserSerializer, EntrySerializer

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
            serializer = TokenSerializer(data={
                # using drf jwt utility functions to generate a token
                "token": jwt_encode_handler(
                    jwt_payload_handler(user)
                )})
            serializer.is_valid()
            return Response(serializer.data)
        return Response(status=status.HTTP_401_UNAUTHORIZED)

class SignupView(generics.CreateAPIView):
    """
    POST auth/register/
    """
    permission_classes = (permissions.AllowAny,)
    serializer_class = UserSerializer

    # def post(self, request, *args, **kwargs):
    #     username = request.data.get("username", "")
    #     password = request.data.get("password", "")
    #     email = request.data.get("email", "")
    #     if not username and not password and not email:
    #         return Response(
    #             data={
    #                 "message": "username, password and email is required to register a user"
    #             },
    #             status=status.HTTP_400_BAD_REQUEST
    #         )
    #     new_user = User.objects.create_user(
    #         username=username, password=password, email=email
    #     )
    #     return Response(status=status.HTTP_201_CREATED)

class UserViewSet(viewsets.ModelViewSet):
    #User CRUD

    serializer_class = UserSerializer
    # queryset = User.objects.all()
    permission_classes = (permissions.IsAuthenticated, UserAccessPermission,)

    def get_queryset(self):
        obj = User.objects.all()
        self.check_object_permissions(self.request, obj)
        return obj

    def get_object(self):
        obj = get_object_or_404(self.get_queryset(), pk=self.kwargs["pk"])
        self.check_object_permissions(self.request, obj)
        return obj

class EntryViewSet(viewsets.ModelViewSet):
    # Entry CRUD

    serializer_class = EntrySerializer
    permission_classes = (permissions.IsAuthenticated, EntryAccessPermission,)
    # queryset = Entry.objects.all()

    def get_queryset(self):
        obj = self.request.user.entry.all()
        self.check_object_permissions(self.request, obj)
        return obj
    
    def get_object(self):
        obj = get_object_or_404(self.get_queryset(), pk=self.kwargs["pk"])
        self.check_object_permissions(self.request, obj)
        return obj


@api_view(['GET'])
@permission_classes((permissions.IsAuthenticated, EntryAccessPermission,))
def WeeklyReport(request):
    report = Entry.objects.annotate(year=ExtractYear('date')).annotate(week=ExtractWeek('date')).values('year', 'week').annotate(totalDistance=Sum('distance')).annotate(totalDuration=Sum('duration'))

    return Response(report)