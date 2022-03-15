from django.urls import path
from .views import index, add_production, RegisterUserView,\
    RegisterDoneView, user_activate,\
    SebLoginView, SLogoutView,\
    ChangeUserInfoView, SeboPasswordChangeView, \
    profile, get_category, category_filter, product_profile, delete_product


urlpatterns = [
    path('', index, name='index'),
    path('add', add_production, name='add'),
    path('register', RegisterUserView.as_view(), name='register'),
    path('register_done', RegisterDoneView.as_view(), name='register_done'),
    path('register/activate/<str:sign>/', user_activate, name='register_activate'),
    path('login', SebLoginView.as_view(), name='login'),
    path('logout', SLogoutView.as_view(), name='logout'),
    path('profile_change', ChangeUserInfoView.as_view(), name='profile_change'),
    path('profile', profile, name='profile'),
    path('password_change', SeboPasswordChangeView.as_view(), name='password_change'),
    path('category', get_category, name='get_category'),
    path('category_filter', category_filter, name='category_filter'),
    path('product/<int:pk>/', product_profile, name='product_profile'),
    path('delete_product', delete_product, name='delete_product')

]
app_name = 'sebo'

