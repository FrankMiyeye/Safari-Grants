from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import render

# ======= Temporary Views =======
def home(request):
    return render(request, 'home.html')

def opportunities(request):
    return render(request, 'opportunities.html')

def destinations(request):
    return render(request, 'destinations.html')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('opportunities/', opportunities, name='opportunities'),
    path('destinations/', destinations, name='destinations'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])