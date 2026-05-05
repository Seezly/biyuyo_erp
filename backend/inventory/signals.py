from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from inventory.models import Product, InventoryMovement
import uuid


@receiver(post_save, sender=Product)
def create_initial_stock_movement(sender, instance, created, **kwargs):
    """
    Create an inventory movement when a product is created with initial stock.
    """
    if created and instance.stock and instance.stock > 0:
        InventoryMovement.objects.create(
            business_id=instance.business_id,
            product_id=instance,
            type='in',
            quantity=instance.stock,
            reference=f'Stock inicial - Producto creado'
        )


@receiver(pre_save, sender=Product)
def track_stock_adjustment(sender, instance, **kwargs):
    """
    Track stock changes for adjustment movements.
    Store the previous stock value for post_save comparison.
    """
    if instance.pk:
        try:
            instance._previous_stock = Product.objects.get(pk=instance.pk).stock or 0
        except Product.DoesNotExist:
            instance._previous_stock = 0
    else:
        instance._previous_stock = 0


@receiver(post_save, sender=Product)
def create_stock_adjustment_movement(sender, instance, created, **kwargs):
    """
    Create an inventory movement when product stock is adjusted after creation.
    """
    if created:
        return

    previous_stock = getattr(instance, '_previous_stock', 0)
    current_stock = instance.stock or 0

    if previous_stock != current_stock:
        difference = current_stock - previous_stock

        if difference > 0:
            movement_type = 'in'
            reference = f'Ajuste de stock: +{difference} unidades'
        else:
            movement_type = 'out'
            reference = f'Ajuste de stock: {difference} unidades'

        InventoryMovement.objects.create(
            business_id=instance.business_id,
            product_id=instance,
            type=movement_type,
            quantity=abs(difference),
            reference=reference
        )