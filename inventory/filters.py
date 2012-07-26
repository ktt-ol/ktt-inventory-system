from django.utils.translation import ugettext_lazy as _
from django.contrib.admin import SimpleListFilter
import models

class HasParent(SimpleListFilter):
	# Human-readable title which will be displayed in the
	# right admin sidebar just above the filter options.
	title = _('has parent')

	# Parameter for the filter that will be used in the URL query.
	parameter_name = 'has_parent'

	def lookups(self, request, model_admin):
		"""
		Returns a list of tuples. The first element in each
		tuple is the coded value for the option that will
		appear in the URL query. The second element is the
		human-readable name for the option that will appear
		in the right sidebar.
		"""
		return (
			('yes', _('Yes')),
			('no',  _('No')),
		)

	def queryset(self, request, queryset):
		"""
		Returns the filtered queryset based on the value
		provided in the query string and retrievable via
		`self.value()`.
		"""
		# Compare the requested value (either 'None' or 'other')
		# to decide how to filter the queryset.
		if self.value() == 'yes':
			return queryset.filter(parent__isnull = False)
		if self.value() == 'no':
			return queryset.filter(parent__isnull = True)

class HasBarcode(SimpleListFilter):
	# Human-readable title which will be displayed in the
	# right admin sidebar just above the filter options.
	title = _('has barcode')

	# Parameter for the filter that will be used in the URL query.
	parameter_name = 'has_barcode'

	def lookups(self, request, model_admin):
		"""
		Returns a list of tuples. The first element in each
		tuple is the coded value for the option that will
		appear in the URL query. The second element is the
		human-readable name for the option that will appear
		in the right sidebar.
		"""
		return (
			('yes', _('Yes')),
			('no',  _('No')),
		)

	def queryset(self, request, queryset):
		"""
		Returns the filtered queryset based on the value
		provided in the query string and retrievable via
		`self.value()`.
		"""
		# Compare the requested value (either 'None' or 'other')
		# to decide how to filter the queryset.
		if self.value() == 'yes':
			return queryset.filter(barcode__isnull = False)
		if self.value() == 'no':
			return queryset.filter(barcode__isnull = True)

class HasIcon(SimpleListFilter):
	# Human-readable title which will be displayed in the
	# right admin sidebar just above the filter options.
	title = _('has icon')

	# Parameter for the filter that will be used in the URL query.
	parameter_name = 'has_icon'

	def lookups(self, request, model_admin):
		"""
		Returns a list of tuples. The first element in each
		tuple is the coded value for the option that will
		appear in the URL query. The second element is the
		human-readable name for the option that will appear
		in the right sidebar.
		"""
		return (
			('yes', _('Yes')),
			('no',  _('No')),
		)

	def queryset(self, request, queryset):
		"""
		Returns the filtered queryset based on the value
		provided in the query string and retrievable via
		`self.value()`.
		"""
		# Compare the requested value (either 'None' or 'other')
		# to decide how to filter the queryset.
		if self.value() == 'yes':
			return queryset.filter(icon__isnull = False)
		if self.value() == 'no':
			return queryset.filter(icon__isnull = True)
