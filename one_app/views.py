from django.shortcuts import render,redirect, get_object_or_404
from .forms import PostForm, PostEditForm, CommentForm, HashtagForm
from .models import Post, Comment, Hashtag
from django.utils import timezone
from django.db.models import Q
from userapp.decorators import *

# Create your views here.
def main(request):
    return render(request, 'main.html')

@login_message_required
def write(request, post = None):
    if request.method == 'POST':
        write_form = PostForm(request.POST, request.FILES, instance=post)
        if write_form.is_valid():
            post = write_form.save(commit=False)
            post.author = request.user
            post.created_at = timezone.now()
            post.save()
            write_form.save_m2m()
            return redirect('detail', post.id)
        else:
            context = {
                'write_form':write_form,
            }
            return render(request, 'write.html', context)
    else:
        write_form = PostForm(instance=post)
        write_form = PostForm (instance = post)
        return render(request, 'write.html', {'write_form':write_form})

def read(request):
    read_forms = Post.objects.all()

    sort = request.GET.get('sort','')
    if sort == 'date':
        read_forms = Post.objects.all().order_by('-created_at')
    elif sort == 'like':
        read_forms = Post.objects.all().order_by('-like_count')

    q = request.GET.get('q', '')
    if q:
        read_forms = read_forms.filter(Q(hashtag__hashtag_content__icontains=q))
    return render(request, 'read.html', {'read_forms':read_forms, 'q': q})

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

def edit(request, id, post = None):
    post = get_object_or_404(Post, id=id)
    if request.method == "POST":
        edit_form = PostEditForm(request.POST, request.FILES, instance = post)
        if edit_form.is_valid():
            post = edit_form.save(commit = False)
            post.updated_at = timezone.now()
            post.save()
            edit_form.save_m2m()
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

@login_message_required
def likes(request, id):
    post = get_object_or_404(Post, id = id)
    if request.user in post.like.all():
        post.like.remove(request.user)
        post.like_count -= 1
        post.save()
    else:
        post.like.add(request.user)
        post.like_count += 1
        post.save()
    return redirect('/detail/' + str(id))

def hashtag(request, hashtag = None):
    if request.method == 'POST':
        form = HashtagForm(request.POST, instance = hashtag)
        if form.is_valid():
            hashtag = form.save(commit = False)
            if Hashtag.objects.filter(hashtag_content = form.cleaned_data['hashtag_content']):
                form = HashtagForm()
                error_message = "이미 존재하는 해시태그입니다."
                return render(request, 'hashtag.html', {'form': form, "error_message": error_message})
            else:
                hashtag.hashtag_content = form.cleaned_data['hashtag_content']
                hashtag.save()
            return redirect('read')
    else:
        form = HashtagForm(instance = hashtag)
        tags = Hashtag.objects.all()
        return render(request, 'hashtag.html', {'form': form, 'tags':tags})

def search(request):
    posts = Post.objects.all()
    search = request.GET.get('search', '')
    if search:
        posts = posts.filter(
            Q(title__icontains = search)|Q(content__icontains = search)
        ).distinct()
        return render(request, 'search.html', {'posts':posts, 'search':search})
    else:
        return render(request, 'search.html')