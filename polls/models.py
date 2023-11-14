from django.db import models
from django.utils import timezone
from phonenumber_field.modelfields import PhoneNumberField
import datetime
import uuid

class Question(models.Model):
    def __str__(self):
        return self.question_text
    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField("date published")


class Choice(models.Model):
    def __str__(self):
        return self.choice_text
    
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

class PhoneNumber(models.Model):
    def __str__(self) -> str:
        return str(self.phone_number ) + " " + str(self.UID)
    phone_number = PhoneNumberField()
    UID = models.UUIDField(default=uuid.uuid4, editable=False)