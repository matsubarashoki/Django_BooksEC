from django.db import models
import datetime
from django.contrib.auth import get_user_model

def custom_timestamp_id():
    dt = datetime.datetime.now()
    # strftime 日付時刻から文字列を生成。引数にフォーマット渡せる
    return dt.strftime('%Y%m%d%H%M%S%f')

class Order(models.Model):
    id = models.CharField(
        default=custom_timestamp_id, editable=False,primary_key=True,max_length=50
    )
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    uid = models.CharField(editable=False, max_length=50)
    is_confirmed = models.BooleanField(default=False)
    amount = models.PositiveIntegerField(default=0)
    tax_included = models.PositiveIntegerField(default=0)
    books  = models.JSONField() #JsonField
    shipping = models.JSONField()
    shipping_at = models.DateTimeField(blank=True, null=True)
    canceled_at = models.DateTimeField(blank=True, null=True)
    memo = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.id