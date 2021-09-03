import Dashboard from "views/Dashboard";
import TableList from "views/Tables";
import UserPage from "views/User";

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
    path: "/tables",
    name: "Recommendation",
    icon: "nc-icon nc-tile-56",
    component: TableList,
    layout: "/admin",
  },
];
export default routes;
