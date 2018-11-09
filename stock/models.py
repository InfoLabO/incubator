from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    category = models.ForeignKey(Category)
    # The amount of the product we have in stock. Updated by signals on the ProductRefill model
    stock_amount = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class Barcode(models.Model):
    product = models.ForeignKey("stock.Product")
    code = models.CharField(max_length=150, unique=True)

    def __str__(self):
        return "Barcode |{}| for {}".format(self.code, self.product)


class StockRefill(models.Model):
    """
    Represents a stock refilling event. Tracks who and when refilled the stock, uses ProductRefill in order
        to track each individual stock that was increased.
    """
    user = models.ForeignKey(
        "users.User", null=True, blank=True, on_delete=models.SET_NULL,
        help_text=(
            "The person responsible for this stock refilling."
            "Ideally the person who did the data entry after shopping"
        )
    )
    when = models.DateTimeField(default=timezone.now)
    updates = models.ManyToManyField(
        to="stock.Product", through="stock.ProductRefill",
        help_text="All the product stocks that were increased in this refill"
    )

    def __str__(self):
        return "Stock refilled by {} on {}".format(self.user, self.when)


class ProductRefill(models.Model):
    """
    Many to many intermediary table used in order to store the product stock being increased and its quantity

    Regrouped in StockRefill.

    Has signals that trigger upon creation and upon an update. See signals.py
    """
    class Meta:
        unique_together = ("refill", "product")

    refill = models.ForeignKey("stock.StockRefill", help_text="The refill that generated this update")
    product = models.ForeignKey("stock.Product", help_text="The product whose stock was refilled")
    amount = models.PositiveIntegerField(
        help_text="The quantity by which the stock was increased",
        validators=[MinValueValidator(1, message="You cannot add a negative amount of stock")]
    )

    def __str__(self):
        return "Refill of {} by {} unit(s)".format(self.product, self.amount)


class Stocktaking(models.Model):
    """
    Represents a stock taking event. Tracks who and when checked the inventory, uses InventoryLine in order
        to track each individual stock that was updated.
    """
    user = models.ForeignKey(
        "users.User", null=True, blank=True, on_delete=models.SET_NULL,
        help_text=("The person responsible for this stock taking.")
    )
    when = models.DateTimeField(default=timezone.now)
    updates = models.ManyToManyField(
        to="stock.Product", through="stock.StocktakeLine",
        help_text="All the product stocks that were updated in this inventory"
    )

    def __str__(self):
        return "Inventory taken by {} on {}".format(self.user, self.when)


class StocktakeLine(models.Model):
    """
    Many to many intermediary table used in order to store the product stock being updated during
        inventory of stock.
    """
    class Meta:
        unique_together = ("stock_taking", "product")

    stock_taking = models.ForeignKey(
        "stock.Stocktaking",
        help_text="The stocktaking that generated this update"
    )
    product = models.ForeignKey("stock.Product", help_text="The product whose stock was refilled")
    old_amount = models.PositiveIntegerField(help_text="Amount before the inventory")
    new_amount = models.PositiveIntegerField(
        help_text="Amount as counted by the inventory",
        validators=[MinValueValidator(0, message="You cannot have a negative amount of stock")]
    )

    @property
    def delta(self):
        return self.new_amount - self.old_amount

    def __str__(self):
        return "Refill of {} by {} unit(s)".format(self.product, self.amount)


class Transaction(models.Model):
    class Meta:
        abstract = True

    user = models.ForeignKey("users.User")
    when = models.DateTimeField(auto_now_add=True)


class TransferTransaction(Transaction):
    receiver = models.ForeignKey("users.User", related_name="incoming_transfers")
    amount = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return "{} a transféré {}€ à {}".format(self.user, self.amount, self.receiver)


class TopupTransaction(Transaction):
    amount = models.DecimalField(max_digits=6, decimal_places=2)
    topup_type = models.CharField(
        max_length=20,
        choices=[
            ('BANK', "Virement"),
            ('CASH', "Caisse"),
        ],
    )

    def __str__(self):
        return "{} a versé {}€ sur son ardoise. ({})".format(self.user, self.amount, self.get_topup_type_display())


class ProductTransaction(models.Model):
    user = models.ForeignKey("users.User", null=True, blank=True)
    when = models.DateTimeField(auto_now_add=True)
    product = models.ForeignKey("stock.Product")
    paid_price = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        editable=False,
        help_text="The price for which the product was sold at the time of the transaction"
    )

    def save(self, *args, **kwargs):
        if not self.pk:
            # Populate the price at the moment the transaction was created
            self.paid_price = self.product.price
        super().save(*args, **kwargs)

    def __str__(self):
        return "{} a dépensé {}€ pour le produit {}".format(self.user, self.product.price, self.product)


class MiscTransaction(Transaction):
    amount = models.DecimalField(max_digits=6, decimal_places=2)
    info = models.TextField()

    def __str__(self):
        return "{} a dépensé {}€ pour {}".format(self.user, self.amount, self.info)
