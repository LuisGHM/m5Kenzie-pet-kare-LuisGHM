from django.db import models


class SexOpt(models.TextChoices):
    MALE = "Male"
    FEMALE = "Female"
    NotInformed = "Not Informed"

# Create your models here.
class Pet(models.Model):
    name = models.CharField(max_length=50)
    age = models.IntegerField()
    weight = models.FloatField()
    sex = models.CharField(max_length=20, choices=SexOpt.choices, default=SexOpt.NotInformed)
    group = models.ForeignKey("groups.Group", on_delete=models.CASCADE, related_name="pets")