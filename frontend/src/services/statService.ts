import axios from "axios";
import { keysToSnake } from "utils/functions";
import { API } from "utils/constants";

export const getCourseLevel = () => {
  return axios.get(`${API.BACKEND}/courses/types`);
};
