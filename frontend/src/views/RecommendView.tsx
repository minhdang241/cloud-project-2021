import React, { useState, useEffect } from "react";
import Pagination from "react-js-pagination";
import SortHeader, { Sort } from "components/Path/SortHeader";
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
import { getAllCourses, getJobsByCareer } from "services/careerService";
import { getAllCareers, getCoursesByCareer } from "services/studyService";
import { CareerDTO, CourseDTO, CareerOptionDTO, JobDTO } from "utils/DTO";
import { keysToCamel } from "utils/functions";
import { Career, Course, Job, CareerOption } from "utils/Types";
import CourseDetails from "components/Path/CourseDetails";
import useDebounce from "utils/useDebounce";

function RecommendView() {
  const [page, setPage] = useState<number>(1);
  const [total, setTotal] = useState<number>(0);

  const [totalJob, setTotalJob] = useState<number>(0);
  const [jobPage, setJobPage] = useState<number>(1);

  const [careers, setCareers] = useState<CareerOption[]>([]);
  const [selectedCareer, setSelectedCareer] = useState<CareerOption>();
  const [courses, setCourses] = useState<Course[]>([]);
  const [jobs, setJobs] = useState<Job[]>([]);

  const [loading, setLoading] = useState<string>("");
  const [loadingCourse, setLoadingCourse] = useState<boolean>(false);

  useEffect(() => {
    (async () => {
      try {
        // Load career
        setLoading("career");
        const { data: careerData } = await getAllCareers();
        const tmpCareerOptions: CareerOption[] = keysToCamel(careerData.items as CareerOptionDTO);
        setCareers(tmpCareerOptions);
      } catch (error) {
        console.error(error);
      } finally {
        setLoading("");
      }
    })();
  }, []);

  useEffect(() => {
    console.log(selectedCareer);
    if (!selectedCareer || loading == "jobs") {
      return;
    }
    (async () => {
      try {
        setLoading("jobs");
        const { data } = await getJobsByCareer(selectedCareer?.id || 0, page, 10);
        const tempJobs: Job[] = keysToCamel(data.items as JobDTO);
        setJobs(tempJobs);
        setTotalJob(data.total);
      } catch (error) {
        console.error(error);
      } finally {
        setLoading("");
      }
    })();
  }, [jobPage, selectedCareer]);

  useEffect(() => {
    console.log(selectedCareer);
    if (!selectedCareer || loadingCourse) {
      return;
    }
    (async () => {
      try {
        setLoadingCourse(true);
        const { data } = await getCoursesByCareer(selectedCareer.id, page, 10);
        const tmp: Course[] = keysToCamel(data.items as CourseDTO);
        setCourses(tmp);
        setTotal(data.total);
      } catch (error) {
        console.error(error);
      } finally {
        setLoadingCourse(false);
      }
    })();
  }, [page, selectedCareer]);

  return (
    <div className="content">
      <Row>
        <Col sm="12" xl="3">
          <Card className="card-stretch">
            <CardHeader>
              <CardTitle className="mb-0" tag="h5">
                Career Table
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
              ) : careers.length == 0 ? (
                <div className="text-muted">No career available</div>
              ) : (
                careers.map((career) => (
                  <div key={career.id} className="selected-course" onClick={() => setSelectedCareer(career)}>
                    <div role="button">{career.careerPath}</div>
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
                  {loading === "job" ? (
                    <tr>
                      <td colSpan={5} className="text-center py-5">
                        <Spinner
                          color="warning"
                          style={{
                            width: "3rem",
                            height: "3rem",
                          }}
                        />
                      </td>
                    </tr>
                  ) : jobs.length == 0 ? (
                    <tr>
                      <td colSpan={5} className="text-muted">
                        No job available
                      </td>
                    </tr>
                  ) : (
                    jobs.map((job, id) => (
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
              {totalJob > 10 && (
                <div className="d-flex justify-content-end">
                  <Pagination
                    activePage={jobPage}
                    totalItemsCount={totalJob}
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
      <Row>
        <Col sm="12">
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
                    <th>Action</th>
                  </tr>
                </thead>
                <tbody>
                  {loadingCourse ? (
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
                        </td>
                      </tr>
                    ))
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
      </Row>
    </div>
  );
}

export default RecommendView;
