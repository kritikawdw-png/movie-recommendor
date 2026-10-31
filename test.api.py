
import requests

url = "https://api.themoviedb.org/3/movie/440"

params = {
    "api_key":"d4d18088f0081cc8f68bb2880ee5a32b"
}

try:
    response = requests.get(
        url,
        params=params,
        timeout=30
    )

    print("Status:", response.status_code)
    print("Response:", response.text[:500])

except requests.exceptions.Timeout:
    print("TMDB connection timed out!")

except requests.exceptions.ConnectionError:
    print("Internet or network connection problem!")

except requests.exceptions.RequestException as e:
    print("Error:", e)
