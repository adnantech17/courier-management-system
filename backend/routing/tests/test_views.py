
import json
from rest_framework import status
from django.test import TestCase, Client
from django.urls import reverse

class TestBranchViews(TestCase) :
    def setUp(self):
        self.client = Client()
        self.branchurl = reverse('branch_api')
        self.branchedgeurl = reverse('branch_edge_api')
        self.post_branch_valid_data = {
            "name":"sample_branch",
            "estimated_processing_time":1,
            "estimated_processing_cost":1
        }
        self.post_branch_invalid_data = {
            "name":"sample_branch",
            "estimated_processing_time":1,
            "estimated_processing_cost":-1
        }
        self.patch_branch_valid_data = {
            "id":1,
            "name":"sample_branch",
            "estimated_processing_time":1,
            "estimated_processing_cost":2
        }
        self.patch_branch_invalid_data = {
            "id":1,
            "name":"sample_branch",
            "estimated_processing_time":1,
            "estimated_processing_cost":-1
        }

    def test_branch_api_get(self):
        self.client.post(self.branchurl,self.post_branch_valid_data)
        self.assertEquals(self.client.get(self.branchurl).status_code, status.HTTP_200_OK)
    def test_branch_api_post_valid_data(self):
        response = self.client.post(self.branchurl,self.post_branch_valid_data)
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)
    def test_branch_api_post_invalid_data(self):
        response = self.client.post(self.branchurl,self.post_branch_invalid_data)
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)
    def test_branch_api_patch_invalid_data(self):
        self.client.post(self.branchurl,self.post_branch_valid_data)
        self.assertEquals(self.client.patch(
            reverse('branch_api_with_primary_key',args=[1]),
            json.dumps(self.patch_branch_invalid_data),
            content_type='application/json'
            ).status_code,status.HTTP_400_BAD_REQUEST)
    
    def test_branch_api_valid_data(self):
        self.client.post(self.branchurl,self.post_branch_valid_data)
        self.assertEquals(self.client.patch(
            reverse('branch_api_with_primary_key',args=[1]),
            json.dumps(self.patch_branch_valid_data),
            content_type='application/json'
            ).status_code,status.HTTP_202_ACCEPTED)
    
    def test_branch_api_delete(self):
        self.client.post(self.branchurl,self.post_branch_valid_data)
        self.assertEquals(self.client.delete(
            reverse('branch_api_with_primary_key',args=[1]),
            ).status_code,status.HTTP_200_OK)


class TestBranchEdgeViews(TestCase):
    def setUp(self):
        self.client = Client()
        self.branchurl = reverse('branch_api')
        self.branchedgeurl = reverse('branch_edge_api')
        self.post_branch_valid_data1 = {
            "name":"sample_branch1",
            "estimated_processing_time":1,
            "estimated_processing_cost":1
        }
        self.post_branch_valid_data2 = {
            "name":"sample_branch2",
            "estimated_processing_time":2,
            "estimated_processing_cost":2
        }
        self.client.post(self.branchurl,self.post_branch_valid_data1)
        self.client.post(self.branchurl,self.post_branch_valid_data2)


        self.post_edge_valid_data = {
            "from_branch":1,
            "to_branch":2,
            "shipping_time":5,
            "shipping_cost":30
        }
        self.post_edge_invalid_data = {
            "from_branch":1,
            "to_branch":3,
            "shipping_time":5,
            "shipping_cost":30
        }
        self.post_edge_invalid_data_range = {
            "from_branch":1,
            "to_branch":2,
            "shipping_time":5,
            "shipping_cost":-30
        }
    def test_edge_post_valid_data(self):
        self.assertEquals(self.client.post(self.branchedgeurl,self.post_edge_valid_data).status_code, status.HTTP_201_CREATED)
    def test_edge_post_invalid_data_set(self):
        self.assertEquals(self.client.post(self.branchedgeurl,self.post_edge_invalid_data).status_code, status.HTTP_400_BAD_REQUEST)
    def test_edge_post_invalid_data_range(self):
        self.assertEquals(self.client.post(self.branchedgeurl,self.post_edge_invalid_data_range).status_code, status.HTTP_400_BAD_REQUEST)
    def test_edge_get(self):
        self.client.post(self.branchedgeurl,self.post_edge_valid_data)
        self.assertEquals(self.client.get(self.branchedgeurl).status_code, status.HTTP_200_OK)
    