import requests

if __name__ == "__main__":
    res = requests.delete(
        url='http://127.0.0.1:8000/resource/t6'
    )

    print(res.status_code)
    print(res.json())