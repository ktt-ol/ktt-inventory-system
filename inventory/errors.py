import logging

from django.http import Http404

logger = logging.getLogger(__name__)


def raise_not_found(request):
    raise Http404('Raised on purpose to render the 404 page')


def raise_server_error(request):
    if not request.user.is_staff:
        raise Http404
    logger.warning('Deliberate error raised by %s', request.user)
    raise RuntimeError(
        f'Raised on purpose by {request.user} to render the 500 page'
    )
