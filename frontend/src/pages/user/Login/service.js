import { ENDPOINTS } from '@/constants/api';
import { request, prepareRequestHeader } from '@/services/api/client';

export async function login(body, options) {
  return request.post(ENDPOINTS.LOGIN, {
    data: body,
    headers: prepareRequestHeader(body, options),
  });
}

export async function getCurrentUser(params) {
  return request.get(ENDPOINTS.CURRENT_USER, {
    params: { ...params },
  });
}
