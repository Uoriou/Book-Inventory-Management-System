from django.db import models

# Create your models here.
#Its like db 
class Books(models.Model):
    name = models.CharField(max_length=100)
    title = models.CharField(max_length=100,null=True)
    price = models.DecimalField(max_digits=12, decimal_places=2,null=True)
    
    def __str__(self):
        return self.name
