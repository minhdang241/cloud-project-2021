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
  const snakeList = keysToSnake(
    list.map((c) => {
      return { courseId: c };
    }),
  );
  const body = keysToSnake({ courseList: snakeList });
  console.log(body);
  return axios.post(`${API.BACKEND}/careers`, body);
};
