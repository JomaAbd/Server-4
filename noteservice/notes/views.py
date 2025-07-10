from django.shortcuts import render

# Create your views here.
from rest_framework import generics, permissions
from .models import Note
from .serializers import NoteSerializer
from .permissions import IsOwner
from django.core.cache import cache

class NoteListCreateView(generics.ListCreateAPIView):
    serializer_class = NoteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        key = f"notes_user_{self.request.user.id}"
        notes = cache.get(key)
        if notes is None:
            notes = Note.objects.filter(user=self.request.user)
            cache.set(key, notes, timeout=30)
        return notes

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        cache.delete(f"notes_user_{self.request.user.id}")

class NoteDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = NoteSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def get_queryset(self):
        return Note.objects.filter(user=self.request.user)

    def perform_update(self, serializer):
        serializer.save()
        cache.delete(f"notes_user_{self.request.user.id}")

    def perform_destroy(self, instance):
        instance.delete()
        cache.delete(f"notes_user_{self.request.user.id}")
