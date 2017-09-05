# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from rest_framework.reverse import reverse
from rest_framework.authtoken.models import Token
from urlparse import urlparse
from .models import FileUpload

class FileUploadTests(APITestCase):
    def setUp(self):
        self.tearDown()
        user = User.objects.create_user('mytest', password='mytest',
                                     email='test@test.test')
        user.save()
        Token.objects.create(user=user)

    def tearDown(self):
        try:
            user = User.objects.get_by_natural_key('mytest')
            user.delete()
        except ObjectDoesNotExist:
            pass
        FileUpload.objects.all().delete()

    def _create_test_file(self, path):
        f = open(path, 'w')
        f.write('test123\n')
        f.close()
        f = open(path, 'rb')
        return {'datafile': f}

    def test_upload_file(self):
        url = reverse('fileupload-list')
        data = self._create_test_file('/tmp/test_upload')

        token = Token.objects.get(user__username='mytest')
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = client.post(url, data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('created', response.data)
        self.assertTrue(urlparse(
            response.data['datafile']).path.startswith(settings.MEDIA_URL))
        self.assertEqual(response.data['owner'],
                         User.objects.get_by_natural_key('mytest').id)
        self.assertIn('created', response.data)

        client.logout()
        response = client.post(url, data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
