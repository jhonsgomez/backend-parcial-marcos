from django.urls import path
from . import views

urlpatterns = [
    path("messages/", view=views.get_messages, name="get-messages"),
    path("messages/create/", view=views.create_message, name="create-message"),
    path(
        "messages/<int:message_id>/delete/", 
        view=views.delete_message, 
        name="delete-message"
    ),
    path(
        "authors/create/", 
        view=views.create_author, 
        name="create-author"
    ),
    path(
        "authors/<str:username>/", 
        view=views.get_author_by_username, 
        name="get-author-by-username"
    ),
    path(
        "authors/<int:author_id>/profile_picture/", 
        view=views.update_profile_picture, 
        name="update-profile-picture"
    ),
    path(
        "authors/<str:username>/status/", 
        view=views.update_user_status, 
        name="update-user-status"
    )
]