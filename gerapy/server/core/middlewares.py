from django.utils.deprecation import MiddlewareMixin


class TransformMiddleware(MiddlewareMixin):
    def __call__(self, request):
        """
        Change request body to str type
        :param request:
        :return:
        """
        if isinstance(request.body, bytes):
            data = getattr(request, '_body', request.body)
            request._body = data.decode('utf-8')
        response = self.get_response(request)
        return response
