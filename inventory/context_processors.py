from inventory.conf import get_barcode_code_length


def barcode_settings(request):
    _min_len, max_len = get_barcode_code_length()
    return {"barcode_code_max_length": max_len}
