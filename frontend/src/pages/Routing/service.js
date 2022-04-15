import { ENDPOINTS } from '@/constants/api';
import { request } from '@/services/api/client';

export async function getBranchEdges(params) {
  return request.get(ENDPOINTS.BRANCH_EDGE, {
    params: params,
  });
}

export async function branchLinkCreate(data, options) {
  return request.post(ENDPOINTS.BRANCH_EDGE, {
    data,
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
