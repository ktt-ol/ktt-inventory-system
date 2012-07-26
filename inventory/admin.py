from django.utils.translation import ugettext_lazy as _
from django.contrib import admin
from django.forms.widgets import Select
from django.db.models import ForeignKey
import filters
import models

class BarcodeInline(admin.TabularInline):
	model = models.Barcode
	fk_name = "item"

class ItemAdmin(admin.ModelAdmin):
	formfield_overrides = {
		ForeignKey: {'widget': Select(attrs = {'class': 'chzn-select'})}
	}

	list_per_page = 100
	list_filter = (
		filters.HasParent,
		filters.HasBarcode,
		'decommissioned',
		'tag',
	)
	list_display = ('name','category','inUse','parent','barcodes')
	ordering = ['-id',]
	search_fields = ['name', 'description', 'barcode__code']
	filter_horizontal = ('tag',)
	save_as = True
	inlines = [ BarcodeInline, ]

class TagAdmin(admin.ModelAdmin):
	ordering = ['name',]
	list_filter = (
		filters.HasIcon,
	)
	search_fields = ['name',]

class BarcodeAdmin(admin.ModelAdmin):
	ordering = ['code',]
	search_fields = ['code',]

class EliminationAdmin(admin.ModelAdmin):
	filter_vertical = ('item',)

admin.site.register(models.Item, ItemAdmin)
admin.site.register(models.Owner)
admin.site.register(models.AcquisitionType)
admin.site.register(models.Acquisition)
admin.site.register(models.Elimination, EliminationAdmin)
admin.site.register(models.Inventory)
admin.site.register(models.Tag, TagAdmin)
admin.site.register(models.BusinessArea)
admin.site.register(models.Category)
admin.site.register(models.Barcode, BarcodeAdmin)
