from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse


class Status(models.Model):
    name = models.CharField(max_length=128)
    description = models.TextField()

    def __str__(self):
        return self.name

class Issue(models.Model):
        title = models.CharField(max_length=128)
        summary = models.CharField(max_length=256)
        description = models.TextField()
        author = models.ForeignKey(
            get_user_model(),
            on_delete = models.CASCADE
        )
        assignee = models.ForeignKey(
            get_user_model(),
            on_delete = models.CASCADE,
            null=True, blank=True,
            related_name ="assignee"
        )
        created_on = models.DateTimeField(auto_now_add=True)
        is_active = models.BooleanField(default=True)
        status = models.ForeignKey(
            Status,
            on_delete=models.CASCADE
        )

        def __str__(self):
            return self.title

        def get_absolute_url(self):
            return reverse("issue_detail", args=[self.id])



