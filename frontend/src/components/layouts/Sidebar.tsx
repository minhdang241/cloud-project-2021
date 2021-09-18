import React from "react";
import { NavLink } from "react-router-dom";
import { Nav, NavItem } from "reactstrap";
import { Auth } from "aws-amplify";

let ps: any;

async function signOut() {
  try {
    await Auth.signOut();
    window.location.reload();
  } catch (error) {
    alert("unexpected error");
  }
}

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
          <li>
            <NavItem className="nav-link" activeClassName="active" onClick={signOut}>
              <i className="nc-icon nc-user-run" />
              <p>Logout</p>
            </NavItem>
          </li>
        </Nav>
      </div>
    </div>
  );
}

export default Sidebar;
