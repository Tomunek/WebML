import json

import requests

GOOD_JSON = {
    "distance_from_home": 1.1111,
    "distance_from_last_transaction": 2.2222,
    "ratio_to_median_purchase_price": 3.3333,
    "repeat_retailer": 1,
    "fraud": 0}

BAD_JSON = {
    "distance_from_home": 1.1111,
    "distance_from_last_transaction": "wrong",
    "ratio_to_median_purchase_price": 3.3333,
    "repeat_retailer": 1,
    "fraud": 0}


def get() -> int:
    print("Sending GET request")
    request_get_all = requests.get('http://127.0.0.1:5000/api/data')
    print(f"Status Code: {request_get_all.status_code}")
    result_list = request_get_all.json()
    print(f"Data points: {len(result_list)}\n")
    return len(result_list)


def handle_response(response: requests.Response) -> int | None:
    print(f"Status Code: {response.status_code}")
    response_as_json = json.loads(response.content)
    if response.status_code == 200:
        record_id = response_as_json.get('id', None)
        print(f"Affected record with id: {record_id}\n")
        return record_id
    print(f"Error: {response_as_json.get('error', None)}\n")
    return None


def post(dictionary: dict) -> int | None:
    print("Sending POST request")
    response_post = requests.post('http://127.0.0.1:5000/api/data', json=dictionary)
    return handle_response(response_post)


def delete(record_id: int) -> int | None:
    print("Sending DELETE request")
    response_delete = requests.delete(f'http://127.0.0.1:5000/api/data/{record_id}')
    return handle_response(response_delete)


def main():
    # TODO: real API testing
    # this is just temporary
    count = get()

    added_id = post(GOOD_JSON)
    count2 = get()
    if count2 != count + 1:
        print("Math error! (sus)")
        print("Seriously: something went wrong")
        exit(1)

    post(BAD_JSON)
    count3 = get()
    if count3 != count2:
        print("Math error! (sus)")
        print("Seriously: something went wrong")
        exit(1)

    delete(added_id)
    count4 = get()
    if count4 != count3 - 1:
        print("Math error! (sus)")
        print("Seriously: something went wrong")
        exit(1)

    print("If you are here, it worked")


if __name__ == '__main__':
    main()
