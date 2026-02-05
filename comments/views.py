from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Prefetch
from posts.models import Post
from comments.models import Comment
from .forms import CommentForm

# Create your views here.

@login_required
def create_comment(request, post_id):

    post = get_object_or_404(Post, id=post_id)

    user_id = request.user.id

    return_url = request.session.get('previous_url',  '/posts')

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post_id = post_id
            comment.user_id = user_id
            comment.save()
            messages.success(request, "Comment created successfully.")
            return redirect(return_url)
    else:
        form = CommentForm()


    context = {
        'form': form,
        'post': post,
        'return_url': return_url,
        'action': 'Add',
    }

    return render(request, 'create_comment.html', context)

@login_required
def edit_comment(request, comment_id):

    comment = get_object_or_404(Comment, id=comment_id, user_id=request.user.id)

    return_url = request.session.get('previous_url',  '/posts')

    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            messages.success(request, "Comment updated successfully.")
            return redirect(return_url)
    else:
        form = CommentForm(instance=comment)

    context = {
        'form': form,
        'comment': comment,
        'post': comment.post,
        'return_url': return_url,
        'action': 'Update',
    }

    return render(request, 'edit_comment.html', context)

@login_required
def delete_comment(request, comment_id):

    comment = get_object_or_404(Comment, id=comment_id)

    return_url = request.session.get('previous_url',  '/posts')

    if comment.user_id != request.user.id and comment.post.user_id != request.user.id:
        messages.error(request, "You don't have permission to delete this comment.")
        return redirect(return_url)

    comment.delete()
    messages.success(request, "Comment deleted successfully.")

    return redirect(return_url)