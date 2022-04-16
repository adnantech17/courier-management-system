import { ENDPOINTS } from '@/constants/api';
import { request } from '@/services/api/client';

export async function getBranches(params) {
  return request.get(ENDPOINTS.BRANCH, {
    params: params,
  });
}

export async function addBranch(data, options) {
  return request.post(ENDPOINTS.BRANCH, {
    data,
  });
}

export async function updateBranch(data) {
  return request.patch(`${ENDPOINTS.BRANCH}${data.id}/`, {
    data,
  });
}

export async function deleteBranch(id) {
  return request.delete(`${ENDPOINTS.BRANCH}${id}/`);
}

export async function getSingleUser(params, id) {
  return request.get(`${ENDPOINTS.USER}/${id}`, {
    params: params,
  });
}

export async function getBranchesForDropdown(params) {
  try {
    const data = await request.get(ENDPOINTS.BRANCH, {
      params: { ...params, page_size: 0 },
    });
    return data.data.map((d) => {
      return {
        value: d.id,
        label: d.name,
      };
    });
  } catch (error) {
    throw error;
  }
}
