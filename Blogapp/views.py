from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Post
from .models import Comment
from .models import Profile
from django.contrib.auth.decorators import login_required, user_passes_test

def home(request):
    posts = Post.objects.filter(is_approved=True).order_by('-created_at')
    return render(request, 'blog/home.html', {'posts': posts})

def signup_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')
            return redirect('signup')
        user = User.objects.create_user(username=username, email=email, password=password)
        messages.success(request, 'Account created successfully. Please login.')
        return redirect('login')
    return render(request, 'blog/signup.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            if user.is_superuser:
                return redirect('admin_dashboard')
            else:
                return redirect('user_dashboard')
        else:
            messages.error(request, 'Invalid credentials.')
    return render(request, 'blog/login.html')

def logout_view(request):
    logout(request)
    return redirect('home')

@login_required
def user_dashboard(request):
    posts = Post.objects.filter(author=request.user)
    total_posts = posts.count()
    approved_posts = posts.filter(is_approved=True).count()
    pending_posts = total_posts - approved_posts
    total_likes = sum(post.likes.count() for post in posts)
    latest_post = posts.filter(is_approved=True).order_by('-created_at').first()

    context = {
        'posts': posts,
        'total_posts': total_posts,
        'approved_posts': approved_posts,
        'pending_posts': pending_posts,
        'latest_post': latest_post,
        'total_likes': total_likes,
    }
    return render(request, 'blog/user_dashboard.html', context)

@login_required
def admin_dashboard(request):
    if not request.user.is_superuser:
        return redirect('user_dashboard')
    posts = Post.objects.all()
    users = User.objects.all()
    pending_posts = Post.objects.filter(is_approved=False).count()
    approved_posts = Post.objects.filter(is_approved=True).count()
    pending_count = Post.objects.filter(is_approved=False).count()
    return render(request, 'blog/admin_dashboard.html', {
        'posts': posts,
        'users': users,
        'pending_count': pending_count,
        'pending_posts': pending_posts,
        'approved_posts': approved_posts,
    })


@login_required
def add_post(request):
    if request.method == 'POST':
        title = request.POST['title']
        content = request.POST['content']
        image = request.FILES.get('image')
        Post.objects.create(author=request.user, title=title, content=content, image=image)
        messages.success(request, 'Post submitted for approval.')
        return redirect('user_dashboard')
    return render(request, 'blog/add_post.html')


@login_required
def edit_post(request, post_id):
    post = get_object_or_404(Post, id=post_id, author=request.user)
    if request.method == 'POST':
        post.title = request.POST['title']
        post.content = request.POST['content']
        if 'image' in request.FILES:
            post.image = request.FILES['image']
        post.save()
        messages.success(request, 'Post updated successfully.')
        return redirect('user_dashboard')
    return render(request, 'blog/edit_post.html', {'post': post})

@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id, author=request.user)
    if request.method == 'POST':
        post.delete()
        messages.success(request, 'Post deleted.')
        return redirect('user_dashboard')
    return render(request, 'blog/delete_post.html', {'post': post})

@login_required
def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id, is_approved=True)
    post.views += 1
    post.save()
    return render(request, 'blog/post_detail.html', {'post': post})

@login_required
def profile_view(request):
    user = request.user
    profile, created = Profile.objects.get_or_create(user=user)
    posts = Post.objects.filter(author=user)
    total_posts = posts.count()
    total_likes = sum(post.likes.count() for post in posts)
    total_comments = Comment.objects.filter(post__author=user).count()

    context = {
        'user': user,
        'profile': profile,
        'total_posts': total_posts,
        'total_likes': total_likes,
        'total_comments': total_comments,
    }
    return render(request, 'blog/profile.html', context)


@login_required
def edit_profile(request):
    user = request.user
    profile, created = Profile.objects.get_or_create(user=user)

    if request.method == 'POST':
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        profile.gender = request.POST.get('gender')
        profile.mobile_no = request.POST.get('mobile_no')

        if 'profile_image' in request.FILES:
            profile.profile_image = request.FILES['profile_image']

        user.save()
        profile.save()
        messages.success(request, "✅ Profile updated successfully!")
        return redirect('profile')

    return render(request, 'blog/edit_profile.html', {'user': user, 'profile': profile})

def is_admin(user):
    return user.is_staff or user.is_superuser

@login_required
@user_passes_test(is_admin)
def approve_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    post.is_approved = True
    post.save()
    messages.success(request, f"✅ '{post.title}' has been approved successfully.")
    return redirect('admin_dashboard')

@login_required
def like_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.user in post.likes.all():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)
    return redirect('post_detail', post_id=post.id)

@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == 'POST':
        content = request.POST.get('content')
        Comment.objects.create(post=post, user=request.user, content=content)
    return redirect('post_detail', post_id=post.id)

@login_required
def toggle_visibility(request, post_id):
    post = get_object_or_404(Post, id=post_id, author=request.user)
    post.is_public = not post.is_public
    post.save()
    return redirect('user_dashboard')

@login_required
def view_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    post.views += 1
    post.save()
    comments = post.comments.all() if hasattr(post, 'comments') else []

    return render(request, 'blog/post_detail.html', {
        'post': post,
        'comments': comments
    })