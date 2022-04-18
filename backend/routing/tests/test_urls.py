from random import randint
from django.test import TestCase
from django.urls import reverse, resolve
from routing.views import *

class TestUrls(TestCase):
    def test_branch_api_url(self) :
        url = reverse('branch_api')
        response = resolve(url)
        self.assertEquals(response.func.view_class,BranchAPI)
    def test_branch_api_with_primary_key_url(self) :
        url = reverse('branch_api_with_primary_key',args=[randint(0,1000)])
        response = resolve(url)
        self.assertEquals(response.func.view_class,BranchAPI)
    def test_branch_edge_api_url(self) :
        url = reverse('branch_edge_api')
        response = resolve(url)
        self.assertEquals(response.func.view_class,BranchEdgeAPI)
