from django.db import models


# Create your models here.
class Author(models.Model):
    name = models.CharField(max_length=150, unique=True)
    profile_picture = models.ImageField(
        upload_to="profile_pictures/", blank=True, null=True
    )
    is_online = models.BooleanField(default=False)
    last_activity = models.DateTimeField(null=True, blank=True)


class Message(models.Model):
    MESSAGE_TYPES = (("text", "Text"), ("image", "Image"), ("pdf", "PDF File"))

    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    content = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to="chat_images/", blank=True, null=True)
    pdf_file = models.FileField(upload_to="chat_pdfs/", blank=True, null=True)
    message_type = models.CharField(
        max_length=10, choices=MESSAGE_TYPES, default="text"
    )
    created_at = models.DateTimeField(auto_now_add=True)
