import { useContext } from "react";
import { Card, CardBody, Row, Col } from "reactstrap";
import { UserContext } from "App";
function User() {
  const { username } = useContext(UserContext);

  const cognito = `CognitoIdentityServiceProvider.1tlmnlptbkmipvrut7fls2fl7e.${username}.userData`;
  const TOKEN = localStorage.getItem(cognito);
  const userData: any = JSON.parse(TOKEN || "");
  console.log(userData);

  return (
    <>
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
    </>
  );
}

export default User;
