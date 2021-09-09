import axios from "axios";
import { keysToSnake } from "utils/functions";
import { API } from "utils/constants";
import { CourseItem, CourseParams, SkillParams } from "utils/Types";
import { CourseItemDTO } from "utils/DTO";

export const getAllCareers = (page?: number, size?: number) => {
  const paramsDTO = keysToSnake({ page: page, size: size });
  return axios.get(`${API.BACKEND}/careers`, {
    params: paramsDTO,
  });
};

export const getRecommendCourses = (career: number) => {
  const body: CourseParams = { careerId: career, schoolId: 1 };
  console.log(body);
  return axios.post(`${API.BACKEND}/careers`, keysToSnake(body));
};

export const getSkills = (list: CourseItem[], career: number) => {
  const snakeList: CourseItemDTO[] = keysToSnake(list);
  const body: SkillParams = { courseList: snakeList, careerId: career };
  return axios.post(`${API.BACKEND}/mismatch_skills`, keysToSnake(body));
};
