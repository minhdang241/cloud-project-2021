import {
  CareerDTO,
  CareerOptionDTO,
  CourseDTO,
  CourseItemDTO,
  CourseLevelDTO,
  CourseParamsDTO,
  JobDTO,
  KeysToCamelCase,
  SkillDTO,
  SkillParamsDTO,
} from "./DTO";

export interface Dictionary<T> {
  [Key: string]: T;
}

export type Course = KeysToCamelCase<CourseDTO>;
export type CourseItem = KeysToCamelCase<CourseItemDTO>;
export type Career = KeysToCamelCase<CareerDTO>;
export type CareerOption = KeysToCamelCase<CareerOptionDTO>;
export type Job = KeysToCamelCase<JobDTO>;
export type CourseParams = KeysToCamelCase<CourseParamsDTO>;
export type SkillParams = KeysToCamelCase<SkillParamsDTO>;
export type Skill = KeysToCamelCase<SkillDTO>;
export type CourseLevel = KeysToCamelCase<CourseLevelDTO>;
