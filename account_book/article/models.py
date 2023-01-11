import datetime

from django.db import models
from config.settings import AUTH_USER_MODEL, SHORT_CUT_HOLD_TIME
from django.utils import timezone


# Create your models here.


class ArticleModels(models.Model):
    writer = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE)
    use_money = models.IntegerField('사용 금액', default=0)
    content = models.TextField('메모', null=True, default=None)
    spending_date = models.DateField('사용 일자', null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = models.Manager()

    def __str__(self) -> str:
        return f"{self.spending_date} - {self.use_money}"


class ShortCutUrlModels(models.Model):
    make_user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE)
    link = models.URLField("기존 링크", max_length=255)
    new_link = models.URLField("단축 URL", default="")

    is_using = models.BooleanField('사용 가능 여부', default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = models.Manager()

    def __str__(self):
        return f"{self.link} / {self.new_link}"

    def check_is_using_time(self):
        if self.is_using:
            if (self.created_at + datetime.timedelta(days=SHORT_CUT_HOLD_TIME)) < timezone.now():
                self.is_using = False
                return False
        else:
            return True
