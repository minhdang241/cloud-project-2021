import { BrowserRouter, Route, Switch, Redirect } from "react-router-dom";
import "bootstrap/dist/css/bootstrap.css";
import "assets/scss/paper-dashboard.scss?v=1.3.0";
import "perfect-scrollbar/css/perfect-scrollbar.css";
import Amplify, { Auth } from "aws-amplify";
import React, { createContext, useEffect, useState } from "react";
import { AWS_CONFIG } from "./utils/constants";
import { withAuthenticator } from "@aws-amplify/ui-react";

import DemoNavbar from "components/layouts/DemoNavbar";
import Footer from "components/layouts/Footer";
import Sidebar from "components/layouts/Sidebar";
import { Routes } from "utils/Types";
import PrivateRoute from "utils/PrivateRoute";

import { adminRoutes, userRoutes } from "utils/routes";

Amplify.configure(AWS_CONFIG);

interface UserContextProps {
  role?: string;
  token?: string;
  username?: string;
  clientId?: string;
}

export const UserContext = createContext<UserContextProps>({});

function App() {
  // TODO save user info to redux, refer to the documentation below
  // https://aws-amplify.github.io/amplify-js/api/classes/authclass.html
  // const [authState, setAuthState] = React.useState();
  // const [user, setUser] = React.useState();
  //

  const [profile, setProfile] = useState<UserContextProps>();
  const [routes, setRoutes] = useState<Routes[]>([]);

  React.useEffect(() => {
    Auth.currentSession()
      .then((data) => {
        const group = data.getAccessToken().payload["cognito:groups"];
        let myRole = "";
        if (group) {
          myRole = group[0];
        } else {
          myRole = "user";
        }

        setProfile({
          role: myRole,
          token: data.getAccessToken().getJwtToken(),
          username: data.getAccessToken().payload["username"],
          clientId: data.getAccessToken().payload["client_id"],
        });
      })
      .catch((err) => console.log(err));
  }, []);

  useEffect(() => {
    const allRoutes: Routes[] = profile?.role == "admin" ? adminRoutes : userRoutes;
    setRoutes(allRoutes);
  }, [profile]);

  return (
    <div>
      <div className="App">
        <BrowserRouter>
          <Switch>
            <Route
              path="/"
              render={(props) => (
                <UserContext.Provider
                  value={{
                    role: profile?.role,
                    token: profile?.token,
                    clientId: profile?.clientId,
                    username: profile?.username,
                  }}
                >
                  <div className="wrapper">
                    <Sidebar routes={routes} bgColor="black" activeColor="warning" {...props} />
                    <div className="main-panel">
                      <DemoNavbar routes={routes} {...props} />
                      <Switch>
                        {routes.map((prop, key) => {
                          return <PrivateRoute path={prop.path} component={prop.component} key={key} />;
                        })}
                        {profile !== undefined && <Redirect from="*" to="/career" />}
                      </Switch>
                      <Footer fluid />
                    </div>
                  </div>
                </UserContext.Provider>
              )}
            />
            <Redirect to="/career" />
          </Switch>
        </BrowserRouter>
      </div>
    </div>
  );
}

export default withAuthenticator(App);
// export default App;
