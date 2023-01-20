import requests
import json
import os
from requests_toolbelt.multipart.encoder import MultipartEncoder


class ApiClass:
    def __init__(self):
        self.base_url = "http://162.240.6.124:9054/swc-ai-tools/"

    def login(self, email, password):
        url = self.base_url + "1.0.0/login"
        data = {"email": email, "password": password}
        response = requests.post(url, data=data)
        return response.json()

    def aitools(self, image, email, token, folder_id):
        url = self.base_url + "1.0.0/aitools"
        with open(image, "r") as file:
            # Get the file name
            file_name = os.path.basename(image)
            # Get the file extension
            file_extension = os.path.splitext(image)[1][1:]
        data = MultipartEncoder(
            fields={
                "email": email,
                "token": token,
                "folder_id": folder_id,
                'image': (file_name, open(image, 'rb'), 'image/'+file_extension),
            }
        )
        response = requests.post(
            url, headers={'Content-Type': data.content_type}, data=data)
        return response.json()

    def update_report(self, data):
        url = self.base_url + "1.0.0/update_report"
        headers = {'Content-type': 'application/json'}

        response = requests.post(url, data=json.dumps(data), headers=headers)
        return response.json()
