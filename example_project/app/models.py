from django.db import models

class ExampleDotCom(models.Model):
    link = models.CharField(max_length=255)

    def __str__(self):
        return self.link
