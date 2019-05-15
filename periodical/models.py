from django.db import models
from django.contrib.auth.models import User
# Create your models here.
# 期刊
class Periodical(models.Model):
    Name = models.CharField(max_length = 20)
    # 年,卷,期,周期
    Year = models.IntegerField()
    Volume = models.IntegerField()
    Phase = models.IntegerField()
    Cycle = models.IntegerField()
    # 邮发代号,CN刊号,ISSN
    Postal = models.CharField(max_length = 20)
    CN = models.CharField(max_length = 20)
    ISSN = models.CharField(max_length = 20)
    # 出版地,库存,总数
    Locus = models.CharField(max_length = 20)
    Reserve = models.IntegerField()
    Total = models.IntegerField()
    # 状态（是否订购）,征订人,征订日期
    Status = models.BooleanField()
    Responsibler = models.ForeignKey(User,on_delete=models.DO_NOTHING)
    Order_Time = models.DateTimeField(auto_now_add=True)
    class Meta:
        verbose_name = '期刊信息'
        verbose_name_plural = verbose_name
    def __str__(self):
        return self.Name

# 论文
class Paper(models.Model):
    Title = models.CharField(max_length = 20)
    Auther = models.CharField(max_length = 20)
    KeyWords = models.CharField(max_length = 20)
    Pages_Start = models.IntegerField()
    Pages_End = models.IntegerField()
    Abstract = models.TextField()
    # 属于哪个期刊
    Belong = models.ForeignKey(Periodical,on_delete=models.DO_NOTHING)
    class Meta:
        verbose_name = '论文信息'
        verbose_name_plural = verbose_name
    def __str__(self):
        return self.Title

# 借阅
class Borrow(models.Model):
    Person = models.ForeignKey(User,on_delete=models.DO_NOTHING)
    Period = models.ForeignKey(Periodical,on_delete=models.DO_NOTHING)
    Borrow_Time = models.DateTimeField(auto_now_add=True)
    Borrow_Duration = models.IntegerField()
    Return_Time = models.DateTimeField(auto_now=True)
    class Meta:
        verbose_name = '借阅信息'
        verbose_name_plural = verbose_name
