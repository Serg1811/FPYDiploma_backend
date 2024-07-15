import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import pre_delete
from django.dispatch import receiver

class CloudUser(AbstractUser):

    pass
    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.email
    
# Директория сохранения файлов и аватаров
def user_directory_path(instance, filename):
    return f'upload_files/{instance.user.id}/{filename}'

class UserFiles(models.Model):
    file = models.FileField(upload_to=user_directory_path)
    name = models.CharField(max_length=250)
    comment = models.CharField(max_length=256, blank=True, null=True)
    user = models.ForeignKey(CloudUser, on_delete=models.CASCADE, related_name='files')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    last_download = models.DateTimeField(blank=True, null=True)
    uuid = models.UUIDField(default=uuid.uuid4)
    type = models.CharField(max_length=50,blank=True, null=True)
    size = models.BigIntegerField()
    
    
@receiver(pre_delete, sender=UserFiles)
def file_model_delete(sender, instance, **kwargs):
    if instance.file.name:
        instance.file.delete(False)
