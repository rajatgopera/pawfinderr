from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from puppy_finder import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('', views.index, name='index'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('report/lost/', views.report_lost, name='report_lost'),
    path('report/found/', views.report_found, name='report_found'),
    path('search/', views.search_puppies, name='search'),
    path('puppy/<int:puppy_id>/', views.puppy_detail, name='puppy_detail'),
    path('profile/', views.profile, name='profile'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
