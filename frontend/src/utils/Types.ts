import { CareerDTO, CourseDTO, CourseItemDTO, CourseParamsDTO, JobDTO, KeysToCamelCase, SkillParamsDTO } from "./DTO";

export interface Dictionary<T> {
  [Key: string]: T;
}

export type Course = KeysToCamelCase<CourseDTO>;
export type CourseItem = KeysToCamelCase<CourseItemDTO>;
export type Career = KeysToCamelCase<CareerDTO>;
export type Job = KeysToCamelCase<JobDTO>;
export type CourseParams = KeysToCamelCase<CourseParamsDTO>;
export type SkillParams = KeysToCamelCase<SkillParamsDTO>;
