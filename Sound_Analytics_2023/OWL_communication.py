import requests
from typing import Union
import sys
import base64


def get_data_from_OWL(data_name: str) -> list:
    """ getData to get data from OWL database
        param:  data_name: is the name of the desired data to collect from https://iotgarage.expericom.ericsson.net/owl/#owl-storage-record
                example; bee_n_pollen

        return: a dictionary on success or an exception if the data couldn't be found."""
    try:
        URL = "https://iotgarage.expericom.ericsson.net/owl/owlws/v2/storage/records/data"

        # send POST request to thedatabase URL, with data_name
        response = requests.post(url=URL, json={"keys": [data_name]})  # {"keys": ["bee_n_pollen"]}

        # data fetched and not an empty array
        if (response.status_code == 200 and response.json()[data_name] != []):
            data = response.json()

            # format response into an array
            values = []
            for entry in data[data_name]:
                val = entry['data'].split(": ")[1][:1]
                values.append(val)
            print(values)

            return values

        else:
            print("\n\Data fetch couldn't success; ", data_name, "doesn't seem to exist in the database...\n\n")
            return []

    except Exception as error:
        raise Exception(error)


def get_latest_img_from_OWL(data_name: str) -> str:
    try:
        URL = "https://iotgarage.expericom.ericsson.net/owl/owlws/v2/storage/records/data"

        # send POST request to thedatabase URL, with data_name
        response = requests.post(url=URL, json={"keys": [data_name]})  # {"keys": ["bee_n_pollen"]}

        # data fetched and not an empty array
        if (response.status_code == 200 and response.json()[data_name] != []):
            data = response.json()

            # if we fetch a picture
            entry = data[data_name][len(data[data_name]) - 1]
            val = entry['data'].split('"')[1:-1][2]
            base64 = val.split(',')[1]

            return base64

        else:
            print("\n\Data fetch couldn't success; ", data_name, "doesn't seem to exist in the database...\n\n")
            return ''

    except Exception as error:
        raise Exception(error)


def post_list_to_OWL(
        sensor_type_list: list, sensor_val_list: list, owl_auto_name: str, store: bool = True
) -> int:
    """
    Post list of sensor_vals of type float/int to OWL app under the tags in the list sensor_type
    Store argument (True by default) specifies if the values are to be stored in OWL
    Returns the status code of the request to the server
    """
    try_count = 0

    while try_count < 5:
        try:
            data2post = '{"user":"hampus","auto":['
            for i in range(len(sensor_val_list)):
                if i != 0:
                    data2post = data2post + ","
                data2post = data2post + construct_data_string(
                    owl_auto_name,
                    sensor_type_list[i],
                    sensor_val_list[i],
                    store,
                )
            data2post = data2post + "]}"
            print(data2post)
            response = requests.post(
                "https://iotgarage.expericom.ericsson.net/bee_team/owl/owlws/v2/auto/execute",
                # "https://iotgarage.expericom.ericsson.net/owl/owlws/v2/auto/execute",
                headers={
                    "Content-type": "application/json",
                    "Cookie": "owl40.connect.sid=s:gVw-F0WS-GAbgZeXRw1V4BPB7wZXqhrT.1w8YvFp5/ZstXo+kBuZzRXtZPgDdueQ+egZb6i/5bTU; owl.connect.sid=s:Or9TLlMegn67cdtqdnY4ggOIY6hWw55S.Pqg1vwyhZxEt1IHyQQYPWQJU/+genih53KyzZRkDrT0",
                },
                data=data2post,
            )
            status = response.status_code
            if status != 200:
                response.close()
                print("trying to post list again")
                try_count += 1
            else:
                print("List posted to Owl")
                try_count = 5
                response.close()
        except Exception:
            try:
                print("Error posting list to Owl:")
                print("Err1: " + str(sys.exc_info))
                try_count = 5
                response.close()
            except Exception:
                status = 0
                print("Post to Owl failed")
    return status


def construct_data_string(
        app_name: str, sensor_type: str, sensor_val: Union[str, int, float], store: bool
) -> str:
    """
    Helper function to post methods
    Formats app_name, sensor_type, sensor_val and store boolean to a string that can be sent as input to OWL
    """
    if store:
        store_string = "true"
    else:
        store_string = "false"

    data_string = (
            '{"name":"'
            + app_name
            + '","trace":true,"args":{"name":"'
            + sensor_type
            + '","value":"'
            + str(sensor_val)
            + '","store":'
            + store_string
            + "}}"
    )
    return data_string


def test_post_list_to_OWL() -> None:
    """
    Test to see whether the method can post the list to OWL
    Use store = false and a sensor_type that OWL does not expect to make sure no changes are made in OWL
    """

    status = post_list_to_OWL(
        ["sound_analysis"],
        ["Test post3"],
        'auto_sound',
        True)

    print(status)
    assert status == 200

