import { ENDPOINTS } from '@/constants/api';
import { request, prepareRequestHeader } from '@/services/api/client';

export async function trackParcel(params, id) {
  return request.get(ENDPOINTS.TRACK, {
    params: { ...params },
  });
}
