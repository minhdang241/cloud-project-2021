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
import { getAllCourses, getRecommendCareer } from "services/courseService";
import { CareerDTO, CourseDTO } from "utils/DTO";
import { keysToCamel } from "utils/functions";
import { Career, Course, Job } from "utils/Types";
import CourseDetails from "components/Recommend/CourseDetails";
function Tables() {
  const [dropdownOpen, setDropdownOpen] = useState(false);
  const [page, setPage] = useState<number>(1);
  const [jobPage, setJobPage] = useState<number>(1);
  const [courses, setCourses] = useState<Course[]>([]);
  const [selectedCourses, setSelectedCourses] = useState<Course[]>([]);

  const [paths, setPaths] = useState<Career[]>([]);
  const [jobs, setJobs] = useState<Job[]>([]);
  const [loading, setLoading] = useState<string>("");
  const dropdownToggle = (e: any) => {
    setDropdownOpen(!dropdownOpen);
  };

  useEffect(() => {
    (async () => {
      try {
        setLoading("courses");
        const { data } = await getAllCourses(page, 10);
        const tempCourses: Course[] = keysToCamel(data.items as CourseDTO);
        setCourses(tempCourses);
      } catch (error) {
        console.error(error);
      } finally {
        setLoading("");
      }
    })();
  }, [page]);

  const updateSelectedCourses = (course: Course) => {
    if (selectedCourses.includes(course)) {
      const tmp: Course[] = selectedCourses.filter((c) => c.id !== course.id);
      setSelectedCourses(tmp);
    } else setSelectedCourses([...selectedCourses, course]);
  };

  const handleGetRecCareer = async () => {
    try {
      setLoading("career");
      setJobs([]);
      const coursesId: number[] = selectedCourses.map((c) => c.id);
      const { data } = await getRecommendCareer(coursesId);
      const tmp: Career[] = keysToCamel(data.career_list as CareerDTO);
      setPaths(tmp);
    } catch (error) {
      console.error(error);
    } finally {
      setLoading("");
    }
  };

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
        <Col sm="12" xl="9">
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
                  {loading === "courses" ? (
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
                  ) : courses.length == 0 ? (
                    <tr>
                      <td colSpan={4} className="text-muted">
                        No course available
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
                            color={selectedCourses.includes(course) ? "danger" : "warning"}
                            className="p-1 ml-3"
                            onClick={() => updateSelectedCourses(course)}
                          >
                            {selectedCourses.includes(course) ? (
                              <i className="fas fa-lg fa-minus"></i>
                            ) : (
                              <i className="fas fa-lg fa-plus"></i>
                            )}
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
                    totalItemsCount={courses.length}
                    pageRangeDisplayed={5}
                    onChange={(pageNumber) => setPage(pageNumber)}
                    itemClass="page-item-ow"
                    linkClass="page-link-ow"
                  />
                </div>
              )}
            </CardBody>
          </Card>
        </Col>
        <Col sm="12" xl="3">
          <Card className="card-stretch">
            <CardHeader>
              <CardTitle className="mb-0" tag="h5">
                Selected Courses
              </CardTitle>
            </CardHeader>
            <CardBody>
              {selectedCourses.length == 0 ? (
                <div className="text-muted">No course selected</div>
              ) : (
                selectedCourses.map((course) => (
                  <div key={course.id} className="selected-course">
                    <div>{course.title}</div>
                    <i
                      role="button"
                      className="fas fa-lg fa-times text-gray"
                      onClick={() => updateSelectedCourses(course)}
                    ></i>
                  </div>
                ))
              )}
            </CardBody>
            <CardFooter>
              <div className="d-flex justify-content-end border-top pt-2">
                <Button
                  disabled={!selectedCourses[0]}
                  color="primary"
                  onClick={() => setSelectedCourses([])}
                  className="mr-3"
                >
                  Clear
                </Button>
                <Button
                  disabled={!selectedCourses[0] || loading == "career"}
                  color="primary"
                  onClick={handleGetRecCareer}
                >
                  Get Path
                </Button>
              </div>
            </CardFooter>
          </Card>
        </Col>
      </Row>
      <Row>
        <Col sm="3">
          <Card Card className="card-stretch">
            <CardHeader>
              <CardTitle className="mb-0" tag="h5">
                Career Path
              </CardTitle>
            </CardHeader>
            <CardBody>
              {loading == "career" ? (
                <div className="text-center py-5">
                  <Spinner
                    color="warning"
                    style={{
                      width: "2rem",
                      height: "2rem",
                    }}
                  />
                </div>
              ) : paths.length == 0 ? (
                <div className="text-muted">No recommendation</div>
              ) : (
                paths.map((path, id) => (
                  <div key={id} className="selected-course" onClick={() => setJobs(path.jobList)}>
                    <div role="button">{path.career}</div>
                  </div>
                ))
              )}
            </CardBody>
          </Card>
        </Col>
        <Col sm="12" xl="9">
          <Card>
            <CardHeader>
              <CardTitle tag="h5" className="mb-0">
                Practical jobs
              </CardTitle>
            </CardHeader>
            <CardBody>
              <Table responsive>
                <thead className="text-primary">
                  <tr>
                    <th>Title</th>
                    <th>Company</th>
                    <th>Location</th>
                    <th>Description</th>
                    <th>Link</th>
                  </tr>
                </thead>
                <tbody>
                  {jobs.length == 0 ? (
                    <tr>
                      <td colSpan={5} className="text-muted">
                        No path selected
                      </td>
                    </tr>
                  ) : (
                    jobs.slice((jobPage - 1) * 10, jobPage * 10).map((job, id) => (
                      <tr key={id}>
                        <td>{job.title}</td>
                        <td>{job.companyName}</td>
                        <td>{job.companyLocation}</td>
                        <td title={job.shortDescription}>{job.shortDescription.slice(0, 50)}...</td>
                        <td>
                          <a href={job.link} target="_blank" rel="noreferrer">
                            View
                          </a>
                        </td>
                      </tr>
                    ))
                  )}
                </tbody>
              </Table>
              {jobs.length > 10 && (
                <div className="d-flex justify-content-end">
                  <Pagination
                    activePage={jobPage}
                    totalItemsCount={jobs.length}
                    pageRangeDisplayed={5}
                    onChange={(pageNumber) => setJobPage(pageNumber)}
                    itemClass="page-item-ow"
                    linkClass="page-link-ow"
                  />
                </div>
              )}
            </CardBody>
          </Card>
        </Col>
      </Row>
    </div>
  );
}

export default Tables;
