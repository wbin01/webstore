#!/usr/bin/env python3
from django.test import TestCase, RequestFactory
from django.db.models import QuerySet
from store.models import *


class IndexViewTestCase(TestCase):

    def setUp(self) -> None:
        self.factory = RequestFactory()
