import requests

def authenticate_token(token):
    auth_url = "http://localhost:3000/check-token"
    headers = {'Authorization': f'Bearer {token}'}

    try:
        print("Received token:", token)
        response = requests.get(auth_url, headers=headers)
        response.raise_for_status()  # Raise an exception for non-2xx responses
        data = response.json()
        if 'message' in data and data['message'] == 'Token is valid':
            return True
        else:
            return False
    except requests.exceptions.RequestException as e:
        print('Error authenticating token:', e)
        return False