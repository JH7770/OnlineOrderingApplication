from django.db import models


class Shop(models.Model):
    shop_name = models.CharField(max_length=20)
    shop_address = models.CharField(max_length=40)


class Menu(models.Model):
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE)  # shop을 외래 키로, shop 삭제 시 같이 삭제
    food_name = models.CharField(max_length=20)


class Order(models.Model):
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE)
    order_date = models.DateTimeField('date ordered')
    address = models.CharField(max_length=40)
    estimated_time = models.IntegerField(default=-1)  # 배달 예상 시간
    deliver_finish = models.BooleanField(default=0)


class OrderFood(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    food_name = models.CharField(max_length=20)
