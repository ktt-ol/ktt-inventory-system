from django.conf import settings

BARCODE_CODE_LENGTH_DEFAULT = (4, 6)


def get_barcode_code_length():
    return (
        getattr(settings, 'BARCODE_CODE_LENGTH', None)
        or BARCODE_CODE_LENGTH_DEFAULT
    )
