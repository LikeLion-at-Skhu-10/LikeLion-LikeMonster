from django import forms
from .models import Post, Comment, Hashtag
 
class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title','content','image','hashtags']

    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        self.fields['title'].required = False

class PostEditForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title','content','image','hashtags']

    def __init__(self, *args, **kwargs):
        super(PostEditForm, self).__init__(*args, **kwargs)
        self.fields['title'].required = False
        
        instance = getattr(self, 'instance', None)
        if instance and instance.pk:
            self.fields['content'].widget.attrs['readonly'] = True

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']

class HashtagForm(forms.ModelForm):
    class Meta:
        model = Hashtag 
        fields = ['name']