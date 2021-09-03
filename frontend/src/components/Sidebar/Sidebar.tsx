import React from "react";
import { NavLink } from "react-router-dom";
import { Nav } from "reactstrap";
// javascript plugin used to create scrollbars on windows
import PerfectScrollbar from "perfect-scrollbar";
import logo from "logo.svg";

let ps: any;

function Sidebar(props: any) {
  const sidebar = React.useRef<HTMLDivElement>(null); //React.useRef();
  // verifies if routeName is the one active (in browser input)
  const activeRoute = (routeName: any) => {
    return props.location.pathname.indexOf(routeName) > -1 ? "active" : "";
  };
  return (
    <div className="sidebar" data-color={props.bgColor} data-active-color={props.activeColor}>
      <div className="sidebar-wrapper" ref={sidebar}>
        <Nav>
          {props.routes.map((prop: any, key: any) => {
            return (
              <li className={activeRoute(prop.path) + (prop.pro ? " active-pro" : "")} key={key}>
                <NavLink to={prop.layout + prop.path} className="nav-link" activeClassName="active">
                  <i className={prop.icon} />
                  <p>{prop.name}</p>
                </NavLink>
              </li>
            );
          })}
        </Nav>
      </div>
    </div>
  );
}

export default Sidebar;
