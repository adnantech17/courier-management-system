import { ENDPOINTS } from '@/constants/api';
import { request } from '@/services/api/client';

export async function getUsers(params) {
  return request.get(ENDPOINTS.USER, {
    params: params,
  });
}

export async function addUser(data, options) {
  return request.post(ENDPOINTS.USER, {
    data,
  });
}

export async function updateUser(data) {
  return request.patch(`${ENDPOINTS.USER}${data.id}/`, {
    data,
  });
}
