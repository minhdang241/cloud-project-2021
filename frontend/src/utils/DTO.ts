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

export type CourseItemDTO = {
  course_id: number;
};

export type CourseParamsDTO = {
  career_id: number;
  school_id: number;
};

export type SkillParamsDTO = {
  course_list: CourseItemDTO[];
  career_id: number;
};
