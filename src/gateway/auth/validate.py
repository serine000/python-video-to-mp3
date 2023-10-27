import os
import requests


def check_token(request):
    """
    Validate the user's request to check for correct  authorization token.

    Args:
            request: The user request

    Returns:
            str: Success message if the file was successfully uploaded.
            str: Error message if the access token is invalid.
    """
    if "Authorization" not in request.headers:
        return None, ("missing credentials", 401)

    token = request.headers["Authorization"]
    if not token:
        return None, ("missing credentials", 401)

    validate_service_address = \
        f"http://{os.environ.get('AUTH_SERVICE_GATEWAY')}/validate"
    response = requests.post(
            validate_service_address,
            headers = {"Authorization": token},
            )

    if response.status_code == 200:
        return response.text, None
    else:
        return None, (response.text, response.status_code)
