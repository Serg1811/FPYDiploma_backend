import mimetypes
import logging

from django.http import FileResponse, HttpResponse
from django.utils.timezone import now
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, generics
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.filters import SearchFilter


from src.cloud.models import UserFiles
from src.cloud.permisions import IsOwnerOrAdmin
from src.cloud.serializers import UserFilesSerializer

logger = logging.getLogger("main")

# Create your views here.

class FileViewSet(viewsets.ModelViewSet):
    queryset = UserFiles.objects.all()
    serializer_class = UserFilesSerializer
    permission_classes = [IsOwnerOrAdmin]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['user', 'name']
    search_fields = ['name', 'comment']

    def perform_create(self, serializer):
        file = self.request.FILES['file']
        filename = file.name
        user = self.request.user

        logger.info(f"Загрузка файла. Имя файла: {file.name}")
        serializer.save(file=file, name=filename, size=file.size, type=file.content_type, user=user)

    def perform_destroy(self, instance):
        logger.info(f"Удаление файла {instance.name}")
        super().perform_destroy(instance)

    def get_queryset(self):
        requested_user = self.request.user
        if requested_user.is_staff:
            return UserFiles.objects.order_by('id')
        return UserFiles.objects.filter(user=requested_user).order_by('id')


    def get_object(self):
        pk = self.kwargs.get('pk')
        obj = get_object_or_404(UserFiles, pk=pk)
        logger.info(obj)
        self.check_object_permissions(self.request, obj)
        return obj

    def perform_update(self, serializer):
        name = self.request.data.get('name', None)
        args = {}
        logger.info(f"Редактирование файла. {self.request.data}")
        if name:
            args['name'] = name
        serializer.save(**args)


    @action(detail=True, methods=['post'])
    def download(self, request, pk=None):
        logger.info(self)
        obj = self.get_object()
        file_type = mimetypes.guess_type(obj.name)[0]
        logger.info(mimetypes.guess_type(obj.name))
        response = FileResponse(obj.file, as_attachment=True)
        obj.last_download = now()
        obj.save()

        return response
        
class ShareFiles(generics.RetrieveAPIView):
    queryset = UserFiles.objects.all()
    serializer_class = UserFilesSerializer
    lookup_field = 'uuid'

    def retrieve(self, request, *args, **kwargs):
        obj = self.get_object()
        response = HttpResponse(obj.file, content_type=obj.type)
        response['Content-Disposition'] = 'inline;filename=' + obj.name
        response["Access-Control-Expose-Headers"] = "Content-Disposition"
        logger.info(f"Свободное скачивание файла по ссылке. {obj.name}")
        obj.last_download = now()
        obj.save()
        return response

