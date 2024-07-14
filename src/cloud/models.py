import uuid
from django.db import models
from django.contrib.auth.models import User

class CloudUser(User):
    
    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.email

class UserFiles(models.Model):
    file = models.FileField(upload_to='upload_files')
    owner = models.ForeignKey(CloudUser, on_delete=models.CASCADE)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    last_download = models.DateTimeField()
    uuid = models.UUIDField(default=uuid.uuid4)
    size = models.BigIntegerField()
