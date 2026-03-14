from adrf.generics import (
    CreateAPIView,
    DestroyAPIView,
    ListAPIView,
    RetrieveAPIView,
    UpdateAPIView,
)
from asgiref.sync import sync_to_async
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Task
from .serializers import (
    TaskCreateSerializer,
    TaskDetailSerializer,
    TaskListSerializer,
    TaskUpdateSerializer,
)


class TodoListView(ListAPIView):
    serializer_class = TaskListSerializer
    permission_classes = (IsAuthenticated,)
    queryset = Task.objects.all()

    async def afilter_queryset(self, queryset):
        return await sync_to_async(list)(queryset.filter(creator=self.request.user))


class TodoDetailView(RetrieveAPIView):
    serializer_class = TaskDetailSerializer
    queryset = Task.objects.all()

    async def retrieve(self, request, pk):
        return await Task.objects.filter(creator=self.request.user, pk=pk).afirst()


class TodoCreateView(CreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskCreateSerializer
    http_method_names = ["post"]


class TodoUpdateView(UpdateAPIView):
    serializer_class = TaskUpdateSerializer
    queryset = Task.objects.all()

    async def update(self, request, pk, **kwargs):
        return await Task.objects.filter(creator=self.request.user, pk=pk).aupdate(
            **kwargs
        )


class TodoDeleteView(DestroyAPIView):
    queryset = Task.objects.all()
    http_method_names = ["delete"]

    async def delete(self, request, pk):
        await Task.objects.filter(creator=self.request.user, pk=pk).adelete()
        return Response(
            data={"msg": "Task was deleted"}, status=status.HTTP_204_NO_CONTENT,
        )
