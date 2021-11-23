from django.db import models
from django.urls import reverse
from django_pandas.managers import DataFrameManager

# Create your models here.
class Book(models.Model):
    isbn = models.CharField(max_length=50)
    title = models.CharField(max_length=250)
    author = models.CharField(max_length=50)
    year = models.IntegerField()
    publisher = models.CharField(max_length=50)
    image_s = models.CharField(max_length=250)
    image_m = models.CharField(max_length=250)
    image_l = models.CharField(max_length=250)

    objects = DataFrameManager()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('book-detail', kwargs={'pk' : self.pk})

class Rating(models.Model):
    isbn = models.ForeignKey(Book,on_delete=models.CASCADE)
    userid = models.CharField(max_length=250)
    rating = models.IntegerField()

    def __str__(self):
        return self.isbn