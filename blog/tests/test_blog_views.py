import pytest
from django.urls import reverse
from blog.models import Post, Category, Tag
from appuser.models import AppUser
from django.utils import timezone
from blog.forms import PostCommentForm

@pytest.mark.django_db
def test_blog_view_list(client):
    author = AppUser.objects.create(username='author', password='pass')
    category = Category.objects.create(name='TestCat', slug='testcat')
    tag = Tag.objects.create(name='TestTag', slug='testtag')
    post = Post.objects.create(
        title='Test Post',
        slug='test-post',
        summary='Summary',
        content='Content',
        is_published=True,
        page_type='normal',
        author=author,
        category=category,
        publishedAt=timezone.now(),
    )
    post.tags.add(tag)
    url = reverse('blog-view')  # Make sure your urls.py has name='blog-list-view' for BlogView
    response = client.get(url)
    assert response.status_code == 200
    assert 'posts' in response.context
    assert post in response.context['posts']
    assert 'tags' in response.context
    assert 'post_categories' in response.context
    assert 'latest_posts' in response.context
    assert 'social_media' in response.context
    assert 'page_title' in response.context

@pytest.mark.django_db
def test_blog_view_filter_by_category(client):
    author = AppUser.objects.create(username='author2', password='pass')
    category = Category.objects.create(name='Cat2', slug='cat2')
    post = Post.objects.create(
        title='Cat Post',
        slug='cat-post',
        summary='Summary',
        content='Content',
        is_published=True,
        page_type='normal',
        author=author,
        category=category,
        publishedAt=timezone.now(),
    )
    url = reverse('blog-view') + f'?category={category.slug}'
    response = client.get(url)
    assert response.status_code == 200
    assert post in response.context['posts']
    assert category.name in response.context['page_title']

@pytest.mark.django_db
def test_blog_view_filter_by_tag(client):
    author = AppUser.objects.create(username='author3', password='pass')
    category = Category.objects.create(name='Cat3', slug='cat3')
    tag = Tag.objects.create(name='Tag3', slug='tag3')
    post = Post.objects.create(
        title='Tag Post',
        slug='tag-post',
        summary='Summary',
        content='Content',
        is_published=True,
        page_type='normal',
        author=author,
        category=category,
        publishedAt=timezone.now(),
    )
    post.tags.add(tag)
    url = reverse('blog-view') + f'?tag={tag.slug}'
    response = client.get(url)
    assert response.status_code == 200
    assert post in response.context['posts']
    assert tag.name in response.context['page_title']

@pytest.mark.django_db
def test_blog_view_search(client):
    author = AppUser.objects.create(username='author4', password='pass')
    category = Category.objects.create(name='Cat4', slug='cat4')
    post = Post.objects.create(
        title='UniqueTitle',
        slug='unique-title',
        summary='Summary',
        content='Content',
        is_published=True,
        page_type='normal',
        author=author,
        category=category,
        publishedAt=timezone.now(),
    )
    url = reverse('blog-view') + '?search=UniqueTitle'
    response = client.get(url)
    assert response.status_code == 200
    assert post in response.context['posts']

@pytest.mark.django_db
def test_blog_view_pagination(client):
    author = AppUser.objects.create(username='author5', password='pass')
    category = Category.objects.create(name='Cat5', slug='cat5')
    for i in range(15):
        Post.objects.create(
            title=f'Post {i}',
            slug=f'post-{i}',
            summary='Summary',
            content='Content',
            is_published=True,
            page_type='normal',
            author=author,
            category=category,
            publishedAt=timezone.now(),
        )
    url = reverse('blog-view')
    response = client.get(url)
    assert response.status_code == 200
    assert len(response.context['posts']) == 9  # paginate_by=9
    response2 = client.get(url + '?page=2')
    assert response2.status_code == 200
    assert len(response2.context['posts']) == 6

@pytest.mark.django_db
def test_blog_detail_view_get(client):
    author = AppUser.objects.create(username='author', password='pass')
    category = Category.objects.create(name='TestCat', slug='testcat')
    tag = Tag.objects.create(name='TestTag', slug='testtag')
    post = Post.objects.create(
        title='Test Post',
        slug='test-post',
        summary='Summary',
        content='Content',
        is_published=True,
        page_type='normal',
        author=author,
        category=category,
        publishedAt=timezone.now(),
    )
    post.tags.add(tag)
    url = reverse('blog-detail-view', kwargs={'slug': post.slug})
    response = client.get(url)
    assert response.status_code == 200
    assert response.context['post'] == post
    assert 'related_posts' in response.context
    assert 'post_comments' in response.context
    assert 'tags' in response.context
    assert 'user' in response.context
    assert 'message' in response.context

@pytest.mark.django_db
def test_blog_detail_view_post_valid(client):
    author = AppUser.objects.create(username='author2', password='pass')
    category = Category.objects.create(name='TestCat2', slug='testcat2')
    post = Post.objects.create(
        title='Test Post2',
        slug='test-post2',
        summary='Summary',
        content='Content',
        is_published=True,
        page_type='normal',
        author=author,
        category=category,
        publishedAt=timezone.now(),
    )
    client.force_login(author)
    url = reverse('blog-detail-view', kwargs={'slug': post.slug})
    data = {'comment': 'A test comment'}
    response = client.post(url, data)
    assert response.status_code == 302
    assert response.url == url
    # After redirect, message should be in session
    response2 = client.get(url)
    assert 'نظر شما با موفقیت ثبت شد' in response2.context['message']
    assert post.post_comments.filter(comment='A test comment', user=author).exists()

@pytest.mark.django_db
def test_blog_detail_view_post_invalid(client):
    author = AppUser.objects.create(username='author3', password='pass')
    category = Category.objects.create(name='TestCat3', slug='testcat3')
    post = Post.objects.create(
        title='Test Post3',
        slug='test-post3',
        summary='Summary',
        content='Content',
        is_published=True,
        page_type='normal',
        author=author,
        category=category,
        publishedAt=timezone.now(),
    )
    client.force_login(author)
    url = reverse('blog-detail-view', kwargs={'slug': post.slug})
    data = {'comment': ''}  # Invalid: comment is required
    response = client.post(url, data)
    assert response.status_code == 302
    assert response.url == url
    # After redirect, error message should be in session
    response2 = client.get(url)
    assert 'comment' in str(response2.context['message'])
    assert not post.post_comments.filter(user=author).exists()
