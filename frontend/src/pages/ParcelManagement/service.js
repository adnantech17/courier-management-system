import { ENDPOINTS } from '@/constants/api';
import { request } from '@/services/api/client';

export async function getParcels(params) {
  return request.get(ENDPOINTS.PARCEL, {
    params: params,
  });
}

export async function addParcel(data, options) {
  return request.post(ENDPOINTS.PARCEL, {
    data,
  });
}

export async function updateParcel(data) {
  return request.patch(`${ENDPOINTS.PARCEL}${data.id}/`, {
    data,
  });
}
