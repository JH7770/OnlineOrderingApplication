from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from order.models import Shop, Menu, Order, OrderFood
from order.serializer import ShopSerializer, MenuSerializer

from django.utils import timezone

@csrf_exempt  # 보안요소 추가
def shop(request):
    if request.method == 'GET':
        # shops = Shop.objects.all()
        # serializer = ShopSerializer(shops, many=True)  # Json
        # return JsonResponse(serializer.data, safe=False)
        shops = Shop.objects.all()
        return render(request, 'order/shop_list.html', {'shop_list':shops})
    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = ShopSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)


@csrf_exempt  # 보안요소 추가
def menu(request, shop):
    if request.method == 'GET':
        # menus = Menu.objects.filter(shop=shop)
        # serializer = MenuSerializer(menus, many=True)  # Json
        # return JsonResponse(serializer.data, safe=False)
        menus = Menu.objects.filter(shop=shop)
        return render(request, 'order/menu_list.html', {'menu_list':menus, 'shop':shop})
    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = MenuSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

@csrf_exempt
def order(request):
    if request.method == 'GET':
        order_list = Order.objects.all()
        return render(request, 'order/order_list.html', {'order_list':order_list})
    elif request.method =='POST':
        address = request.POST['address']
        order_date = timezone.now()
        shop = request.POST['shop']
        food_list = request.POST.getlist('menu')
        shop_item = Shop.objects.get(pk=shop)
        shop_item.order_set.create(address=address, order_date=order_date, shop=int(shop))

        order_item = Order.objects.get(pk = int(shop_item.order_set.lastest('id').id))
        for food in food_list:
            order_item.orderfood_set.create(food_name=food)


        return HttpResponse(status=200)