from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, Http404
from .forms import *
from .models import *
from django.core.paginator import Paginator
from django.views.decorators.http import require_POST
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


# Create your views here.
def home(request):
    return render(request, 'Home/home_page.html')


def book_list(request):
    books = Literature.published.filter(type="bk")
    paginator = Paginator(books, 3)
    page_number = request.GET.get('page', 1)
    print(request.GET)
    books = paginator.page(page_number)
    context = {
        'books': books,
    }

    return render(request, 'Home/book_list.html', context)


def journal_list(request):
    journals = Literature.published.filter(type="jn")
    paginator = Paginator(journals, 3)
    page_number = request.GET.get('page', 1)
    print(request.GET)
    journals = paginator.page(page_number)
    context = {
        'journals': journals,
    }

    return render(request, 'Home/journal_list.html', context)


def article_list(request):
    articles = Literature.published.filter(type="ar")
    paginator = Paginator(articles, 3)
    page_number = request.GET.get('page', 1)
    print(request.GET)
    articles = paginator.page(page_number)
    context = {
        'articles': articles,
    }

    return render(request, 'Home/article_list.html', context)


def pots_list(request):
    posts = Literature.published.all()
    paginator = Paginator(posts, 3)
    page_number = request.GET.get('page', 1)
    print(request.GET)
    posts = paginator.page(page_number)
    context = {
        'posts': posts,
    }

    return render(request, 'Home/post_list.html', context)


def post_detail(request, id):
    post = get_object_or_404(Literature, id=id, status=Literature.Status.PUBLISHED)
    comments = post.comment.filter(active=True)
    form = CommentForm()
    context = {
        'post': post,
        'form': form,
        'comments': comments
    }
    return render(request, 'Home/detail_post.html', context)


def author_list(request):
    authors = Authors.published.all()
    paginator = Paginator(authors, 3)
    page_number = request.GET.get('page', 1)
    print(request.GET)
    authors = paginator.page(page_number)
    context = {
        'authors': authors,
    }
    return render(request, "Home/author_list.html", context)


def author_detail(request, id):
    author = get_object_or_404(Authors, id=id, status=Authors.Status.PUBLISHED)

    context = {
        'author': author,
    }

    return render(request, "Home/author_detail.html", context)


def ticket(request):
    if request.method == 'POST':
        form = TicketForm(request.POST)
        if form.is_valid():
            ticket_obj = Ticket.objects.create()
            cd = form.cleaned_data
            ticket_obj.massage = cd['massage']
            ticket_obj.name = cd['name']
            ticket_obj.email = cd['email']
            ticket_obj.phone = cd['phone']
            ticket_obj.subject = cd['subject']
            ticket_obj.save()
            return redirect("Home:home")

    else:
        form = TicketForm()
    return render(request, "forms/ticket.html", {"form": form})


@require_POST
# @login_required
def post_comment(request, post_id):
    post = get_object_or_404(Literature, id=post_id, status=Literature.Status.PUBLISHED)
    comment = None
    form = CommentForm(data=request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.save()

    context = {
        'post': post,
        'form': form,
        'comment': comment
    }

    return render(request, "forms/comment.html", context)


def log_out(request):
    logout(request)
    return redirect(request.META.get('HTTP_REFERER'))


def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])
            user.save()
            Account.objects.create(user=user)
            return render(request, 'forms/register_done.html', {'user': user})
    else:
        form = UserRegisterForm()
    return render(request, 'forms/register.html', {'form': form})


# @login_required
# def profile(request):
#     user = request.user
#     return render(request, "Home/profile.html", context={'user': user})


@login_required
def edit_profile(request):
    if request.method == "POST":
        user_form = EditUserForm(request.POST, instance=request.user)
        account_form = EditAccountForm(request.POST, instance=request.user.account, files=request.FILES)
        if account_form.is_valid() and user_form.is_valid():
            account_form.save()
            user_form.save()
    else:
        user_form = EditUserForm(instance=request.user)
        account_form = EditAccountForm(instance=request.user.account)

    context = {
        'user_form': user_form,
        'account_form': account_form,
    }
    return render(request, "Home/profile.html", context)
