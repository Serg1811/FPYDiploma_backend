import mimetypes
import logging

from django.http import FileResponse
from django.utils.timezone import now
from rest_framework import viewsets
from rest_framework.generics import get_object_or_404

from src.cloud.models import UserFiles
from src.cloud.permisions import IsOwnerOrAdmin
from src.cloud.serializers import UserFilesSerializer

logger = logging.getLogger("main")

# Create your views here.

class FileViewSet(viewsets.ModelViewSet):
    queryset = UserFiles.objects.all()
    serializer_class = UserFilesSerializer
    permission_classes = [IsOwnerOrAdmin]

    def perform_create(self, serializer):
        file = self.request.FILES['file']
        comment = self.request.POST.get('comment', None)
        rename = self.request.POST.get('rename', None)
        filename = rename if rename else file.name
        logger.info(f"Загрузка файла. Имя файла: {file.name}, переименование: {rename}, коммент: {comment}")
        serializer.save(name=filename, size=file.size, owner=self.request.user, comment=comment)

    def perform_destroy(self, instance):
        logger.info(f"Удаление файла {instance.name}")
        super().perform_destroy(instance)

    def get_queryset(self):
        user = self.request.user
        requested_user_id = self.request.query_params.get('id', None)
        if requested_user_id:
            return UserFiles.objects.filter(owner=requested_user_id).order_by('id')
        return UserFiles.objects.filter(owner=user).order_by('id')

    def get_object(self):
        pk = self.kwargs.get('pk')
        obj = get_object_or_404(UserFiles, pk=pk)
        self.check_object_permissions(self.request, obj)
        return obj

    def perform_update(self, serializer):
        name = self.request.data.get('name', None)
        args = {}
        logger.info(f"Редактирование файла. {self.request.data}")
        if name:
            args['name'] = name
        serializer.save(**args)

    def retrieve(self, request, *args, **kwargs):
        obj = self.get_object()
        file_type = mimetypes.guess_type(obj.name)[0]
        content_type = file_type if file_type else "application/octet-stream"
        response = FileResponse(obj.file.file, as_attachment=True, content_type=content_type, filename =obj.name )
        logger.info(f"Скачивание файла по кнопке. name = {obj.name} ,file_type = {content_type} ")
        obj.last_download = now()
        obj.save()

        return response
