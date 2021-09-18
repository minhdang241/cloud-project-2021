/* eslint-disable camelcase */

import { Dictionary } from "./Types";

type CamelCase<S extends string> = S extends `${infer P1}_${infer P2}${infer P3}`
  ? `${Lowercase<P1>}${Uppercase<P2>}${CamelCase<P3>}`
  : Lowercase<S>;

export type KeysToCamelCase<T> = {
  [K in keyof T as CamelCase<string & K>]: T[K] extends Dictionary<T> ? KeysToCamelCase<T[K]> : T[K];
};

export type CourseDTO = {
  id: number;
  code: string;
  title: string;
  description: string;
  outcome: string;
  level: "BASIC" | "ADVANCED";
};

export type JobDTO = {
  title: string;
  company_name: string;
  company_location: string;
  short_description: string;
  link: string;
};

export type CareerDTO = {
  career: string;
  job_list: KeysToCamelCase<JobDTO>[];
};

export type CareerOptionDTO = {
  id: number;
  career_path: string;
  total_jobs: number;
};

export type CourseParamsDTO = {
  career_id: number;
  school_id: number;
};

export type SkillItemDTO = {
  name: string;
  recommended_courses: CourseDTO[];
};

export type SkillDTO = {
  missing_skills: KeysToCamelCase<SkillItemDTO>[];
  matching_skills: KeysToCamelCase<SkillItemDTO>[];
};

export type CourseLevelDTO = {
  level: string;
  count: number;
};

export type WordFreqDTO = {
  value: string;
  count: number;
};

export type WordFrquenciesDTO = {
  words: Array<WordFreqDTO>;
};

export type JobDistrictDTO = {
  company_district: number;
  count: number;
};
