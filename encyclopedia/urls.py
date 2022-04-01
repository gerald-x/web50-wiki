from django.urls import path

from . import views

app_name = 'wiki'
urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.title, name="title"),
    path("wiki/search/", views.search_page, name="search"),
    path("wiki/new_page/", views.new_page, name="new_page"),
    path("wiki/edit/", views.edit_page, name="edit"),
    path("wiki/save_page/", views.save_page, name="save_page"),
    path("wiki/random_page/", views.random_page, name="random_page")
]
