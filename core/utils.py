from rest_framework.views import exception_handler


def custom_exception(exc, context):
    response = exception_handler(exc, context)

    if response is not None:
        response.data['status_code'] = response.status_code
        response.data['error_message'] = response.data.get('detail', 'An error occurred.')
    return response
