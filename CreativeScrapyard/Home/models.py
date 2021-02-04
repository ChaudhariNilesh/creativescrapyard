from django.db import models

# Create your models here.
class Query(models.Model):
    query_id = models.PositiveIntegerField(primary_key=True)
    name = models.CharField(max_length=200)
    email = models.EmailField(max_length=256, null=False)
    query_subject = models.CharField(max_length=50, null=False)
    query_message = models.CharField(max_length=500, null=False)
    query_status = models.CharField(max_length=80)
    query_date = models.DateTimeField(auto_now_add=True, null=False, blank=False)

    def __str__(self):
        return self.email