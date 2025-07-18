from django.db import models


class NewManager(models.Manager):
    def get_by_status(self,status) :
        return self.get_queryset().filter(status=status)

