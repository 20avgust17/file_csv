from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator
from django.db import models
from django.urls import reverse


class User(AbstractUser):
    pass

class Column(models.Model):
    class ColumnsTypeChoices(models.TextChoices):
        FULL_NAME = "Full_name"
        JOB = "Job"
        EMAIL = "Email"
        PHONE_NUMBER = "Phone_number"
        COMPANY_NAME = "Company_name"
        TEXT = "Text"
        NUMBER = "Number"
        ADDRESS = "Address"

    name = models.CharField(max_length=255)
    type = models.CharField(max_length=255, choices=ColumnsTypeChoices.choices)
    order = models.PositiveBigIntegerField(unique=True)
    start_num = models.IntegerField(default=18)
    end_num = models.IntegerField(default=60)

    def __str__(self):
        return f"Full_name: {self.name}, Type: {self.type}"


class Schema(models.Model):
    class SeparatorChoices(models.TextChoices):
        COMMA = ","
        COLON = ":"
        SEMICOLON = ";"

    class CharacterChoices(models.TextChoices):
        SINGLE_QUOTES = "'"
        DOUBLE_QUOTES = '"'

    title = models.CharField(max_length=255)
    modified = models.TimeField(auto_now=True)
    columns = models.ManyToManyField(Column, related_name="schemas")
    separator = models.CharField(
        max_length=2,
        choices=SeparatorChoices.choices,
        default=","
    )
    string_character = models.CharField(
        max_length=2,
        choices=CharacterChoices.choices,
        default='"'
    )

    def __str__(self):
        return f"Title: {self.title}, modified: {self.modified}"


class CSVData(models.Model):
    modified = models.TimeField(auto_now=True)
    schema = models.ForeignKey(Schema, on_delete=models.CASCADE)
    csv_file = models.FileField()
    rows = models.IntegerField(validators=[MinValueValidator(0)])
    status = models.BooleanField(default=False)