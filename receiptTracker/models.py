from django.db import models
from django.conf import settings
from django.urls import reverse

class Receipt(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    store_name = models.CharField(max_length=100)
    date_of_purchase = models.DateField()
    item_list = models.TextField()  # You can also use a many-to-many relationship to a separate Item model
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.store_name} on {self.date_of_purchase}"
    
    def get_absolute_url(self):
        return reverse('receipt-detail', kwargs={'pk': self.pk})
