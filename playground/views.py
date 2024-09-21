from django.shortcuts import render
from django.contrib.contenttypes.models import ContentType
from django.db.models.aggregates import Count, Max, Min, Sum, Avg
from store.models import Product, Order, OrderItem, Collection
from tags.models import TaggedItem

# Create your views here.
# it's a request handler. It takes a request and returns a response


def say_hello(request):
    # exists = Product.objects.filter(pk=1).exists()
    # name = "Worldo" if exists else "World"
    # __contains lookup type is case sensitive. __icontains is case insensitive
    # on peut ajouter deux fois __: collection__id__gt=1 par exemple

    # queryset = TaggedItem.objects.get_tags_for(Order, 2)

    # pour update un objet, il faut d'abord le get(), parce que si on update seulement un des fields sans expliciter les autres, les autres vont devenir des empty strings par exemple.
    collection = Collection.objects.get(pk=11)
    collection.title = "Games"
    collection.featured_product = None
    collection.save()

    # insert an object
    # collection = Collection()
    # collection.title = "Video Games"
    # collection.featured_product = Product.objects.get(pk=1)
    # collection.save()
    # collection.id
    return render(
        request,
        "hello.html",
        {"name": "sup", "tags": "tags"},
    )
