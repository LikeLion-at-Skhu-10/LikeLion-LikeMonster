from django.db import models
from django.core.exceptions import ValidationError

class Post(models.Model):
    title = models.CharField(max_length=20)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to='images/', blank=True)

    def __str__(self):
        return self.title

    def clean(self):
        title = self.title
        content = self.content
        if title == "" or content == "":
            raise ValidationError("글을 작성해주세요")
        return super(Post,self).clean()
