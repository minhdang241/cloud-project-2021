import { CourseDTO, KeysToCamelCase } from "./DTO";

export interface Dictionary<T> {
  [Key: string]: T;
}

export type Course = KeysToCamelCase<CourseDTO>;
