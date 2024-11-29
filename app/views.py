from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .serializers import AuthorSerializer, MessageSerializer
from .models import Author, Message
from django.utils import timezone


@api_view(["POST"])
def create_author(request):
    username = request.data.get("username")

    if not username:
        return Response(
            {"error": "Error al crear el Author."}, status=status.HTTP_404_NOT_FOUND
        )

    author, _ = Author.objects.get_or_create(name=username)

    serializer = AuthorSerializer(author, data=request.data, partial=True)

    if serializer.is_valid():
        return Response(serializer.data, status=status.HTTP_200_OK)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
def get_messages(request):
    messages = Message.objects.all().order_by("created_at")
    serializer = MessageSerializer(messages, many=True)
    return Response(serializer.data)


@api_view(["POST"])
def create_message(request):
    username = request.data.get("username")
    content = request.data.get("content")
    image = request.FILES.get("image")
    pdf_file = request.FILES.get("pdf_file")

    if not username:
        return Response(
            {"error": "El nombre de usuario es requerido."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    author = Author.objects.get(name=username)

    # Determine message type
    if image:
        message_type = "image"
        serializer = MessageSerializer(
            data={"message_type": message_type, "image": image}
        )
    elif pdf_file:
        # Validate PDF file
        if not pdf_file.name.lower().endswith(".pdf"):
            return Response(
                {"error": "Solo se permiten archivos PDF."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        message_type = "pdf"
        serializer = MessageSerializer(
            data={"message_type": message_type, "pdf_file": pdf_file}
        )
    else:
        # Text message
        if not content:
            return Response(
                {"error": "El contenido es requerido para mensajes de texto."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        message_type = "text"
        serializer = MessageSerializer(
            data={"content": content, "message_type": message_type}
        )

    if serializer.is_valid():
        serializer.save(author=author)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["DELETE"])
def delete_message(request, message_id):
    try:
        message = Message.objects.get(id=message_id)
    except Message.DoesNotExist:
        return Response(
            {"error": "Mensaje no encontrado."}, status=status.HTTP_404_NOT_FOUND
        )

    # Check if the user is the author of the message
    username = request.data.get("username")
    if not username or message.author.name != username:
        return Response(
            {"error": "No tienes permiso para eliminar este mensaje."},
            status=status.HTTP_403_FORBIDDEN,
        )

    message.delete()
    return Response(
        {"message": "Mensaje eliminado correctamente."}, status=status.HTTP_200_OK
    )


@api_view(["POST"])
def update_user_status(request, username):
    author = Author.objects.get(name=username)
    is_online = request.data.get("is_online")
    author.is_online = is_online
    author.last_activity = timezone.now()
    author.save()

    serializer = AuthorSerializer(author)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["PUT"])
def update_profile_picture(request, author_id):
    try:
        author = Author.objects.get(id=author_id)
    except Author.DoesNotExist:
        return Response(
            {"error": "Autor no encontrado."}, status=status.HTTP_404_NOT_FOUND
        )

    serializer = AuthorSerializer(author, data=request.data, partial=True)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
def get_author_by_username(request, username):
    try:
        author = Author.objects.get(name=username)
    except Author.DoesNotExist:
        return Response(
            {"error": "Autor no encontrado."}, status=status.HTTP_404_NOT_FOUND
        )

    serializer = AuthorSerializer(author, data=request.data, partial=True)

    if serializer.is_valid():
        return Response(serializer.data, status=status.HTTP_200_OK)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
