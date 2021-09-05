import { useState } from "react";
import Pagination from "react-js-pagination";

// reactstrap components
import {
  Card,
  CardHeader,
  CardBody,
  CardTitle,
  CardFooter,
  Table,
  Row,
  Col,
  Dropdown,
  DropdownToggle,
  DropdownMenu,
  DropdownItem,
  Button,
  Label,
  Input,
  FormGroup,
} from "reactstrap";

function Tables() {
  const [dropdownOpen, setDropdownOpen] = useState(false);
  const [page, setPage] = useState<number>(1);
  const [added, setAdded] = useState<boolean>(false);
  const dropdownToggle = (e: any) => {
    setDropdownOpen(!dropdownOpen);
  };

  return (
    <div className="content">
      <Row className="align-items-center mb-2">
        <Col md="6">
          <form>
            <div className="no-border input-group mb-0">
              <input placeholder="Search course name" type="text" className="form-control" />
              {/* <div className="input-group-append">
                <span className="input-group-text">
                  <i className="nc-icon nc-zoom-split"></i>
                </span>
              </div> */}
            </div>
          </form>
        </Col>
        <Col md="4">
          <div className="d-flex">
            <Button className="mr-3">Search</Button>
            <Dropdown isOpen={dropdownOpen} toggle={(e: any) => dropdownToggle(e)}>
              <DropdownToggle caret>All majors&nbsp;&nbsp;</DropdownToggle>
              <DropdownMenu right>
                <DropdownItem>Information Technology</DropdownItem>
                <DropdownItem>Software Engineering</DropdownItem>
                <DropdownItem>Electrical Engineering</DropdownItem>
                <DropdownItem>Robotics</DropdownItem>
              </DropdownMenu>
            </Dropdown>
          </div>
        </Col>
      </Row>
      <Row>
        <Col md="9">
          <Card>
            <CardHeader>
              <CardTitle tag="h5" className="mb-0">
                Course Table
              </CardTitle>
            </CardHeader>
            <CardBody>
              <Table responsive>
                <thead className="text-primary">
                  <tr>
                    <th></th>
                    <th>Course ID</th>
                    <th>Course Name</th>
                    <th>Major</th>
                    <th className="text-right">Credits</th>
                  </tr>
                </thead>
                <tbody>
                  <tr>
                    <td>
                      <Button
                        size="sm"
                        color={added ? "danger" : "warning"}
                        className="p-1"
                        onClick={() => setAdded(!added)}
                      >
                        {!added ? <i className="fas fa-lg fa-plus"></i> : <i className="fas fa-lg fa-minus"></i>}
                      </Button>
                    </td>
                    <td>Dakota Rice</td>
                    <td>Niger</td>
                    <td>Oud-Turnhout</td>
                    <td className="text-right">$36,738</td>
                  </tr>
                </tbody>
              </Table>
              <div className="d-flex justify-content-end">
                <Pagination
                  activePage={page}
                  totalItemsCount={10}
                  pageRangeDisplayed={5}
                  onChange={(pageNumber) => setPage(pageNumber)}
                  itemClass="page-item"
                  linkClass="page-link"
                />
              </div>
            </CardBody>
          </Card>
        </Col>
        <Col>
          <Card>
            <CardHeader>
              <CardTitle className="mb-0" tag="h5">
                Selected Courses
              </CardTitle>
            </CardHeader>
            <CardBody>
              <div className="selected-course">
                <div>Cloud Computing</div>
                <i role="button" className="fas fa-lg fa-times text-gray" onClick={() => setAdded(false)}></i>
              </div>
            </CardBody>
            <CardFooter>
              <div className="d-flex justify-content-end border-top pt-2">
                <Button color="primary">Get recommendation</Button>
              </div>
            </CardFooter>
          </Card>
        </Col>
      </Row>
      <Card>
        <CardHeader>
          <CardTitle className="mb-0" tag="h5">
            Career Path
          </CardTitle>
        </CardHeader>
        <CardBody>
          <Table responsive>
            <thead className="text-primary">
              <tr>
                <th>Job Name</th>
                <th>Desciption</th>
                <th>Company</th>
                <th>Salary</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td>Dakota Rice</td>
                <td>Niger</td>
                <td>Oud-Turnhout</td>
                <td>$36,738</td>
              </tr>
            </tbody>
          </Table>
        </CardBody>
      </Card>
    </div>
  );
}

export default Tables;
