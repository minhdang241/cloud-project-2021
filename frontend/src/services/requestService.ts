import axios from "axios";
import { keysToSnake } from "utils/functions";
import { API } from "utils/constants";

export const getRequests = (page?: number, size?: number, orderField?: string) => {
  const paramsDTO = keysToSnake({ page: page, size: size, orderField: orderField });
  return axios.get(`${API.BACKEND}/requests`, {
    params: paramsDTO,
  });
};
