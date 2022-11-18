from django.shortcuts import render,redirect, get_object_or_404
from .forms import PostForm, PostEditForm, CommentForm
from .models import Post, Comment
from django.utils import timezone
from userapp.decorators import *

# Create your views here.
def main(request):
    return render(request, 'main.html')

@login_message_required
def write(request):
    if request.method == 'POST':
        write_form = PostForm(request.POST, request.FILES)
        if write_form.is_valid():
            write_form = write_form.save(commit=False)
            write_form.author = request.user
            write_form.created_at = timezone.now()
            write_form.save()
            return redirect('detail', write_form.id)
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
    if request.method == 'POST':
        cmt_form = CommentForm(request.POST)
        if cmt_form.is_valid():
            comment = cmt_form.save(commit=False)
            comment.post_id = post
            comment.author = request.user
            comment.content = cmt_form.cleaned_data['content']
            comment.save()
            return redirect('detail', post.id)
    else:
        cmt_form = CommentForm()
        cmts = Comment.objects.filter(post_id=id)
        return render(request, 'detail.html', {'post':post, 'cmt_form':cmt_form, 'cmts':cmts})

def edit(request, id):
    post = get_object_or_404(Post, id=id)
    if request.method == "POST":
        edit_form = PostEditForm(request.POST, request.FILES, instance = post)
        if edit_form.is_valid():
            post = edit_form.save(commit = False)
            post.updated_at = timezone.now()
            post.save()
            return redirect('detail', id)
    else:
        edit_form = PostEditForm(instance = post)
        url = post.image.url
        return render(request, 'edit.html', {'edit_form': edit_form, 'url': url})

def delete(request, id):
    post = get_object_or_404(Post, id = id)
    post.delete()
    return redirect('read')

def cmt_edit(request, post_id, cmt_id):
    post = get_object_or_404(Post, id=post_id)
    comment = get_object_or_404(Comment, id=cmt_id)
    form = CommentForm(instance=comment)
    if request.method == 'POST':
        edit_form = CommentForm(request.POST, instance=comment)
        if edit_form.is_valid():
            edit_form.save()
            return redirect('detail', post_id)
    return render(request, 'cmt_edit.html', {'form':form, 'post':post, 'comment':comment})

def cmt_delete(request, id):
    comment = get_object_or_404(Comment, id=id)
    comment.delete()
    return redirect('detail', comment.post_id.id)

def likes(request, id):
    like_b = get_object_or_404(Post, id = id)
    if request.user in like_b.post_like.all():
        like_b.post_like.remove(request.user)
        like_b.like_count -= 1
        like_b.save()
    else:
        like_b.post_like.add(request.user)
        like_b.like_count += 1
        like_b.save()
    return redirect('detail', like_b.id)