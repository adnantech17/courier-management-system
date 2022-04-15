import { ENDPOINTS } from '@/constants/api';
import { request, prepareRequestHeader } from '@/services/api/client';

export async function checkRouteParcel(params, id) {
  return request.get(`${ENDPOINTS.CHECK_ROUTE}${id}/`, {
    params: { ...params },
  });
}

export async function routeParcel(data) {
  return request.post(ENDPOINTS.ROUTE, {
    data,
  });
}
