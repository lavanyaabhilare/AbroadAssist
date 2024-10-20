from django.db import models

class user_otp(models.Model):
    id = models.AutoField
    username = models.TextField(max_length=100,blank=False)
    email = models.EmailField(max_length=50,unique=True,blank=False)
    password = models.TextField(max_length=40,blank=False)
    gen_otp = models.IntegerField()
