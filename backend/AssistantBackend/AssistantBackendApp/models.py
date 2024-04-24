from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from django.utils import timezone


class RequestHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_requested = models.DateTimeField(default=timezone.now)
    # date_requested = models.DateTimeField(default=timezone.now().astimezone(pytz.timezone('Asia/Shanghai')))
    url = models.CharField(max_length=1000)
    text = models.CharField(max_length=200, default="")


class Dashboards(models.Model):
    table_name = models.CharField(max_length=200)
    url = models.CharField(max_length=200)
    


class Filters(models.Model):
    filter_name = models.CharField(max_length=200)
    fk_dashboard = models.ForeignKey(Dashboards, on_delete=models.CASCADE)
    id_native_filter = models.CharField(max_length=100)


class FilterValues(models.Model):
    fk_filter = models.ForeignKey(Filters, on_delete=models.CASCADE)
    filter_value = models.CharField(max_length=200)
