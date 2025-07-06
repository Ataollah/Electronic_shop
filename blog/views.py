from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views.generic import DetailView, ListView
from blog.forms import PostCommentForm
from blog.models import Tag, Category, Post
from siteInfo.models import SocialMedia


# Create your views here.
class BlogView(ListView):
    model = Post
    template_name = 'blog/List/list.html'
    context_object_name = 'posts'
    paginate_by = 9

    def get_queryset(self):
        posts = Post.objects.prefetch_related('media', 'author').filter(page_type='normal', is_published=True).order_by('-publishedAt')
        category = self.request.GET.get('category')
        tag = self.request.GET.get('tag')
        search_query = self.request.GET.get('search')

        if category:
            posts = posts.filter(category__slug=category)
        if tag:
            posts = posts.filter(tags__slug=tag)
        if search_query:
            posts = posts.filter(Q(title__icontains=search_query) | Q(summary__icontains=search_query) | Q(content__icontains=search_query))

        return posts

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tags'] = Tag.objects.all()
        context['post_categories'] = Category.objects.all()
        context['latest_posts'] = Post.objects.filter(is_published=True).order_by('-createdAt')[:3]
        context['social_media'] = SocialMedia.objects.all()
        context['page_title'] = "وبلاگ"

        category = self.request.GET.get('category')
        tag = self.request.GET.get('tag')

        if category:
            context['page_title'] += " - " + Category.objects.get(slug=category).name
        if tag:
            context['page_title'] += " - " + Tag.objects.get(slug=tag).name

        return context




class BlogDetailView(DetailView):
    model = Post
    template_name = 'blog/Detail/details.html'
    context_object_name = 'post'

    def get_object(self, queryset=None):
        return get_object_or_404(Post.objects.prefetch_related('media', 'tags', 'author'), slug=self.kwargs.get('slug'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.object
        context['related_posts'] = Post.objects.filter(category=post.category).order_by('-publishedAt')[:3]
        context['post_comments'] = post.post_comments.filter(is_published=True)
        context['tags'] = post.tags.all()
        context['user'] = self.request.user
        context['message'] = self.request.session.pop('message', '')
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = PostCommentForm(request.POST)
        if  form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.post = self.object
            comment.save()
            request.session['message'] = 'نظر شما با موفقیت ثبت شد'
        else:
            request.session['message'] = form.errors
        return HttpResponseRedirect(reverse('blog-detail-view', kwargs={'slug': self.object.slug}))