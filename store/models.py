from django.db import models
from django.core.validators import MinValueValidator

# Create your models here.

# it will be possible to generate a db based on the models defined below


class Collection(models.Model):

    title = models.CharField(max_length=255)

    featured_product = models.ForeignKey(
        "Product", on_delete=models.SET_NULL, null=True, related_name="+"
    )

    def __str__(
        self,
    ) -> str:
        return self.title

    # __str__ is a magic method that returns a string representation of the object. Notamment dans admin panel, Store, le nom de chaque collection est montré par le titre plutot que par object (n)
    # use quotes for Product because it's defined below. It's a forward reference.

    class Meta:
        ordering = ["title"]  # order by title (in admin panel)


# many to many relationship with Product


class Promotion(models.Model):

    description = models.CharField(max_length=255)

    discount = models.FloatField()

    # product_set is the default name for the reverse relationship from Product to Promotion

    # we can change it by specifying related_name. It's a good practice to specify related_name everywhere if it's specified once.


class Product(models.Model):

    title = models.CharField(max_length=255)

    description = models.TextField(blank=True)

    # always use DecimalField for money. it's always required to specify max_digits and decimal_places
    unit_price = models.DecimalField(
        max_digits=6, decimal_places=2, validators=[MinValueValidator(1)]
    )  # validators=[MinValueValidator(1)] ensures that the value is at least 1

    inventory = models.IntegerField()

    # auto_now will set the field to now every time the object is saved

    # auto_now_add will set the field to now when the object is first created

    last_update = models.DateTimeField(auto_now=True)

    # on définit le parent chez l'enfant, pas l'inverse

    collection = models.ForeignKey(Collection, on_delete=models.PROTECT)

    # protect means that if the collection is deleted, the products contained in the collection will not be deleted

    promotions = models.ManyToManyField(Promotion, blank=True)

    # many-to-many relationship with Promotion. plural here because there may be several promotions.
    slug = models.SlugField()

    def __str__(
        self,
    ) -> str:
        return self.title

    # __str__ is a magic method that returns a string representation of the object. Notamment dans admin panel, Store, le nom de chaque collection est montré par le titre plutot que par object (n)
    # use quotes for Product because it's defined below. It's a forward reference.

    class Meta:
        ordering = ["title"]  # order by title (in admin panel)


class Customer(models.Model):

    MEMBERSHIP_BRONZE = "B"

    MEMBERSHIP_SILVER = "S"

    MEMBERSHIP_GOLD = "G"

    MEMBERSHIP_CHOICES = [
        (MEMBERSHIP_BRONZE, "Bronze"),
        (MEMBERSHIP_SILVER, "Silver"),
        (MEMBERSHIP_GOLD, "Gold"),
    ]

    first_name = models.CharField(max_length=255)

    last_name = models.CharField(max_length=255)

    email = models.EmailField(unique=True)

    phone = models.CharField(max_length=255)

    birth_date = models.DateField(null=True)

    # null=True allows the field to be empty

    membership = models.CharField(
        max_length=1, choices=MEMBERSHIP_CHOICES, default=MEMBERSHIP_BRONZE
    )

    # pas besoin de créer Address ici, car on a déjà une relation one-to-one avec Address. Django va s'en occuper
    def __str__(
        self,
    ) -> str:
        return f"{self.first_name, self.last_name}"  # au lieu d'avoir Customer Object (1), on aura le nom du customer quand on clique sur son nom

    class Meta:
        ordering = ["first_name"]  # order by title (in admin panel)


class Order(models.Model):

    PAYMENT_STATUS_PENDING = "P"

    PAYMENT_STATUS_COMPLETE = "C"

    PAYMENT_STATUS_FAILED = "F"

    PAYMENT_STATUS_CHOICES = [
        (PAYMENT_STATUS_PENDING, "Pending"),
        (PAYMENT_STATUS_COMPLETE, "Complete"),
        (PAYMENT_STATUS_FAILED, "Failed"),
    ]

    placed_at = models.DateTimeField(auto_now_add=True)

    payment_status = models.CharField(
        max_length=1, choices=PAYMENT_STATUS_CHOICES, default=PAYMENT_STATUS_PENDING
    )

    customer = models.ForeignKey(Customer, on_delete=models.PROTECT)


class OrderItem(models.Model):

    order = models.ForeignKey(Order, on_delete=models.PROTECT)

    product = models.ForeignKey(Product, on_delete=models.PROTECT)

    quantity = models.PositiveSmallIntegerField()

    # we have a unit price here because the price of the product can change, but we want to keep the price at the time of the order

    unit_price = models.DecimalField(max_digits=6, decimal_places=2)


class Address(models.Model):

    street = models.CharField(max_length=255)

    city = models.CharField(max_length=255)

    zip_code = models.CharField(max_length=10, null=True)

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)

    # if we want one-to-one: primarykey defined here because if not, django will create one, and relationship will be one-to-many (one customer can have many addresses)

    # on_delete=models.CASCADE means that if the customer is deleted, the address will also be deleted

    # on_delete=models.PROTECT is another option, which will prevent the deletion of the customer if the address is still associated with it


class Cart(models.Model):

    created_at = models.DateTimeField(auto_now_add=True)


class CartItem(models.Model):

    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)

    product = models.ForeignKey(Product, on_delete=models.PROTECT)

    quantity = models.PositiveSmallIntegerField()
