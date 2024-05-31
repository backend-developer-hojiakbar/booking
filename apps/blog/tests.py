import os
from rest_framework.test import APITestCase
from django.urls import reverse
from  apps.blog.models import Booking
from django.contrib.auth.models import User


class ReservationAPITest(APITestCase):
    def setUp(self):
        self.reservation_data = {
            'user': 'John Doe',
            'from_date': '2024-04-03',
            'guests_number': '19',
            'to_date': '2024-04-06',
        }
        self.reservation = Booking.objects.create(**self.reservation_data)


    def test_create_reservation(self):
        url = reverse('booking-list')
        response = self.client.post(url, self.reservation_data, format='json')
        self.assertEqual(response.status_code, 201)

    def test_get_reservation_list(self):
        url = reverse('booking-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_update_reservation(self):
        url = reverse('booking-detail', args=[self.reservation.id])
        updated_data = {'user': 'Jane Doe'}
        response = self.client.put(url, updated_data, format='json')
        self.assertEqual(response.status_code, 200)

    def test_delete_reservation(self):
        url = reverse('booking-detail', args=[self.reservation.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204)


# class ReservationApiTestCase(APITestCase):
#     base_url = reverse('booking-list')
#     reservation_data = {
#         'user': 'John Doe',
#         'from_date': '2024-04-03',
#         'guests_number': '19',
#         'to_date': '2024-04-06',
#     }
#     def test_create_reservation(self):
#         url = reverse('booking-list')
#         response = self.client.post(url, self.reservation_data, format='json')
#         self.assertEqual(response.status_code, 201)
