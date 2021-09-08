import { useState, useEffect } from "react";
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
  Spinner,
} from "reactstrap";
import { getAllCourses } from "services/courseService";
import { CourseDTO } from "utils/DTO";
import { keysToCamel } from "utils/functions";
import { Course } from "utils/Types";
import CourseDetails from "components/Recommend/CourseDetails";
function Tables() {
  const [dropdownOpen, setDropdownOpen] = useState(false);
  const [page, setPage] = useState<number>(1);
  const [added, setAdded] = useState<boolean>(false);

  const [courses, setCourses] = useState<Course[]>([]);
  const [loading, setLoading] = useState<boolean>(false);
  const dropdownToggle = (e: any) => {
    setDropdownOpen(!dropdownOpen);
  };

  useEffect(() => {
    (async () => {
      try {
        setLoading(true);
        const { data } = await getAllCourses(page, 10);
        const tempCourses: Course[] = keysToCamel(data.items as CourseDTO);
        setCourses(tempCourses);
      } catch (error) {
        console.error(error);
      } finally {
        setLoading(false);
      }
    })();
  }, [page]);

  return (
    <div className="content">
      <Row className="align-items-center mb-2">
        <Col md="6">
          <form>
            <div className="no-border input-group mb-0">
              <input placeholder="Search course name" type="text" className="form-control" />
            </div>
          </form>
        </Col>
        <Col md="4">
          <div className="d-flex">
            <Button className="mr-3">Search</Button>
            <Dropdown isOpen={dropdownOpen} toggle={(e: any) => dropdownToggle(e)}>
              <DropdownToggle caret>All levels&nbsp;&nbsp;</DropdownToggle>
              <DropdownMenu right>
                <DropdownItem>Basic</DropdownItem>
                <DropdownItem>Advanced</DropdownItem>
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
                    <th>Code</th>
                    <th>Title</th>
                    <th>Levels</th>
                    <th>Actions</th>
                  </tr>
                </thead>
                <tbody>
                  {loading ? (
                    <tr>
                      <td colSpan={4} className="text-center py-5">
                        <Spinner
                          color="warning"
                          style={{
                            width: "3rem",
                            height: "3rem",
                          }}
                        />
                      </td>
                    </tr>
                  ) : (
                    courses.map((course) => (
                      <tr key={course.id}>
                        <td>{course.code}</td>
                        <td>{course.title}</td>
                        <td>{course.level === "ADVANCED" ? "Advanced" : "Basic"}</td>
                        <td>
                          <CourseDetails course={course} />
                          <Button
                            title="Select course"
                            size="sm"
                            color={added ? "danger" : "warning"}
                            className="p-1 ml-3"
                            onClick={() => setAdded(!added)}
                          >
                            {!added ? <i className="fas fa-lg fa-plus"></i> : <i className="fas fa-lg fa-minus"></i>}
                          </Button>
                        </td>
                      </tr>
                    ))
                  )}
                </tbody>
              </Table>
              {courses.length > 10 && (
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
              )}
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
