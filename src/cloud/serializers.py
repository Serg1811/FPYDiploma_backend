from .models import CloudUser, UserFiles
from djoser.serializers import UserCreateSerializer
from rest_framework import serializers


class UserSerializer(UserCreateSerializer):
    class Meta:
        model = CloudUser
        fields = ['id', 'username', 'email', 'is_staff', 'is_active', 'date_joined','last_login']
        read_only_fields = ('username', 'id')
        
    def get_files_count(self, obj):
        return UserFiles.objects.filter(owner=obj).count()

    def get_files_size(self, obj):
        size = UserFiles.objects.filter(owner=obj).aggregate(sum=Sum('size')).get('sum')
        return size if size else 0
        
class UserFilesSerializer(serializers.ModelSerializer):
    
    creator = UserSerializer(
        read_only=True,
    )

    class Meta:
        model = UserFiles
        fields = '__all__'
        read_only_fields = ['id', 'owner', 'name', 'uploaded_at', 'last_download', 'uuid', 'size', 'file_download_url']
