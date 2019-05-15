from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    nickname = models.CharField(max_length=20)
    GENDER_CHOICE = (
          (u'M', u'Male'),
          (u'F', u'Female'),
      )
    gender = models.CharField(null=True,max_length=2,choices=GENDER_CHOICE,default='')
    def __str__(self):
        return '<Profile: %s for %s>' % (self.nickname,self.user.username)