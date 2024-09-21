from django.contrib import admin
from . import models


@admin.register(
    models.Product
)  # saying that this class is the admin model for Product. then we don't need admin.site.register
class ProductAdmin(admin.ModelAdmin):
    list_display = [
        "title",
        "unit_price",
        "inventory",
        "inventory_status",
        "collection_title",
    ]  # affiche les colonnes title, unit_price, inventory dans l'admin panel
    list_editable = [
        "unit_price",
        "inventory",
    ]  # permet d'éditer les colonnes unit_price et inventory directement dans l'admin panel. Propose un input field pour chaque cellule
    list_per_page = 10
    list_select_related = [
        "collection"
    ]  # permet de faire un join avec la table collection. Réduit le nombre de queries

    @admin.display(ordering="inventory")  # permet de trier par inventory
    def inventory_status(self, product):
        if product.inventory < 10:
            return "Low"
        return "OK"

    @admin.display(
        ordering="collection__title"
    )  # permet de trier par collection__title
    def collection_title(self, product):
        return product.collection.title


@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = [
        "first_name",
        "last_name",
        "membership",
    ]
    ordering = ["first_name", "last_name"]
    list_filter = ["membership"]
    list_editable = ["membership"]
    search_fields = ["first_name", "last_name"]
    list_per_page = 10


@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "placed_at",
        "customer",
    ]
    list_filter = ["payment_status"]
    list_per_page = 10


# Register your models here.
admin.site.register(models.Collection)
# admin.site.register(models.Product, ProductAdmin) plus besoin de ça parce qu'on a déjà fait ça avec @admin.register
