import Dashboard from "views/Dashboard";
import CareerPath from "views/Career";
import UserPage from "views/User";
import StudyPath from "views/Study";
import RecommendView from "views/RecommendView";
import { Routes } from "./Types";

export const userRoutes: Routes[] = [
  {
    path: "/user-page",
    name: "User Profile",
    icon: "nc-icon nc-single-02",
    component: UserPage,
  },
  {
    path: "/career",
    name: "Career Path",
    icon: "nc-icon nc-briefcase-24",
    component: CareerPath,
  },
  {
    path: "/recommend",
    name: "Study Path",
    icon: "nc-icon nc-book-bookmark",
    component: RecommendView,
  },
  {
    path: "/study",
    name: "Skill Analysis",
    icon: "nc-icon nc-ruler-pencil",
    component: StudyPath,
  },
];

export const adminRoutes: Routes[] = [
  {
    path: "/dashboard",
    name: "Dashboard",
    icon: "nc-icon nc-bank",
    component: Dashboard,
  },
  ...userRoutes,
];
