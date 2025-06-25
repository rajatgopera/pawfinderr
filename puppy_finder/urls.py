from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('report_lost/', views.report_lost, name='report_lost'),
    path('report_found/', views.report_found, name='report_found'),
    path('search/', views.search_puppies, name='search'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('puppy/<int:puppy_id>/', views.puppy_detail, name='puppy_detail'),
    path('profile/', views.profile, name='profile'),
    path('mark_reunited/<int:puppy_id>/', views.mark_as_reunited, name='mark_reunited'),
    path('', views.index, name='index'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
