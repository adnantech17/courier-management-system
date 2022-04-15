import { ENDPOINTS } from '@/constants/api';
import { request, prepareRequestHeader } from '@/services/api/client';

export async function checkReceivedSerial(params, id) {
  return request.get(`${ENDPOINTS.CHECK_RECEIVE}${id}/`, {
    params: { ...params },
  });
}

export async function receiveParcel(data) {
  return request.post(ENDPOINTS.RECEIVE, {
    data,
  });
}
