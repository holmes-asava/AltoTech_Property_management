from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase
from user_manager.models import User
from work_manager.models import WorkOrder, TechnicianRequest
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
        self.testing_description = "testing_description"
        self.testing_defect_type = TechnicianRequest.DefectType.Electricity

    def generate_testing_data(self, work_type):
        data = {
            "room": 0,
            "work_type": work_type,
        }
        if work_type == WorkOrder.WorkType.MAID_REQUEST:
            data["description"] = self.testing_description
        elif work_type == WorkOrder.WorkType.TECHNICIAN_REQUEST:
            data["defect_type"] = self.testing_defect_type
        elif work_type == WorkOrder.WorkType.AMENITY_REQUEST:
            data["amenity_request_list"] = {"toothbrush": 1}
        return data

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
                url="/work_order/", data=self.generate_testing_data(type.value)
            )
            if type in [
                WorkOrder.WorkType.AMENITY_REQUEST,
                WorkOrder.WorkType.TECHNICIAN_REQUEST,
            ]:
                self.assertEqual(self.response.status_code, status.HTTP_201_CREATED)
            else:
                self.assertEqual(self.response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_work_order_by_maid(self):
        self.given_user(self.maid_user)
        for type in WorkOrder.WorkType:
            self.user_posts(
                url="/work_order/", data=self.generate_testing_data(type.value)
            )
            if type in [
                WorkOrder.WorkType.AMENITY_REQUEST,
                WorkOrder.WorkType.TECHNICIAN_REQUEST,
            ]:
                self.assertEqual(self.response.status_code, status.HTTP_403_FORBIDDEN)
            else:
                self.assertEqual(self.response.status_code, status.HTTP_201_CREATED)

    def test_create_work_order_by_supervisor(self):
        self.given_user(self.supervisor_user)
        for type in WorkOrder.WorkType:
            self.user_posts(
                url="/work_order/", data=self.generate_testing_data(type.value)
            )
            if type in [
                WorkOrder.WorkType.AMENITY_REQUEST,
            ]:
                self.assertEqual(self.response.status_code, status.HTTP_403_FORBIDDEN)
            else:
                self.assertEqual(self.response.status_code, status.HTTP_201_CREATED)
