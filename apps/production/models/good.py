from django.db import models


class Good(models.Model):
    shop = models.ForeignKey('shop.Shop', on_delete=models.CASCADE, related_name='goods')
    name = models.CharField(max_length=50)

    supplier = models.ForeignKey('production.Supplier', null=True, blank=True,
                                 on_delete=models.SET_NULL, related_name='goods')
    order_lead_time = models.TimeField(null=True, blank=True)

    # META
    class Meta:
        ordering = ('name',)
        unique_together = ('shop', 'name')
