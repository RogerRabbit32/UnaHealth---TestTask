import pytest
from django.urls import reverse
from rest_framework import status
from django.contrib.auth.models import User

from rest_framework.test import APIClient
import io


@pytest.fixture
def user(db):
    return User.objects.create_user(username='testuser', password='password')


@pytest.fixture
def api_client():
    return APIClient()


def test_upload_csv_success(user, api_client):
    url = reverse('glucoselevel-upload')
    csv_content = "Gerät,Seriennummer,Datum,Uhrzeit,Messeinheit 1,Glukosewert 1,Messeinheit 2,Glukosewert 2,Status\n" \
                  "Test Device,12345678,20-02-2021 23:57,0,100,1,200,1,OK\n"
    csv_file = io.BytesIO(csv_content.encode('utf-8'))
    csv_file.name = 'test.csv'

    data = {
        'file': csv_file,
        'user_id': user.id
    }

    response = api_client.post(url, data, format='multipart')
    assert response.status_code == status.HTTP_201_CREATED


def test_upload_csv_missing_file(user, api_client):
    url = reverse('glucoselevel-upload')
    data = {
        'user_id': user.id
    }

    response = api_client.post(url, data, format='multipart')
    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_upload_csv_missing_user_id(api_client):
    url = reverse('glucoselevel-upload')
    csv_content = "Gerät,Seriennummer,Datum,Uhrzeit,Messeinheit 1,Glukosewert 1,Messeinheit 2,Glukosewert 2,Status\n" \
                  "Test Device,12345678,20-02-2021 23:57,0,100,1,200,1,OK\n"
    csv_file = io.BytesIO(csv_content.encode('utf-8'))
    csv_file.name = 'test.csv'

    data = {
        'file': csv_file,
    }

    response = api_client.post(url, data, format='multipart')
    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_export_excel_missing_user_id(api_client):
    url = reverse('glucoselevel-export')

    response = api_client.get(url)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
