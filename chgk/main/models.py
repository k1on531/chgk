from django.db import models


class Questions(models.Model):
    question = models.TextField()
    answer = models.TextField()
    comment = models.TextField()
    source = models.TextField()
    author = models.TextField()
