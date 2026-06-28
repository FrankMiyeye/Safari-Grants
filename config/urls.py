from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import render

# ======= All Views =======
def home(request):
    return render(request, 'home.html')

def opportunities(request):
    return render(request, 'opportunities.html')

def destinations(request):
    return render(request, 'destinations.html')

def register(request):
    return render(request, 'register.html')

def login_page(request):
    return render(request, 'login.html')

def dashboard(request):
    return render(request, 'dashboard.html')

# ======= URL Patterns =======
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('opportunities/', opportunities, name='opportunities'),
    path('destinations/', destinations, name='destinations'),
    path('register/', register, name='register'),
    path('login/', login_page, name='login'),
    path('dashboard/', dashboard, name='dashboard'),
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