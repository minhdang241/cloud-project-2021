import axios from "axios";
import { keysToSnake } from "utils/functions";
import { API } from "utils/constants";
import { CourseParams } from "utils/Types";
import { getHeaders } from "utils/functions";

export const getAllCareers = (name: string, page?: number, size?: number) => {
  const paramsDTO = keysToSnake({ page: page, size: size });
  return axios.get(`${API.BACKEND}/careers`, {
    params: paramsDTO,
    headers: getHeaders(name),
  });
};

export const getCoursesByCareer = (name: string, career: number, page?: number, size?: number) => {
  const paramsDTO = keysToSnake({ page: page, size: size });
  const body: CourseParams = { careerId: career, schoolId: 1 };
  return axios.get(`${API.BACKEND}/recommendation/courses`, {
    params: { ...paramsDTO, ...keysToSnake(body) },
    headers: getHeaders(name),
  });
};

export const getSkills = (name: string, list: number[], career: number) => {
  const courseList = list.join("&course_ids=");
  const params = { careerId: career };
  return axios.get(`${API.BACKEND}/recommendation/mismatch_skills?course_ids=${courseList}`, {
    params: keysToSnake(params),
    headers: getHeaders(name),
  });
};
