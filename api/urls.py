from django.urls import path, re_path, include
from rest_framework import routers
from .views import LoginView, SignupView, UserViewSet, EntryViewSet, WeeklyReport

router = routers.DefaultRouter()

router.register(r'user', UserViewSet, basename='user')
router.register(r'entry', EntryViewSet, basename='entry')

auth_urls = [
	path('login/', LoginView.as_view(), name="login"),
	path('signup/', SignupView.as_view(), name="signup")	
]

urlpatterns = [
	path('auth/', include(auth_urls)),
	path('weeklyReport/', WeeklyReport, name="weekly"),
	re_path(r'^', include(router.urls)),
]