def greet_middleware(get_response):
    def inner(request):
        print(f'Hello there, request to {request.get_full_path()}.')
        response = get_response(request)
        print('Goodbye, response!')
        return response
    return inner
