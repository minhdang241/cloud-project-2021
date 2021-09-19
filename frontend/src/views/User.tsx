import { useContext, useState, useEffect } from "react";
import { Card, CardBody, Row, Col } from "reactstrap";
import { UserContext } from "App";
import { AWS_CONFIG } from "utils/constants";

function User() {
  const { username } = useContext(UserContext);
  const [userData, setUserData] = useState<any>();

  useEffect(() => {
    if (username) {
      const cognito = `CognitoIdentityServiceProvider.${AWS_CONFIG.aws_user_pools_web_client_id}.${username}.userData`;
      const TOKEN = localStorage.getItem(cognito);
      setUserData(JSON.parse(TOKEN || ""));
    }
  }, [username]);

  return (
    <>
      {userData && (
        <div className="content">
          <Row>
            <Col sm={{ size: 4, offset: 4 }}>
              <Card className="card-user">
                <div className="image">
                  <img alt="..." src={require("assets/img/damir-bosnjak.jpg").default} />
                </div>
                <CardBody>
                  <div className="author">
                    <a href="#pablo" onClick={(e) => e.preventDefault()}>
                      <img
                        alt="..."
                        className="avatar border-gray"
                        src={require("assets/img/damir-bosnjak.jpg").default}
                      />
                      <h5 className="title">{userData.Username}</h5>
                    </a>
                  </div>
                  <p className="description text-center">
                    <i className="fas fa-phone mr-3"></i>
                    {userData.UserAttributes[3].Value}
                    <br />
                    <i className="fas fa-envelope mr-3"></i> {userData.UserAttributes[4].Value}
                  </p>
                </CardBody>
              </Card>
            </Col>
          </Row>
        </div>
      )}
    </>
  );
}

export default User;
