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
from django.db import models

class Tag(models.Model):
	name = models.CharField(max_length=64)
	icon = models.FileField(upload_to="icons/", blank=True, null=True)

	def __str__(self):
		return self.name

	class Meta:
		verbose_name = _("tag")
		verbose_name_plural = _("tags")


class BusinessArea(models.Model):
	name = models.CharField(max_length=64)

	def __str__(self):
		return self.name

	class Meta:
		verbose_name = _("business area")
		verbose_name_plural = _("business areas")

class Category(models.Model):
	name = models.CharField(max_length=64)

	def __str__(self):
		return self.name

	class Meta:
		verbose_name = _("category")
		verbose_name_plural = _("categories")


class AcquisitionType(models.Model):
	name = models.CharField(max_length=64)

	def __str__(self):
		return self.name

	class Meta:
		verbose_name = _("acquisition type")
		verbose_name_plural = _("acquisition types")

class Owner(models.Model):
	firstname = models.CharField(max_length=64)
	lastname = models.CharField(max_length=64)

	def __str__(self):
		return "%s %s" % (self.firstname, self.lastname)

	class Meta:
		verbose_name = _("owner")
		verbose_name_plural = _("owners")

class Item(models.Model):
	name = models.TextField()
	description = models.TextField(blank=True, verbose_name=_('description'))
	business_area = models.ForeignKey(BusinessArea, verbose_name=_('business area'), on_delete=models.PROTECT)
	category = models.ForeignKey(Category, verbose_name=_('category'), on_delete=models.PROTECT)
	decommissioned = models.BooleanField(verbose_name=_('decommissioned'),default=False)
	targetQuantity = models.IntegerField(blank=True, null=True, verbose_name=_('target quantity'))
	depreciation = models.BooleanField(verbose_name=_('deprecation'),default=False)
	datasheet = models.FileField(upload_to="datasheets/", blank=True, null=True, verbose_name=_('datasheet'))
	parent = models.ForeignKey('self', blank=True, null=True, on_delete=models.SET_NULL, verbose_name=_('parent'), related_name='item_parents')
	temp_parent = models.ForeignKey('self', blank=True, null=True, on_delete=models.SET_NULL, verbose_name=_('temporal parent'), related_name='item_temp_parents')
	inUse = models.BooleanField(verbose_name=_('in use'),default=False)
	supplier = models.TextField(blank=True, verbose_name=_('supplier'))
	note = models.TextField(blank=True, verbose_name=_('note'))
	ean = models.IntegerField(blank=True, null=True, verbose_name=_('EAN'))
	premium = models.BooleanField(verbose_name=_('premium'),default=False)
	unlabeled = models.BooleanField(verbose_name=_('unlabeled'),default=False)
	image = models.ImageField(upload_to="images/", blank=True, null=True, verbose_name=_('image'))
	contact = models.TextField(blank=True, verbose_name=_('contact'))
	tag = models.ManyToManyField(Tag, verbose_name=_('tags'))
	permanentLoan = models.BooleanField(verbose_name=_('permanent loan'),default=False)
	owner = models.ForeignKey(Owner, blank=True, null=True, on_delete=models.SET_NULL, verbose_name=_('owner'))

	def barcodes(self):
		barcodes = Barcode.objects.filter(item = self.id)
		result = ', '.join(str(barcode.code) for barcode in barcodes)
		return result
	barcodes.short_description = _("barcodes")

	def one_barcode(self):
		barcodes = Barcode.objects.filter(item = self.id)
		return barcodes[0].code if barcodes else None

	def has_parent(self):
		if self.parent is not None:
			return True
		return False

	def has_barcode(self):
		if self.barcodes() != "":
			return True
		return False

	def __str__(self):
		return _(u"%(name)s (codes: %(barcodes)s)") % {'name': self.name, 'barcodes': self.barcodes()}

	class Meta:
		verbose_name = _("item")
		verbose_name_plural = _("items")

class Barcode(models.Model):
	code = models.CharField(max_length=10,primary_key=True)
	item = models.ForeignKey(Item, on_delete=models.CASCADE)

	def __str__(self):
		return "%s" % self.code

	def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
		self.code = self.code.upper().strip()
		super(Barcode, self).save(force_insert, force_update, using, update_fields)

	class Meta:
		verbose_name = _("barcode")
		verbose_name_plural = _("barcodes")

class Acquisition(models.Model):
	item = models.ForeignKey(Item, on_delete=models.CASCADE)
	date = models.DateField()
	amount = models.IntegerField()
	unitPrice = models.IntegerField(blank=True, null=True)
	kind = models.ForeignKey(AcquisitionType, on_delete=models.PROTECT)

	def __str__(self):
		return "%s: %s (%sx)" % (self.date, self.item, self.amount)

	class Meta:
		verbose_name = _("acquisition")
		verbose_name_plural = _("acquisitions")

class Elimination(models.Model):
	item = models.ForeignKey(Item, verbose_name=_("Item"), on_delete=models.CASCADE)
	date = models.DateField(verbose_name=_("Date"))
	revenue = models.IntegerField(verbose_name=_("Revenue"), help_text=_("Please use the following format: <em>Money in Cent</em>."))
	reason = models.TextField(verbose_name=_("Reason"))

	def __str__(self):
		return "%s: %s" % (self.date, self.item.__str__())

	class Meta:
		verbose_name = _("elimination")
		verbose_name_plural = _("eliminations")

class Inventory(models.Model):
	item = models.ForeignKey(Item, on_delete=models.CASCADE)
	date = models.DateField()
	amount = models.IntegerField()

	def __str__(self):
		return "%s: %s (%s)" % (str(self.date), str(self.item), str(self.amount))

	class Meta:
		verbose_name = _("inventory")
		verbose_name_plural = _("inventory")
