from habr.api.serializers import UserSerializer


# Create your views here.
def jwt_response_payload_handler(token, user, request):
    user = request.POST.user
    data = UserSerializer(user, context={'request': request}).data
    print(data['username'])
    return ({
        "id": data['id'],
        "username": data['username'],
        "first_name": data['first_name'],
        "last_name": data['last_name'],
        "email": data['email'],
        "date_joined": data['date_joined']

    })
