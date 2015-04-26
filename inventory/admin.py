# Copyright (c) 2012-2013 Sebastian Reichel <sre@ring0.de>
#
# Permission to use, copy, modify, and/or distribute this software for any
# purpose with or without fee is hereby granted, provided that the above
# copyright notice and this permission notice appear in all copies.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES WITH
# REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY
# AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY SPECIAL, DIRECT,
# INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM
# LOSS OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE OR
# OTHER TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION WITH THE USE OR
# PERFORMANCE OF THIS SOFTWARE.

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
	#filter_vertical = ('item',)
	pass

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
