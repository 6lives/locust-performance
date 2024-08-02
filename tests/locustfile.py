import random
import uuid

from locust import HttpUser, task, between

import logging
from http.client import HTTPConnection

HTTPConnection.debuglevel = 1
logging.basicConfig()
logging.getLogger().setLevel(logging.DEBUG)
requests_log = logging.getLogger("requests.packages.urllib3")
requests_log.setLevel(logging.DEBUG)
requests_log.propagate = True


class DemoQaRegisterUser(HttpUser):
    wait_time = between(1, 2)
    pages = [
        '/elements',
        '/forms',
        '/alertsWindows',
        '/widgets',
        '/interaction'
    ]



    # @task
    # def home_page(self):
    #     self.client.get("/hello", name='homepage')

    # @task
    # def view_items(self):
    #     for page in self.pages:
    #         self.client.get(page, name=f"page item {page}")

    @task
    def login(self):
        user = {
            "password": f'A{random.randint(1, 5)}@bAAAAAAAAA',
            "userName": f"username-{uuid.uuid4()}"
        }

        with self.client.post('/Account/v1/User', json=user) as response:
            if not response.json()['userID']:
                response.failure('userid not created')

        with self.client.post('/Account/v1/GenerateToken', json=user) as response1:
            if response1.json()['status'] == 'Failed':
                response1.failure('unsuccessful login')
