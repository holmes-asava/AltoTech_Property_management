from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase
from user_manager.models import User
from work_manager.models import WorkOrder, TechnicianRequest
from django.urls import reverse
from datetime import datetime
from datetime import timedelta


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

    def generate_testing_data_updating(self, work_status):
        return {
            "assigned_to": self.maid_user.id,
            "room": 0,
            "start_at": datetime.now() + timedelta(days=-1),
            "finished_at": datetime.now() + timedelta(days=1),
            "work_status": work_status,
        }

    def generate_testing_data_creation(self, work_type):
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

    def user_posts(self, url, data, format="json"):
        self.response = self.client.post(url, data, format)
        self.response_json = self.response.json()
        return self.response_json

    def user_put(self, url, data, format="json"):
        self.response = self.client.put(url, data, format)
        self.response_json = self.response.json()
        return self.response_json

    def user_patch(self, url, data, format="json"):
        self.response = self.client.patch(url, data, format)
        self.response_json = self.response.json()
        return self.response_json

    def assertResponseWithWorkStatus(self, type, work_status, key=None):
        if (
            work_status == WorkOrder.WorkStatus.CANCEL_BY_GUEST
            and type != WorkOrder.WorkType.CLEANING
            and (not key or key == "work_status")
        ):
            self.assertEqual(self.response.status_code, status.HTTP_400_BAD_REQUEST)
        else:
            self.assertEqual(self.response.status_code, status.HTTP_200_OK)

    def test_create_work_order_by_guest(self):
        self.given_user(self.guest_user)
        for type in WorkOrder.WorkType:
            self.user_posts(
                url="/work_order/", data=self.generate_testing_data_creation(type.value)
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
                url="/work_order/", data=self.generate_testing_data_creation(type.value)
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
                url="/work_order/", data=self.generate_testing_data_creation(type.value)
            )
            if type in [
                WorkOrder.WorkType.AMENITY_REQUEST,
            ]:
                self.assertEqual(self.response.status_code, status.HTTP_403_FORBIDDEN)
            else:
                self.assertEqual(self.response.status_code, status.HTTP_201_CREATED)

    def test_update_work_order_by_guest(self):
        self.given_user(self.guest_user)
        for type in WorkOrder.WorkType:
            data = self.generate_testing_data_creation(type.value)
            target_workorder = WorkOrder.objects.create(**data)
            self.user_put(
                url=f"/work_order/{target_workorder.work_order_number}/",
                data=self.generate_testing_data_updating(
                    WorkOrder.WorkStatus.IN_PROGRESS
                ),
            )
            self.assertEqual(self.response.status_code, status.HTTP_403_FORBIDDEN)
            self.user_patch(
                url=f"/work_order/{target_workorder.work_order_number}/",
                data=self.generate_testing_data_updating(
                    WorkOrder.WorkStatus.IN_PROGRESS
                ),
            )
            self.assertEqual(self.response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_work_order_by_maid(self):
        self.given_user(self.maid_user)
        for type in WorkOrder.WorkType:
            data = self.generate_testing_data_creation(type.value)
            target_workorder = WorkOrder.objects.create(**data)
            for work_status in WorkOrder.WorkStatus:
                updating_data = self.generate_testing_data_updating(work_status)
                self.user_put(
                    url=f"/work_order/{target_workorder.work_order_number}/",
                    data=updating_data,
                )
                self.assertResponseWithWorkStatus(type, work_status)
                for key, value in updating_data.items():
                    self.user_patch(
                        url=f"/work_order/{target_workorder.work_order_number}/",
                        data={key: value},
                    )
                    self.assertResponseWithWorkStatus(type, work_status, key)

    def test_update_work_order_by_supervisor(self):
        self.given_user(self.supervisor_user)
        for type in WorkOrder.WorkType:
            data = self.generate_testing_data_creation(type.value)
            target_workorder = WorkOrder.objects.create(**data)
            for work_status in WorkOrder.WorkStatus:
                updating_data = self.generate_testing_data_updating(work_status)
                self.user_put(
                    url=f"/work_order/{target_workorder.work_order_number}/",
                    data=updating_data,
                )
                self.assertResponseWithWorkStatus(type, work_status)
                for key, value in updating_data.items():
                    self.user_patch(
                        url=f"/work_order/{target_workorder.work_order_number}/",
                        data={key: value},
                    )
                    self.assertResponseWithWorkStatus(type, work_status, key)

    def test_update_work_order_failed_when_update_not_allowed(self):
        test_not_allowed_fields = {
            "created_by": self.supervisor_user.id,
            "work_order_number": 1234,
            "work_type": WorkOrder.WorkType.CLEANING,
            "amenity_request_list": {"test": 1},
            "description": "testing_description",
            "defect_type": TechnicianRequest.DefectType.Electricity,
        }
        for user in [self.maid_user, self.supervisor_user]:
            self.given_user(user)
            for not_allowed_ket, not_allow_value in test_not_allowed_fields.items():
                for type in WorkOrder.WorkType:
                    data = self.generate_testing_data_creation(type.value)
                    target_workorder = WorkOrder.objects.create(**data)
                    for work_status in WorkOrder.WorkStatus:
                        updating_data = self.generate_testing_data_updating(work_status)
                        updating_data.update({not_allowed_ket: not_allow_value})
                        self.user_put(
                            url=f"/work_order/{target_workorder.work_order_number}/",
                            data=updating_data,
                        )
                        self.assertEqual(
                            self.response.status_code, status.HTTP_400_BAD_REQUEST
                        )

                    self.user_patch(
                        url=f"/work_order/{target_workorder.work_order_number}/",
                        data={not_allowed_ket: not_allow_value},
                    )
                    self.assertEqual(
                        self.response.status_code, status.HTTP_400_BAD_REQUEST
                    )
