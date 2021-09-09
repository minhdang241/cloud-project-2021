import axios from "axios";
import { keysToSnake } from "utils/functions";
import { API } from "utils/constants";

export const getAllCourses = (page?: number, size?: number) => {
  const paramsDTO = keysToSnake({ page: page, size: size });
  return axios.get(`${API.BACKEND}/courses`, {
    params: paramsDTO,
  });
};

export const getRecommendCareer = (list: number[]) => {
  const params = list.join("&course_ids=");
  return axios.get(`${API.BACKEND}/recommendation/careers?course_ids=${params}`);
};
