from django.db import models

class Category(models.Model):
    cat_id = models.IntegerField(primary_key=True)
    short_name = models.CharField(max_length=200)
    def __unicode__(self):
        return self.cat_id
    
