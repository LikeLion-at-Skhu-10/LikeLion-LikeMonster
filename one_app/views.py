from django.shortcuts import render,redirect, get_object_or_404
from .forms import PostForm
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
            return redirect('main')
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
    detail_form = get_object_or_404(Post, id=id)
    return render(request, 'detail.html', {'detail_form':detail_form})

def edit(request, id):
    edit = get_object_or_404(Post, id=id)
    if request.method == 'POST':
        edit_form = PostForm(request.POST, request.FILES, instance=edit_form)
        if edit_form.is_valid():
            edit_form.save(commit=False)
            edit_form.save()
            return redirect('read')
    else:
        edit_form = PostForm(instance=edit)
        image = edit.image
        return render(request, 'edit.html', {'edit_form':edit_form, 'image': image})

def delete(request, id):
    delete_form = get_object_or_404(Post, id=id)
    delete_form.delete()
    return redirect('read')