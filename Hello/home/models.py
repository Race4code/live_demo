from django.db import models

# Create your models here.

class Todos(models.Model):
    id=models.AutoField(blank=False,primary_key=id)
    todo_title=models.CharField(max_length=100)
    status=models.BooleanField(default=False)
    timestamp=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.todo_title