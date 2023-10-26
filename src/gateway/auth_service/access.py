import configparser
import os
import requests
import os
import requests


def login(request):
    auth = requests.authorization
    if not auth:
        return None, ("missing credentials", 401)
    basicAuth = (auth.username, auth.password)

    auth_service_address = f"http://{os.environ.get("AUTH_SERVICE_GATEWAY")}/login"

    try:
        response = requests.post(
                auth_service_address,
                auth = basicAuth
                )
    except (
            requests.exceptions.RequestException,
            requests.exceptions.Timeout,
            requests.exceptions.TooManyRedirects
            ) as e:
        return None, (str(e), 500)

    if response.status_code == 200:
        return response.text, None
    return None, (response.text, response.status_code)
