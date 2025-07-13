from django.urls import path
from .views import RegisterView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


urlpatterns += [
    path('register', RegisterView.as_view()),
    path('token/', TokenObtainPairView.as_view()),
    path('token/refresh', TokenRefreshView.as_view()),
    path('oauth/', include('social_django.urls', namespace='social')),
    path('oauth/success/', google_login_success, name='oauth-success'),
]