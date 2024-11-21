"""
URL configuration for mealgenie project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path

from users.views import login_view, register_view, logout_view, home_view, profile_view, grocery_list_view, add_grocery_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', login_view, name='login'),
    path('register/', register_view, name='register'),
    path('home/<str:username>', home_view, name='home'),
    path('home/profile/', profile_view, name='profile'),
    path('logout/', logout_view, name='logout'),
    path('home/grocery-list/', grocery_list_view, name='grocery_list'),
    # path('home/<str:username>#my-groceries', name='my_groceries'),
    path('home/grocery-list/add', add_grocery_view, name='add_grocery'),
]