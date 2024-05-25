from django.db import models
#----------------------------------------------------------------------------------------------------------------------------------------------------------
class UserDetails(models.Model):
    userId = models.AutoField(primary_key=True)  # Auto-generated unique ID
    email_id = models.EmailField(max_length=200,null=False)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100,null=False)
    profile_image = models.ImageField(upload_to='profile_images/', default='profile_images/default.png')
    password = models.CharField(max_length=35,null=False)

    def __str__(self):
        return f"{self.userId} - {self.first_name} {self.last_name}"
#----------------------------------------------------------------------------------------------------------------------------------------------------------