from django.db import models
from ckeditor.fields import RichTextField
# Create your models here.


class Article(models.Model):
    """
    Defines attributes of the Article table
    """
    author = models.ForeignKey("auth.User", on_delete=models.CASCADE,
                               verbose_name="Author")
    title = models.CharField(max_length=50, verbose_name="Title")
    content = RichTextField(verbose_name="Article Content")
    created_date = models.DateTimeField(auto_now_add=True,
                                        verbose_name="Date Created")
    article_image = models.FileField(blank=True, null=True,
                                     verbose_name="Add an Article Image")

    def __str__(self):
        return str(self.title)
    class Meta:
        ordering = ["-created_date"]


class Comment(models.Model):
    """
    Defines attributes of the Comments table
    """
    # Can make queries such as 'article.comments.all()'
    article = models.ForeignKey(Article, on_delete=models.CASCADE,
                                verbose_name="Article",
                                related_name="comments")
    comment_author = models.CharField(max_length=50, verbose_name="Name")
    comment_content = models.CharField(max_length=200, verbose_name="Comment")
    comment_date = models.DateTimeField(auto_now_add=True,
                                        verbose_name="Date Commented")

    def __str__(self):
        return str(self.comment_content)
    class Meta:
        ordering = ["-comment_date"]
