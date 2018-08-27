from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^get_active_user/', views.ActiveUserApiView.as_view()),
    url(r'^get_total_revenue/', views.TotalRevenueApiView.as_view()),
]