from django.utils.deprecation import MiddlewareMixin


class TransformMiddleware(MiddlewareMixin):
    white_list = [
        'api/user/auth'
    ]
    
    def __call__(self, request):
        """
        Change request body to str type
        :param request:
        :return:
        """
        if isinstance(request.body, bytes) and request.path not in self.white_list:
            # api/user/auth rest_framework auth
            data = getattr(request, '_body', request.body)
            request._body = data.decode('utf-8')
        response = self.get_response(request)
        return response
