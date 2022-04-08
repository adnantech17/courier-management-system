import { extend } from 'umi-request';

export const request = extend({
  prefix: 'http://localhost:8000',
});

export const prepareRequestHeader = (payload, options = {}) => {
  const adjustedOptions = {
    ...options,
  };
  if (payload instanceof FormData) {
    adjustedOptions['Content-Type'] = 'multipart/form-data';
  } else {
    adjustedOptions['Content-Type'] = 'application/json';
  }
  return adjustedOptions;
};
