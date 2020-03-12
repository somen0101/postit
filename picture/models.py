from django.db import models
from django.conf import settings
from django.utils import timezone


class Post(models.Model):
    title = models.CharField(max_length=200)
    text = models.TextField()
    upload_date = models.DateTimeField()

    def publish(self):
        self.published_date = timezone.now()

        self.save()

    def __str__(self):
        return self.title


class PostTagName(models.Model):
    name = models.CharField(max_length=200, default="")

    def __str__(self):
        return self.name


class PostTagList(models.Model):
    content = models.ForeignKey(Post, on_delete=models.CASCADE)
    tag = models.ForeignKey(PostTagName, on_delete=models.CASCADE)


class PostComment(models.Model):
    id = models.BigAutoField(
        primary_key=True,
    )
    no = models.IntegerField(
        default=0,
    )
    user_name = models.CharField(
        max_length=30,
        null=True,
        blank=False,
    )
    topic = models.ForeignKey(
        Post,
        on_delete=models.PROTECT,
    )
    message = models.TextField(
        max_length=1000, default=""
    )
    pub_flg = models.BooleanField(
        default=True,
    )
    created = models.DateTimeField(
        auto_now_add=True,
    )

    def __str__(self):
        return '{}-{}'.format(self.topic.id, self.no)




# Create your models here.
