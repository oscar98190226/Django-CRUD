from django.urls import path, include
from .views import LoginView, SignupView, UserViewSet

auth_urls = [
	path('login/', LoginView.as_view(), name="login"),
	path('signup/', SignupView.as_view(), name="signup")	
]

urlpatterns = [
	path('auth/', include(auth_urls)), 
	path('user/', UserViewSet)
]