import requests
from config.config import TOKEN_URL, USERNAME, PASSWORD, AUTH_HEADER, ACCEPT_HEADER

def generate_token():
    payload = {
        'grant_type': 'password',
        'username': USERNAME,
        'password': PASSWORD
    }

    headers = {
        'Authorization': AUTH_HEADER,
        'Accept': ACCEPT_HEADER,
        'Content-Type': 'application/x-www-form-urlencoded',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36'
    }

    print("Payload:", payload)  # Debug: Print the payload
    print("Headers:", headers)  # Debug: Print the headers

    try:
        response = requests.post(TOKEN_URL, data=payload, headers=headers)
        response.raise_for_status()
        token = response.json().get('access_token')
        if token:
            print(f"Generated token: {token}")
        return token
    except requests.exceptions.HTTPError as err:
        print(f"Error generating token: {err.response.status_code} - {err.response.text}")
        return None

if __name__ == "__main__":
    generate_token()
