import Dashboard from "views/Dashboard";
import CareerPath from "views/Career";
import UserPage from "views/User";
import StudyPath from "views/Study";

const routes = [
  {
    path: "/dashboard",
    name: "Dashboard",
    icon: "nc-icon nc-bank",
    component: Dashboard,
    layout: "/admin",
  },
  {
    path: "/user-page",
    name: "User Profile",
    icon: "nc-icon nc-single-02",
    component: UserPage,
    layout: "/admin",
  },
  {
    path: "/career",
    name: "Career Path",
    icon: "nc-icon nc-briefcase-24",
    component: CareerPath,
    layout: "/admin",
  },
  {
    path: "/study",
    name: "Study Path",
    icon: "nc-icon nc-ruler-pencil",
    component: StudyPath,
    layout: "/admin",
  },
];
export default routes;
