from django.db import models


class UserRegistrationModel(models.Model):

    name = models.CharField(max_length=100)

    loginid = models.CharField(max_length=100, unique=True)

    password = models.CharField(max_length=100)

    mobile = models.CharField(max_length=100, unique=True)

    email = models.CharField(max_length=100, unique=True)

    locality = models.CharField(max_length=100)

    address = models.CharField(max_length=1000)

    city = models.CharField(max_length=100)

    state = models.CharField(max_length=100)

    status = models.CharField(max_length=100, default="activated")


    def __str__(self):

        return self.loginid


    class Meta:

        db_table = "UserRegistrations"