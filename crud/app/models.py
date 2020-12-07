from django.db import models

# Create your models here.

class CrudExample(models.Model):
	field1 = models.CharField(max_length=255)
	field2 = models.CharField(max_length=255)
	field3 = models.CharField(max_length=255)
	createTime = models.DateTimeField(auto_now_add=True)
	updateTime = models.DateTimeField(auto_now=True)