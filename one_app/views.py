from django.shortcuts import render,redirect, get_object_or_404
from .forms import PostForm, EditForm
from .models import Post
from django.utils import timezone

# Create your views here.
def main(request):
    return render(request, 'main.html')

def write(request):
    if request.method == 'POST':
        write_form = PostForm(request.POST, request.FILES)
        if write_form.is_valid():
            write_form = write_form.save(commit=False)
            write_form.created_at = timezone.now()
            write_form.save()
            return redirect('detail', id)
        else:
            context = {
                'write_form':write_form,
            }
            return render(request, 'write.html', context)
    else:
        write_form = PostForm
        return render(request, 'write.html', {'write_form':write_form})

def read(request):
    read_forms = Post.objects.all()
    return render(request, 'read.html', {'read_forms':read_forms})

def detail(request, id):
    post = get_object_or_404(Post, id=id)
    return render(request, 'detail.html', {'post':post})

def edit(request, id):
    post = get_object_or_404(Post, id=id)
    if request.method == "POST":
        edit_form = EditForm(request.POST, request.FILES, instance = post)
        if edit_form.is_valid():
            post = edit_form.save(commit = False)
            post.updated_at = timezone.now()
            post.save()
            return redirect('detail', id)
    else:
        edit_form = EditForm(instance = post)
        url = post.image.url
        return render(request, 'edit.html', {'edit_form': edit_form, 'url': url})

def delete(request, id):
    post = get_object_or_404(Post, id = id)
    post.delete()
    return redirect('read')