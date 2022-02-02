from django.contrib import admin
from django.urls import path
from django.contrib.auth.views import LogoutView

from base import views
from base.views.pay_views import PayCancelView, PaySuccessView
urlpatterns = [
    path('admin/', admin.site.urls),

    #index
    path('', views.IndexView.as_view()),
    path('book/<str:pk>', views.BooksDetailView.as_view()),

    #cart
    path('cart/', views.CartListView.as_view()),
    path('cart/add/', views.AddCartView.as_view()),
    path('cart/remove/<str:pk>/', views.remove_from_cart),

    #Pay
    path('pay/checkout/', views.PayWithStripe.as_view()),
    path('pay/success/', views.PaySuccessView.as_view()),
    path('pay/cancel/', views.PayCancelView.as_view()),

    #Account
    path('login/', views.Login.as_view()),
    path('logout/', LogoutView.as_view()),
    path('signup/', views.SignUpView.as_view()),
    path('account/', views.AccountUpdateView.as_view()),
    path('profile/', views.ProfileUpdateView.as_view()),


]
