import { BrowserRouter, Route, Switch, Redirect } from "react-router-dom";
import "bootstrap/dist/css/bootstrap.css";
import "assets/scss/paper-dashboard.scss?v=1.3.0";
import "perfect-scrollbar/css/perfect-scrollbar.css";
import AdminLayout from "./components/layouts/Admin";
import Amplify, { Auth } from "aws-amplify";
import React from "react";
import { AWS_CONFIG } from "./utils/constants";
import { withAuthenticator } from "@aws-amplify/ui-react";

Amplify.configure(AWS_CONFIG);

function App() {
  // TODO save user info to redux, refer to the documentation below
  // https://aws-amplify.github.io/amplify-js/api/classes/authclass.html
  // const [authState, setAuthState] = React.useState();
  // const [user, setUser] = React.useState();
  //
  React.useEffect(() => {
    Auth.currentSession()
      .then((data) => {
        const group = data.getAccessToken().payload["cognito:groups"];
        let role = "";
        if (group) {
          role = group[0];
        } else {
          role = "user";
        }
        console.log(role);
      })
      .catch((err) => console.log(err));
  }, []);

  return (
    <div>
      <div className="App">
        <BrowserRouter>
          <Switch>
            <Route path="/admin" render={(props) => <AdminLayout {...props} />} />
            <Redirect to="/admin/career" />
          </Switch>
        </BrowserRouter>
      </div>
    </div>
  );
}

export default withAuthenticator(App);
