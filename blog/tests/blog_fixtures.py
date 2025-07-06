import datetime
import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from blog.models import *
from appuser.tests.appuser_fixtures import *

@pytest.fixture
def category(db):
    return Category.objects.create(
        name="Test Category",
        slug="test-category"
    )

@pytest.fixture
def tag(db):
    return Tag.objects.create(name='Test Tag', slug='test-tag')

@pytest.fixture
def post(db, app_user, category, tag):
    post = Post.objects.create(
        page_type='normal',
        slug="test-post",
        title='Test Post',
        sub_title='Test Subtitle',
        keyword='test,post',
        summary='Test summary',
        is_published=True,
        publishedAt=timezone.now(),
        content='Test content',
        author=app_user,
        category=category,
        post_media_type='no_picture',
    )
    post.tags.add(tag)
    return post

@pytest.fixture
def post_list(db, post):
    post_list = PostList.objects.create(
        title="Test Post List",
        place="blog_page"
    )
    post_list.posts.add(post)
    return post_list

@pytest.fixture
def post_media(db, post):
    image_file= SimpleUploadedFile('test.jpg', b'content')
    return PostMedia.objects.create(
        post=post,
        file=image_file,
        url="https://example.com/media/test.jpg",
        type="image"
    )

@pytest.fixture
def post_comment(db,app_user,post,category, django_user_model):
    comment = PostComment.objects.create(
        post=post,
        comment='Test comment',
        user=app_user,
        is_published=True
    )
    return comment




@pytest.fixture
def about_us(db, app_user, category, tag):
    post = Post.objects.create(
        page_type='about_us',
        slug="About-US",
        title='About US',
        sub_title='About us sub title',
        keyword='test,post',
        summary='Test summary',
        is_published=True,
        publishedAt=timezone.now(),
        content='Test content',
        author=app_user,
        category=category,
        post_media_type='no_picture',
    )
    post.tags.add(tag)
    return post

