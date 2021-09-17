import { BrowserRouter, Route, Switch, Redirect } from "react-router-dom";
import "bootstrap/dist/css/bootstrap.css";
import "assets/scss/paper-dashboard.scss?v=1.3.0";
import "perfect-scrollbar/css/perfect-scrollbar.css";
import AdminLayout from "./components/layouts/Admin";
import Amplify from "aws-amplify";
import React from "react";
import { AWS_CONFIG } from "./utils/constants";
import { withAuthenticator } from "@aws-amplify/ui-react";
import { AuthState, onAuthUIStateChange } from "@aws-amplify/ui-components";

Amplify.configure(AWS_CONFIG);

Amplify.configure();

function App() {
  console.log("here", AWS_CONFIG);
  // TODO save user info to redux, refer to the documentation below
  // https://aws-amplify.github.io/amplify-js/api/classes/authclass.html
  // IMPORTANT: to determine whether the user is an admin, we must decode the Access Token (stored in local storage or in the authData below)
  //  the admin user has the attribute call cognito:group =  ["admin"]
  // const [authState, setAuthState] = React.useState();
  // const [user, setUser] = React.useState();
  //
  React.useEffect(() => {
    return onAuthUIStateChange((nextAuthState, authData) => {
      console.log(nextAuthState);
      console.log(authData);
    });
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
