import axios, { AxiosResponse } from "axios";
import { keysToSnake } from "utils/functions";
import { JobDistrictDTO, WordFrquenciesDTO } from "utils/DTO";
import { API } from "utils/constants";

export const getCourseLevel = () => {
  return axios.get(`${API.BACKEND}/courses/levels`);
};

export const getCourseWordCloud = (): Promise<AxiosResponse<WordFrquenciesDTO>> => {
  return axios.get(`${API.BACKEND}/courses/word-cloud`);
};

export const getJobWordCloud = (): Promise<AxiosResponse<WordFrquenciesDTO>> => {
  return axios.get(`${API.BACKEND}/jobs/word-cloud`);
};

export const getJobCompany = (): Promise<AxiosResponse<WordFrquenciesDTO>> => {
  return axios.get(`${API.BACKEND}/jobs/company`);
};

export const getJobDistrict = (): Promise<AxiosResponse<JobDistrictDTO>> => {
  return axios.get(`${API.BACKEND}/jobs/district`);
};
