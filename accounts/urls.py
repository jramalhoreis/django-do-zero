
from django.urls import path

from accounts import views


urlpatterns = [
    path('accounts/signup', views.AccountCreateView.as_view(), name='signup'),
    path('accounts/edit/<int:pk>', views.AccountUpdateView.as_view(), name="account_edit_perfil"),
    path('accounts/profile', views.AccountTemplateView.as_view(), name='account_detail')
]
