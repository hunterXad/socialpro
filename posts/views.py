from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from .forms import *
from .models import *
from django.views.generic import DeleteView
from django.urls import reverse_lazy



class PostListView(View):
    def get(self, request):
        posts = Post.objects.order_by('-created_at')
        return render(request, 'post_list.html', {'posts': posts})

class PostDetailView(View):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login') 
        return super().dispatch(request, *args, **kwargs)
   
    def get(self, request, post_id):
        post = get_object_or_404(Post, pk=post_id)
        comments = post.comments.all().order_by('-created_at')
        comment_form = CommentForm()
        return render(request, 'post_detail.html', {'post': post, 'comments': comments, 'comment_form': comment_form})
   
    def post(self, request, post_id):
         
        post = get_object_or_404(Post, pk=post_id)
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            return redirect('post_detail', post_id=post_id)
        comments = post.comments.all()
        return render(request, 'post_detail.html', {'post': post, 'comments': comments, 'comment_form': comment_form})


class AddPostView(LoginRequiredMixin, View):
    def get(self, request):
        form = PostForm()
        return render(request, 'add_post.html', {'form': form})

    def post(self, request):
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            form.instance.author = request.user
            form.save()
            return redirect('post_list')
        return render(request, 'add_post.html', {'form': form})
    
    
    
class LikePostView(LoginRequiredMixin, View):
    def post(self, request, post_id):
        post = get_object_or_404(Post, pk=post_id)
        profile = Profile.objects.get(user=request.user)
        if profile in post.likes.all():
            post.likes.remove(profile)
            liked = False
        else:
            post.likes.add(profile)
            liked = True
        post.save()
        return JsonResponse({'likes': post.total_likes(), 'liked': liked})

    
class LikeCommentView(LoginRequiredMixin, View):
    def post(self, request, comment_id):
        comment = get_object_or_404(Comment, pk=comment_id)
        if request.user in comment.likes.all():
            comment.likes.remove(request.user)
            liked = False
        else:
            comment.likes.add(request.user)
            liked = True
        comment.save()
        return JsonResponse({'likes': comment.likes.count(), 'liked': liked})
    
class CommentDeleteView(DeleteView):
    model = Comment
    template_name = 'comment_confirm_delete.html'  
    success_url = reverse_lazy('post_list')  

    
    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(author=self.request.user)