from django.shortcuts import render, HttpResponse, redirect, get_object_or_404, reverse
from .forms import ArticleForm
from django.contrib import messages
from .models import Article, Comment
from django.contrib.auth.decorators import login_required

# Create your views here.


def articles(request):
    keyword = request.GET.get("keyword")

    if keyword:
        articles = Article.objects.filter(title__contains=keyword)
        return render(request, "articles.html", {"articles": articles})
    articles = Article.objects.all()
    return render(request, "articles.html", {"articles": articles})


def index(request):
    '''Returns the template for the main page'''
    context = {
        "number1": 10,
        "number2": [1, 2, 3, 4, 5]
    }
    return render(request, "index.html", context)


def about(request):
    return render(request, "about.html")


@login_required(login_url="user:login")
def dashboard(request):
    articles = Article.objects.filter(author=request.user)
    context = {
        "articles": articles
    }
    return render(request, "dashboard.html", context)


@login_required(login_url="user:login")
def addArticle(request):
    form = ArticleForm(request.POST or None, request.FILES or None)

    if form.is_valid():
        article = form.save(commit=False)
        # form.save() creates an article object and does article.save().
        # A username must be provided as well otherwise:
        # 'NOT NULL constraint failed: article_article.author_id'
        article.author = request.user
        article.save()
        messages.success(request, "Article added successfully!")
        return redirect("index")

    return render(request, "addarticle.html", {"form": form})


def detail(request, id):
    # article = Article.objects.filter(id=id).first()
    article = get_object_or_404(Article, id=id)
    comments = article.comments.all()
    return render(request, "detail.html", {"article": article, "comments":comments})


@login_required(login_url="user:login")
def updateArticle(request, id):
    article = get_object_or_404(Article, id=id)
    form = ArticleForm(request.POST or None, request.FILES or None, instance=article)
    
    if form.is_valid():
        article = form.save(commit=False)
        article.author = request.user
        article.save()
        messages.success(request, "Article updated successfully!")
        return redirect("index")
    
    if request.POST.get("title") and not request.POST.get("content"):
        messages.info(request, "Content can't be empty!")
        form = ArticleForm(instance=article)
        return render(request, "update.html", {"form": form})
    
    # If form is not valid or the request is "GET"
    return render(request, "update.html", {"form": form})


@login_required(login_url="user:login")
def deleteArticle(request, id):
    article = get_object_or_404(Article, id=id)
    article.delete()
    messages.success(request, "Article deleted successfully!")
    # Redirect to the url under the app 'Article'
    return redirect("article:dashboard")


def addComment(request, id):
    article = get_object_or_404(Article, id=id)

    if request.method == "POST":
        comment_author = request.POST.get("comment_author")
        comment_content = request.POST.get("comment_content")

        newComment = Comment(comment_author=comment_author, comment_content=comment_content)

        newComment.article = article

        newComment.save()

    return redirect(reverse("article:detail", kwargs={"id":id}))
