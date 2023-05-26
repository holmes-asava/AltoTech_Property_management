from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase
from user_manager.models import User
from work_manager.models import WorkOrder
from django.urls import reverse


class WorkOrderTestCase(APITestCase):
    def setUp(self):
        self.guest_user = User.objects.create(
            email="guest@gmail.com", role_type=User.RoleType.GUEST
        )
        self.maid_user = User.objects.create(
            email="maid@gmail.com", role_type=User.RoleType.MAID
        )
        self.supervisor_user = User.objects.create(
            email="supervisor@gmail.com", role_type=User.RoleType.SUPERVISOR
        )

    def given_user(self, user):
        self.current_user = user
        self.client.force_login(user)

    def ser_gets(self, url):
        self.response = self.client.get(url, format="json")
        self.response_json = self.response.json()
        return self.response_json

    def user_posts(self, url, data, format="json", content_type="application/json"):
        self.response = self.client.post(url, data, format)
        self.response_json = self.response.json()
        return self.response_json

    def user_put(self, url, data, format="json", content_type="application/json"):
        self.response = self.client.put(url, data, format, content_type)
        self.response_json = self.response.json()
        return self.response_json

    def user_patch(self, url, data, format="json", content_type="application/json"):
        self.response = self.client.patch(url, data, format, content_type)
        self.response_json = self.response.json()
        return self.response_json

    def test_create_work_order_by_guest(self):
        self.given_user(self.guest_user)
        for type in WorkOrder.WorkType:
            self.user_posts(
                url="/work_order/",
                data={
                    "room": 0,
                    "work_type": type.value,
                    "amenity_request_list": {"test": 1234},
                },
            )
