from django.urls import path

from . import views

app_name = 'encyclopedia'

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:filename>/", views.markdown_view, name="filename"),
    path("wiki/search", views.search_page, name="search_page"),
    path("wiki/create", views.create_page, name="create_page"),
    path("wiki/save_page", views.save_page, name="save_page"),
    path("edit/<str:filename>", views.edit_page, name="edit_page"),
    path("wiki/random_page", views.random_page, name="random_page"),
]
