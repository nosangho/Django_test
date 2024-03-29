from django.shortcuts import render, redirect
from .models import Post, Category, Tag
from django.views.generic import ListView, DetailView, UpdateView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import CommentForm

class Postlist(ListView):
    model = Post

    def get_queryset(self):
        return Post.objects.order_by('-created')
    
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(Postlist, self).get_context_data(**kwargs)
        context['category_list'] = Category.objects.all()
        context['post_without_category'] = Post.objects.filter(category=None).count()

        return context
    
class PostDetail(DetailView):
    model = Post

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(PostDetail, self).get_context_data(**kwargs)
        context['category_list'] = Category.objects.all()
        context['post_without_category'] = Post.objects.filter(category=None).count()
        context['comment_form'] = CommentForm()

        return context

class PostCreate(LoginRequiredMixin, CreateView):
    model = Post
    fields = [
        'title', 'content', 'image', 'category', 'tags'
    ]

    def form_valid(self, form):
        current_user = self.request.user
        if current_user.is_authenticated:
            form.instance.author = current_user
            return super(type(self), self).form_valid(form)
        else:
            return redirect('/blog/')


class PostUpdate(UpdateView):
    model = Post
    fields = [
        'title', 'content', 'image', 'category', 'tags'
    ]

class PostListByTag(ListView):
    
    def get_queryset(self):
        tag_slug = self.kwargs['slug']
        tag = Tag.objects.get(slug=tag_slug)
        return tag.post_set.order_by('-created')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(type(self), self).get_context_data(**kwargs)
        context['category_list'] = Category.objects.all()
        context['post_without_category'] = Post.objects.filter(category=None).count()
        tag_slug = self.kwargs['slug']
        context['tag'] = Tag.objects.get(slug=tag_slug)
        return context



class PostListByCategory(ListView):

    def get_queryset(self):
        slug = self.kwargs['slug']

        if slug == '_none':
            category = None
        else:
            category = Category.objects.get(slug=slug)
        
        return Post.objects.filter(category=category).order_by('-created')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(type(self), self).get_context_data(**kwargs)
        context['category_list'] = Category.objects.all()
        context['post_without_category'] = Post.objects.filter(category=None).count()
        
        slug = self.kwargs['slug']
        if slug == '_none':
            context['category'] = '미분류'
        else:
            category = Category.objects.get(slug=slug)
            context['category'] = category

        #context['title'] = 'Blog - {}'.format(category.name)
        return context

def new_comment(request, pk):
    post = Post.objects.get(pk=pk)
    
    if request.method == "POST":
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            return redirect(comment.get_absolute_url())
    else:
        return redirect('/blog/')