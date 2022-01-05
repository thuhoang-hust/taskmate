from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class TaskList(models.Model):
    manage = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    # on_delete to del user1==del all task of user1
    task = models.CharField(max_length=300)
    done = models.BooleanField(default=False)

    def __str__(self):
        return self.task + ' - ' + str(self.done)
