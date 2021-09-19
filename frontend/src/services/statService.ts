import axios, { AxiosResponse } from "axios";
import { getHeaders } from "utils/functions";
import { CountDTO, JobDistrictDTO, WordFrquenciesDTO } from "utils/DTO";
import { API } from "utils/constants";

export const getCourseLevel = (name: string) => {
  return axios.get(`${API.BACKEND}/courses/levels`, {
    headers: getHeaders(name),
  });
};

export const getCourseWordCloud = (name: string): Promise<AxiosResponse<WordFrquenciesDTO>> => {
  return axios.get(`${API.BACKEND}/courses/word-cloud`, {
    headers: getHeaders(name),
  });
};

export const getJobWordCloud = (name: string): Promise<AxiosResponse<WordFrquenciesDTO>> => {
  return axios.get(`${API.BACKEND}/jobs/word-cloud`, {
    headers: getHeaders(name),
  });
};

export const getJobCompany = (name: string): Promise<AxiosResponse<WordFrquenciesDTO>> => {
  return axios.get(`${API.BACKEND}/jobs/company`, {
    headers: getHeaders(name),
  });
};

export const getJobDistrict = (name: string): Promise<AxiosResponse<JobDistrictDTO>> => {
  return axios.get(`${API.BACKEND}/jobs/district`, {
    headers: getHeaders(name),
  });
};

export const getCounts = (name: string): Promise<AxiosResponse<CountDTO>> => {
  return axios.get(`${API.BACKEND}/counts`, {
    headers: getHeaders(name),
  });
};

export const crawl = (name: string) => {
  return axios.post(
    `${API.BACKEND}/requests`,
    {},
    {
      headers: getHeaders(name),
    },
  );
};
