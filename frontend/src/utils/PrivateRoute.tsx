import * as React from "react";
import { Route, Redirect, RouteComponentProps } from "react-router-dom";
import type { RouteProps } from "react-router-dom";
import { UserContext } from "App";

interface PrivateRouteParams extends RouteProps {
  component: React.ComponentType<RouteComponentProps<any>> | React.ComponentType<any>;
}

const PrivateRoute = ({ component: Component, ...rest }: PrivateRouteParams) => {
  const { role } = React.useContext(UserContext);

  return role !== undefined ? <Route {...rest} render={(props) => <Component {...props} />} /> : null;
};

export default PrivateRoute;
