from rest_framework.response import Response
from rest_framework import status, exceptions
from rest_framework.views import exception_handler

def custom_exception_handler(exc, context):
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)
    if response:
        error_message = response.data.get('detail', '')

        if error_message:
            response.data = {}
            response.data['success'] = False
            response.data['data'] = None
            response.data['msg'] = error_message
        elif not isinstance(response.data.values()[0], basestring):
            data = response.data
            response.data = {}
            response.data['success'] = False
            response.data['data'] = data
            response.data['msg'] = "validation failed"
    return response

class CustomExceptionHandlerMixin(object):

    # override rest framework handle exception,
    # because we don't want change existing API response by define custom exception_handler
    def handle_exception(self, exc):
        """
        Handle any exception that occurs, by returning an appropriate response,
        or re-raising the error.
        """
        if isinstance(exc, (exceptions.NotAuthenticated,
                            exceptions.AuthenticationFailed)):
            # WWW-Authenticate header for 401 responses, else coerce to 403
            auth_header = self.get_authenticate_header(self.request)

            if auth_header:
                exc.auth_header = auth_header
            else:
                exc.status_code = status.HTTP_403_FORBIDDEN

        exception_handler = custom_exception_handler

        context = self.get_exception_handler_context()
        response = exception_handler(exc, context)

        if response is None:
            raise

        response.exception = True
        return response

def response_template(data=None, status=status.HTTP_200_OK, success=True, message=''):
    response_dict = {
        'success': success,
        'status_code': status,
        'data': data,
        'msg': message}
    return Response(status=status, data=response_dict)


def success_response(data=None):
    return response_template(data)

def created_response(data):
    return response_template(data, status.HTTP_201_CREATED)

def server_error_response(message=None):
    if not message:
        message = ("ups! something went wrong Please try again. "
                   "If you keep seeing this message please contact our customer services")
    return response_template(
        None, status.HTTP_500_INTERNAL_SERVER_ERROR, False, message)

def not_found_response(message, data=None):
    return response_template(
        data, status.HTTP_404_NOT_FOUND, False, message)

def general_error_response(message, data=None):
    return response_template(
        data, status.HTTP_400_BAD_REQUEST, False, message)
