from django.db.models import Sum
from .models import CloudUser, UserFiles
from djoser.serializers import UserSerializer
from rest_framework import serializers
from rest_framework.reverse import reverse

class CouldUserSerializer(UserSerializer):
    
    files_count = serializers.SerializerMethodField()
    files_size = serializers.SerializerMethodField()
    class Meta:
        model = CloudUser
        fields = ['id', 'username', 'email', 'is_staff',  'first_name', 'is_active', 'date_joined', 'is_staff', 'files_count', 'files_size']
        read_only_fields = ('username', 'id', 'is_staff')
        
    def get_files_count(self, obj):
        return UserFiles.objects.filter(user=obj).count()

    def get_files_size(self, obj):
        size = UserFiles.objects.filter(user=obj).aggregate(sum=Sum('size')).get('sum')
        return size if size else 0
        
        
class CouldUserDeleteSerializer(serializers.Serializer):
    """
    Для настройки djoser в settings.py. Теперь djoser при удалении user по id не требует пароль от этого user.
    """
    pass

class UserFilesSerializer(serializers.ModelSerializer):
    file_download_url = serializers.SerializerMethodField()

    class Meta:
        model = UserFiles
        fields = '__all__'

        read_only_fields = [
            'id',
            'user',
            'file',
            'uploaded_at',
            'last_download',
            'uuid',
            'type',
            'size',
            'file_download_url',
        ]

    def get_file_download_url(self, obj):
        return self.context['request'].build_absolute_uri(reverse('share', args=[str(obj.uuid)]))
