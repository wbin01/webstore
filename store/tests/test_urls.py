#!/usr/bin/env python3
from django.test import TestCase, RequestFactory
from store.views import index


class URLSTestCase(TestCase):

    def setUp(self) -> None:
        self.factory = RequestFactory()

    def test_url_index(self) -> None:
        request = self.factory.get('/')
        with self.assertTemplateUsed('index.html'):
            response = index(request)
            self.assertEqual(response.status_code, 200)
