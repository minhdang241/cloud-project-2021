import axios from "axios";
import { keysToSnake } from "utils/functions";
import { API } from "utils/constants";
import { getHeaders } from "utils/functions";

export const getAllCourses = (
  name: string,
  page?: number,
  size?: number,
  sort?: string,
  order?: string,
  title?: string,
) => {
  const paramsDTO = keysToSnake({ page: page, size: size, sortedBy: sort, order: order, title: title });
  return axios.get(`${API.BACKEND}/courses`, {
    params: paramsDTO,
    headers: getHeaders(name),
  });
};

export const getRecommendCareer = (name: string, list: number[]) => {
  const params = list.join("&course_ids=");
  return axios.get(`${API.BACKEND}/recommendation/careers?course_ids=${params}`, {
    headers: getHeaders(name),
  });
};

export const getJobsByCareer = (name: string, career: number, page?: number, size?: number) => {
  const paramsDTO = keysToSnake({ page: page, size: size, careerId: career });
  return axios.get(`${API.BACKEND}/jobs`, {
    params: paramsDTO,
    headers: getHeaders(name),
  });
};
