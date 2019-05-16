from django.contrib import admin
from .models import Periodical,Paper
# Register your models here.
@admin.register(Periodical)
class PeriodicalAdmin(admin.ModelAdmin):
    list_display = ('id','Name','Year','Volume','Cycle','Locus','Reserve','Total','Status','Responsibler','Order_Time')

@admin.register(Paper)
class PaperAdmin(admin.ModelAdmin):
    list_display = ('id','Title','Auther','KeyWords','Pages_Start','Pages_End','Abstract','Belong')