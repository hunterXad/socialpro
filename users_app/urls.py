from django.urls import path 
from .views import *
from django.conf.urls.static import static
from django.conf import settings



urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('signup/', UserSignupView.as_view(), name='signup'),
    path('login/', UserLoginView.as_view(), name='login'),  
    path('logout/', UserLogoutView.as_view(), name='logout'), 
    path('profile/', ProfileView.as_view(), name='profile'),
    path('profile/<str:username>/', ProfileDetailView.as_view(), name='profile')

    
]   + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
