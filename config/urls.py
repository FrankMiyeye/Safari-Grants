from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import render

# Import accounts views
from accounts.views import (
    register_view,
    login_view,
    logout_view,
    dashboard_view,
)

# ======= Simple Page Views =======
def home(request):
    return render(request, 'home.html')

def opportunities(request):
    return render(request, 'opportunities.html')

def destinations(request):
    return render(request, 'destinations.html')

# ======= URL Patterns =======
urlpatterns = [
    path('admin/', admin.site.urls),

    # Main pages
    path('', home, name='home'),
    path('opportunities/', opportunities, name='opportunities'),
    path('destinations/', destinations, name='destinations'),

    # Auth pages
    path('register/', register_view, name='register'),
    path('login/',    login_view,    name='login'),
    path('logout/',   logout_view,   name='logout'),
    path('dashboard/', dashboard_view, name='dashboard'),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )
    urlpatterns += static(
        settings.STATIC_URL,
        document_root=settings.STATICFILES_DIRS[0]
    )