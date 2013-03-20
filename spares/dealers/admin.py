from django.contrib import admin
from spares.dealers.models import Dealer


class DealersAdmin(admin.ModelAdmin):
    list_display = ('name', 'webSite')
    list_filter = ('webSite',)

admin.site.register(Dealer, DealersAdmin)