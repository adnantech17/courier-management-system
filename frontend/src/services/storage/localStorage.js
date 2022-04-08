export const setItem = (index, data) => {
  localStorage.setItem(index, data);
};

export const getItem = (index) => {
  localStorage.getItem(index);
};

export const removeItem = (index) => {
  localStorage.removeItem(index);
};
