import os
import requests


def check_login(request):
    """
    Send request authorization to check for correct user login authorization.

    Args:
            request: The user request

    Returns:
            str: Token if the user is validated.
            str: Error message if the access token is invalid.
    """
    auth = requests.authorization
    if not auth:
        return None, ("missing credentials", 401)
    basicAuth = (auth.username, auth.password)

    auth_service_address = \
        f"http://{os.environ.get('AUTH_SERVICE_GATEWAY')}/login"

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
