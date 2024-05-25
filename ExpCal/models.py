from django.db import models
from VAV.models import UserDetails
from django.db import migrations


class CategoryInfo(models.Model):
    categoryId = models.AutoField(primary_key=True,null=False)
    category_name = models.CharField(max_length=255,null=False)

    def __str__(self):
        return f"{self.categoryId} - {self.category_name}"

class ExpDetails(models.Model):
    expId = models.AutoField(primary_key=True)
    userId = models.ForeignKey(UserDetails, on_delete=models.CASCADE, null=False)
    date = models.DateField(null=False)
    categoryId = models.ForeignKey(CategoryInfo, on_delete=models.CASCADE, null=False)
    additional_info = models.TextField(default="---",max_length=1000)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def save(self, *args, **kwargs):
        # If date is not provided, set it to the current date
        if not self.date:
            self.date = date.today()
        super().save(*args, **kwargs)
        
    def __str__(self):
        return f"{self.expId} - {self.userId} - {self.categoryId} - {self.amount} - {self.date}"
