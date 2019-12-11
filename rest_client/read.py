import requests

if __name__ == "__main__":
    res = requests.get(
        url='http://127.0.0.1:8000/resource/t3'
    )
    print(res.status_code)
    d = res.json()
    print('sensor_id:', d['sensor_id'])
    print('temperature:', d['temperature'])
    print('location:', d['location'])
    print('datetime:', d['datetime'])

    # res = requests.get(
    #     url='http://127.0.0.1:8000/resource/location/3nd Engineering Building, KOREATECH'
    # )
    # print(res.status_code)
    # print(res.json())
