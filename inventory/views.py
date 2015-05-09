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

from django.shortcuts import get_object_or_404
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import render_to_response
from django.shortcuts import render
from django.http import HttpResponse
from django.db.models import Q
import models
from django.core.mail import mail_admins
from forms import UploadFileForm
from django.core.exceptions import ObjectDoesNotExist
from models import Barcode



def home(request):
	return render_to_response('home.html')


def item(request, selectedid):
	p = get_object_or_404(models.Barcode, pk=selectedid.upper())

	parentpath = []
	temp_parentpath = []

	x = p.item
	parentpath.append(x)
	x = x.parent
	while x:
		parentpath.append(x)
		if x.temp_parent:
			x = x.temp_parent
		else:
			x = x.parent

	x = p.item
	while x:
		temp_parentpath.append(x)
		if x.temp_parent:
			x = x.temp_parent
		else:
			x = x.parent


	temp_parentpath.reverse()
	parentpath.reverse()

	parameters = {
		"user": request.user,
		"id": p.item.id,
		"image": p.item.image,
		"name": p.item.name,
		"codes": p.item.barcodes(),
		"description": p.item.description,
		"supplier": p.item.supplier,
		"note": p.item.note,
		"in_use": p.item.inUse,
		"parent": p.item.parent,
		"temporary_parent": p.item.temp_parent,
		"parentpath": parentpath,
		"temporary_parentpath": temp_parentpath,
		"children": models.Item.objects.filter(Q(parent = p.item.id) | Q(temp_parent = p.item.id)),
		"tags": p.item.tag.all(),
		"owner": p.item.owner,

	}
	return render_to_response('item.html', parameters)


def search(request, term):
	results = models.Item.objects.filter(Q(name__contains = term) | Q(description__contains = term))

	return render_to_response('search.html', {
		"term": term,
		"results": results
	})


def graph(request):
	items = models.Item.objects.all()

	result = render_to_response('graph.txt', {"items": items})
	result['Content-Type'] = "text/plain; charset=utf-8"

	return result


def upload(request):
	#if request.method == 'POST':
	form = UploadFileForm(request.POST, request.FILES)
	if form.is_valid() and request.user.is_authenticated:
		codefile = request.FILES['file']
		data = codefile.read().splitlines()

		if request.POST['type'] == '1':
			parent = ''
			for code in data:
				if code != 'NEWPARENT':
					if parent == '':
						p = get_object_or_404(models.Barcode, pk=code.upper())
						parent = code
					else:
						i = get_object_or_404(models.Barcode, pk=code.upper())
						i.item.parent = p.item
						i.item.save()
				else:
					parent = ''
		elif request.POST['type'] == '2':
			index = 0
			error = 0
			business_area = models.BusinessArea.objects.get(name='ideell')
			category = models.Category.objects.get(name='Inventar')
			parent = models.Barcode.objects.get(code='H0000')
			tag = models.Tag.objects.get(name='Regale & Storage')

			for code in data:
				if code[0] == 'H' and len(code) == 5:
					try:
						b = Barcode.objects.get(code=code.upper())
						error += 1
						data[index] = code + ' existiert bereits'
					except ObjectDoesNotExist:
						description = 'Borte im Hochregal \nReihe: ' + code[1] + '\nRegal: ' + code[2]
						i = models.Item(name='Regalborte', description=description, business_area=business_area, category=category, parent=parent.item)
						i.save()
						barcode = Barcode(code=code, item=i)
						barcode.save()
				else:
					data[index] = code + ' ist nicht im richtigen Format'
					error += 1
				index += 1
		return render(request, 'upload.html', {'form': form, 'data': data})
	else:
		form = UploadFileForm()
	return render(request, 'upload.html', {'form': form})


def stats(request):
	return render_to_response('stats.html', {
		"number_of_codes": models.Barcode.objects.count(),
		"number_of_items": models.Item.objects.count(),
		"number_of_items_with_parent": models.Item.objects.filter(parent__isnull=False).count(),
		"number_of_items_without_parent": models.Item.objects.filter(parent__isnull=True).count(),
		"max_barcodes_item": models.Item.objects.raw('SELECT inventory_item.*, COUNT(inventory_barcode.item_id) AS number_of_attached_barcodes FROM inventory_item INNER JOIN inventory_barcode ON inventory_barcode.item_id = inventory_item.id GROUP BY inventory_barcode.item_id ORDER BY COUNT(inventory_barcode.item_id) DESC LIMIT 1;')[0],
	})
