import axios from "axios";
import { keysToSnake } from "utils/functions";
import { API } from "utils/constants";
import { CourseItem, SkillParams } from "utils/Types";
import { CourseItemDTO, SkillParamsDTO } from "utils/DTO";

export const getAllCourses = (page?: number, size?: number) => {
  const paramsDTO = keysToSnake({ page: page, size: size });
  return axios.get(`${API.BACKEND}/courses`, {
    params: paramsDTO,
  });
};

export const getRecommendCareer = (list: CourseItem[]) => {
  const snakeList: CourseItemDTO[] = keysToSnake(list);
  const body: Partial<SkillParams> = { courseList: snakeList };
  return axios.post(`${API.BACKEND}/careers`, keysToSnake(body));
};
