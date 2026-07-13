from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import render
from django.contrib.sitemaps.views import sitemap
from config.sitemaps import StaticViewSitemap
from django.contrib.sitemaps.views import sitemap
from config.sitemaps import StaticViewSitemap

sitemaps = {
    'static': StaticViewSitemap,
}


from accounts.views import (
    register_view,
    login_view,
    logout_view,
    dashboard_view,
)
from django.views.generic import TemplateView

# Add to urlpatterns:
path('robots.txt', TemplateView.as_view(
    template_name='robots.txt',
    content_type='text/plain'
), name='robots'),

# ======= Simple Page Views =======
def home(request):
    return render(request, 'home.html')

def opportunities(request):
    return render(request, 'opportunities.html')

def destinations(request):
    return render(request, 'destinations.html')

def profile(request):
    return render(request, 'profile.html')

def contact(request):
    return render(request, 'contact.html')

def blog(request):
    return render(request, 'blog.html')

def packages(request):
    return render(request, 'packages.html')

# ======= URL Patterns =======
urlpatterns = [
    path('admin/', admin.site.urls),

    # Main pages
    path('',               home,          name='home'),
    path('opportunities/', opportunities, name='opportunities'),
    path('destinations/',  destinations,  name='destinations'),
    path('profile/',       profile,       name='profile'),
    path('contact/',       contact,       name='contact'),
    path('blog/',          blog,          name='blog'),
    path('packages/', packages, name='packages'),
    path('sitemap.xml', sitemap, {'sitemaps': {'static': StaticViewSitemap}}, name='sitemap'),

    # Auth pages
    path('register/',  register_view,  name='register'),
    path('login/',     login_view,     name='login'),
    path('logout/',    logout_view,    name='logout'),
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
