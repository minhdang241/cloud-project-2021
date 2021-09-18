import {
  CareerDTO,
  CareerOptionDTO,
  CourseDTO,
  CourseLevelDTO,
  CourseParamsDTO,
  JobDTO,
  KeysToCamelCase,
  RequestDTO,
  SkillDTO,
} from "./DTO";

export interface Dictionary<T> {
  [Key: string]: T;
}

export type Course = KeysToCamelCase<CourseDTO>;
export type Career = KeysToCamelCase<CareerDTO>;
export type CareerOption = KeysToCamelCase<CareerOptionDTO>;
export type Job = KeysToCamelCase<JobDTO>;
export type CourseParams = KeysToCamelCase<CourseParamsDTO>;
export type Skill = KeysToCamelCase<SkillDTO>;
export type CourseLevel = KeysToCamelCase<CourseLevelDTO>;
export type Request = KeysToCamelCase<RequestDTO>;
