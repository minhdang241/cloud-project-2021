import {
  CareerDTO,
  CareerOptionDTO,
  CountDTO,
  CourseDTO,
  CourseLevelDTO,
  CourseParamsDTO,
  JobDistrictDTO,
  JobDTO,
  KeysToCamelCase,
  RequestDTO,
  SkillDTO,
  WordFreqDTO,
  WordFrquenciesDTO,
} from "./DTO";

export type Routes = {
  path: string;
  name: string;
  icon?: string;
  component: (props: any) => JSX.Element;
};
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
export type WordFreq = KeysToCamelCase<WordFreqDTO>;
export type WordFrquencies = KeysToCamelCase<WordFrquenciesDTO>;
export type JobDistrict = KeysToCamelCase<JobDistrictDTO>;
export type Request = KeysToCamelCase<RequestDTO>;
export type Count = KeysToCamelCase<CountDTO>;
