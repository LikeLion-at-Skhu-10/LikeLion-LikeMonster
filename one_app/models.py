from django.db import models
from django.core.exceptions import ValidationError
from userapp.models import CustomUser

class Post(models.Model):
    title = models.CharField(max_length=20)
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='post_author')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to='images/', blank=True)
    # 좋아요 기능
    post_like = models.ManyToManyField(CustomUser,related_name='like_users', blank =True)
    like_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title

    def clean(self):
        title = self.title
        content = self.content
        if title == "" or content == "":
            raise ValidationError("글을 작성해주세요")
        return super(Post,self).clean()

class Comment(models.Model):
    def __str__(self):
        return self.content

    post_id = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='cmt')
    content = models.CharField(max_length=100)
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='cmt_author')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
