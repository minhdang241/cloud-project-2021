import { CareerDTO, CourseDTO, JobDTO, KeysToCamelCase } from "./DTO";

export interface Dictionary<T> {
  [Key: string]: T;
}

export type Course = KeysToCamelCase<CourseDTO>;
export type Career = KeysToCamelCase<CareerDTO>;
export type Job = KeysToCamelCase<JobDTO>;
