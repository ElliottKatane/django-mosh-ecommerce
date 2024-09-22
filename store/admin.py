from django.contrib import admin, messages
from django.urls import reverse
from django.utils.html import format_html, urlencode
from . import models
from django.db.models.aggregates import Count


class InventoryFilter(admin.SimpleListFilter):
    title = "inventory"
    parameter_name = "inventory"

    def lookups(self, request, model_admin):
        return [
            ("<10", "Low"),
            (">=10", "OK"),
        ]  # les valeurs qu'on veut afficher dans le dropdown. On retourne une liste de tuple. chaque tuple est un filtre. Le premier élément est la valeur qu'on veut afficher, le deuxième est la valeur qu'on veut passer dans l'url

    def queryset(
        self, request, queryset
    ):  # ici, on implémente notre logique de filtre. On retourne le queryset filtré
        if self.value() == "<10":
            return queryset.filter(inventory__lt=10)


@admin.register(
    models.Product
)  # saying that this class is the admin model for Product. then we don't need admin.site.register
class ProductAdmin(admin.ModelAdmin):
    # fields and exclude are mutually exclusive. You can't use both at the same time
    # they are used to customize the form in the admin panel
    autocomplete_fields = ["collection"]
    prepopulated_fields = {"slug": ["title"]}
    # permet de préremplir un champ en fonction d'un autre champ. si on édite manuellement le slug field, ça ne prendra pas le nouveau titre en compte
    actions = [
        "clear_inventory"
    ]  # permet d'ajouter une action custom dans l'admin panel. Le nom de l'action corresond EXACTEMENT au nom de la méthode qu'on veut appeler
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
    list_filter = ["collection", "last_update", InventoryFilter]
    list_select_related = [
        "collection"
    ]  # permet de faire un join avec la table collection. Réduit le nombre de queries
    search_fields = ["title"]

    @admin.display(
        ordering="collection__title"
    )  # permet de trier par collection__title
    def collection_title(self, product):
        return product.collection.title

    @admin.display(ordering="inventory")  # permet de trier par inventory
    def inventory_status(self, product):
        if product.inventory < 10:
            return "Low"
        return "OK"

    @admin.action(description="Clear inventory")
    def clear_inventory(self, request, queryset):
        updated_count = queryset.update(inventory=0)
        self.message_user(  # message_user est une méthode de la classe parente admin.ModelAdmin
            request,
            f"{updated_count} products were successfully updated",  # cet argument est le message qu'on veut afficher
            messages.INFO,  # la façon par laquelle le message ci-dessus sera affiché. (info = en vert, error en rouge, etc)
        )


@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = [
        "first_name",
        "last_name",
        "membership",
        "orders_count",  # Ensure this matches the method name exactly
    ]
    ordering = ["first_name", "last_name"]
    list_filter = ["membership"]
    list_per_page = 10
    list_editable = ["membership"]
    search_fields = ["first_name__istartswith", "last_name__istartswith"]

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(orders_count=Count("order"))

    @admin.display(description="Number of Orders", ordering="orders_count")
    def orders_count(self, customer):
        url = (
            reverse(
                "admin:store_order_changelist"
            )  # Ensure 'store_order_changelist' matches your app and model names
            + "?"
            + urlencode({"customer__id": str(customer.id)})
        )
        return format_html('<a href="{}"> {} </a>', url, customer.orders_count)


class OrderItemInline(admin.TabularInline):  # aussi possible d'utilsier StackedInline
    model = models.OrderItem
    autocomplete_fields = ["product"]
    min_num = 1
    max_num = 10
    extra = 0


@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    autocomplete_fields = ["customer"]
    inlines = [OrderItemInline]
    list_display = [
        "id",
        "placed_at",
        "customer",
    ]
    list_filter = ["payment_status"]
    list_per_page = 10


# Register your models here.
@admin.register(models.Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = [
        "title",
        "products_count",
    ]
    search_fields = ["title"]
    list_per_page = 10

    @admin.display(ordering="products_count")
    def products_count(self, collection):
        url = (
            reverse("admin:store_product_changelist")
            + "?"
            + urlencode({"collection__id": str(collection.id)})
        )
        return format_html('<a href="{}"> {} </a>', url, collection.products_count)

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(products_count=Count("product"))


# admin.site.register(models.Product, ProductAdmin) plus besoin de ça parce qu'on a déjà fait ça avec @admin.register
