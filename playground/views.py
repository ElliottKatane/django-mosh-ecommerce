from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
from store.models import Product, Order

# Create your views here.
# it's a request handler. It takes a request and returns a response


def say_hello(request):
    # exists = Product.objects.filter(pk=1).exists()
    # name = "Worldo" if exists else "World"
    # __contains lookup type is case sensitive. __icontains is case insensitive
    # on peut ajouter deux fois __: collection__id__gt=1 par exemple

    # queryset = (
    #     Product.objects.prefetch_related("promotions")
    #     .select_related("collection")
    #     .all()
    # )
    queryset = (
        Order.objects.select_related("customer")
        .prefetch_related("orderitem_set")
        .order_by("-placed_at")[:5]
    )
    return render(request, "hello.html", {"name": "sup", "orders": list(queryset)})
