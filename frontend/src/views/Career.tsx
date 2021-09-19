import React, { useState, useEffect, useContext } from "react";
import Pagination from "react-js-pagination";

// reactstrap components
import { Card, CardHeader, CardBody, CardTitle, CardFooter, Table, Row, Col, Button, Spinner } from "reactstrap";
import { getAllCourses, getRecommendCareer } from "services/careerService";
import { CareerDTO, CourseDTO } from "utils/DTO";
import { keysToCamel } from "utils/functions";
import { Career, Course, Job } from "utils/Types";
import CourseDetails from "components/Path/CourseDetails";
import useDebounce from "utils/useDebounce";
import SortHeader, { Sort } from "components/Path/SortHeader";
import { UserContext } from "App";

function Tables() {
  const { username } = useContext(UserContext);

  const [dropdownOpen, setDropdownOpen] = useState(false);
  const [page, setPage] = useState<number>(1);
  const [total, setTotal] = useState<number>(0);
  const [jobPage, setJobPage] = useState<number>(1);

  const [sort, setSort] = useState<Sort>({ by: "", order: "" });
  const [search, setSearch] = useState<string>("");
  const [isSearch, setIsSearch] = useState<boolean>(false);
  const [clear, setClear] = useState<boolean>(false);
  const debounceSort = useDebounce(sort);
  const [courses, setCourses] = useState<Course[]>([]);
  const [selectedCourses, setSelectedCourses] = useState<Course[]>([]);

  const [paths, setPaths] = useState<Career[]>([]);
  const [jobs, setJobs] = useState<Job[]>([]);
  const [loading, setLoading] = useState<string>("");

  useEffect(() => {
    if (isSearch) {
      setIsSearch(false);
      return;
    }
    (async () => {
      try {
        setLoading("courses");
        const { data } = await getAllCourses(username || "", page, 10, sort.by, sort.order, search);
        const tempCourses: Course[] = keysToCamel(data.items as CourseDTO);
        setCourses(tempCourses);
        setTotal(data.total);
      } catch (error) {
        console.error(error);
      } finally {
        setLoading("");
      }
    })();
  }, [page, debounceSort]);

  const updateSelectedCourses = (course: Course, remove: boolean) => {
    if (remove) {
      const tmp: Course[] = selectedCourses.filter((c) => c.id !== course.id);
      setSelectedCourses(tmp);
    } else setSelectedCourses([...selectedCourses, course]);
  };

  const handleGetRecCareer = async () => {
    try {
      setLoading("career");
      setJobs([]);
      const coursesId: number[] = selectedCourses.map((c) => {
        return c.id;
      });
      const { data } = await getRecommendCareer(username || "", coursesId);
      const tmp: Career[] = keysToCamel(data.career_list as CareerDTO);
      setPaths(tmp);
    } catch (error) {
      console.error(error);
    } finally {
      setLoading("");
    }
  };

  const isSelected = (id: number): boolean => {
    if (selectedCourses.findIndex((c) => c.id == id) > -1) {
      return true;
    }
    return false;
  };

  const onSearchCourse = async (reset?: boolean) => {
    setIsSearch(page !== 1);
    setClear(!reset);
    try {
      setLoading("courses");
      const { data } = await getAllCourses(username || "", 1, 10, sort.by, sort.order, reset ? "" : search);
      const tempCourses: Course[] = keysToCamel(data.items as CourseDTO);
      setCourses(tempCourses);
      setTotal(data.total);
    } catch (error) {
      console.error(error);
    } finally {
      setLoading("");
      setPage(1);
    }
  };

  return (
    <div className="content">
      <Row className="align-items-center mb-2">
        <Col md="6">
          <form
            onSubmit={(e) => {
              e.preventDefault();
              onSearchCourse();
            }}
          >
            <div className="no-border input-group mb-0">
              <input
                placeholder="Search course title"
                type="text"
                className="form-control"
                value={search}
                onChange={(e) => setSearch(e.target.value)}
              />
              {clear && (
                <div className="input-group-append">
                  <span className="input-group-text">
                    <i
                      role="button"
                      className="fas fa-lg fa-times"
                      onClick={() => {
                        setClear(false);
                        setSearch("");
                        onSearchCourse(true);
                      }}
                    />
                  </span>
                </div>
              )}
            </div>
          </form>
        </Col>
        <Col md="4">
          <div className="d-flex">
            <Button className="mr-3" onClick={() => onSearchCourse()}>
              Search
            </Button>
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
                  <SortHeader headers={["code", "title", "level", "action"]} sort={sort} setSort={setSort} />
                </thead>
                <tbody>
                  {loading === "courses" ? (
                    <tr>
                      <td colSpan={4} className="text-center py-9">
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
                    courses.map((course) => {
                      const selected: boolean = isSelected(course.id);
                      return (
                        <tr key={course.id}>
                          <td>{course.code}</td>
                          <td>{course.title}</td>
                          <td>{course.level === "ADVANCED" ? "Advanced" : "Basic"}</td>
                          <td>
                            <CourseDetails course={course} />
                            <Button
                              title="Select course"
                              size="sm"
                              color={selected ? "danger" : "warning"}
                              className="p-1 ml-sm-1 ml-lg-2"
                              onClick={() => updateSelectedCourses(course, selected)}
                            >
                              {selected ? (
                                <i className="fas fa-lg fa-minus"></i>
                              ) : (
                                <i className="fas fa-lg fa-plus"></i>
                              )}
                            </Button>
                          </td>
                        </tr>
                      );
                    })
                  )}
                </tbody>
              </Table>
              {total > 10 && (
                <div className="d-flex justify-content-end">
                  <Pagination
                    activePage={page}
                    totalItemsCount={total}
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
                      onClick={() => updateSelectedCourses(course, true)}
                    ></i>
                  </div>
                ))
              )}
            </CardBody>
            <CardFooter>
              <div className="d-flex justify-content-end justify-content-xl-around border-top pt-2">
                <Button
                  disabled={!selectedCourses[0]}
                  color="primary"
                  onClick={() => setSelectedCourses([])}
                  className="mr-3 m-xl-0"
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
        <Col sm="12" xl="3">
          <Card className="card-stretch">
            <CardHeader>
              <CardTitle className="mb-0" tag="h5">
                Career Path
              </CardTitle>
            </CardHeader>
            <CardBody>
              {loading == "career" ? (
                <div className="text-center py-9">
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
                  <div role="button" key={id} className="selected-course" onClick={() => setJobs(path.jobList)}>
                    <div>{path.career}</div>
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
                    <th>Action</th>
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
                          <Button
                            title="Hiring post"
                            size="sm"
                            color="warning"
                            className="p-1 ml-sm-1 ml-lg-2"
                            onClick={() => window.open(job.link, "_blank")?.focus()}
                          >
                            <i className="fas fa-lg fa-external-link-alt"></i>
                          </Button>
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
