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
import { getAllCareers, getCoursesByCareer, getSkills } from "services/studyService";
import { CareerDTO, CareerOptionDTO, CourseDTO, SkillDTO } from "utils/DTO";
import { keysToCamel } from "utils/functions";
import { Career, CareerOption, Course, CourseItem, Job, Skill } from "utils/Types";
import CourseDetails from "components/Path/CourseDetails";

function StudyPath() {
  const [dropdownOpen, setDropdownOpen] = useState(false);
  const [page, setPage] = useState<number>(1);
  const [total, setTotal] = useState<number>(0);

  const [careers, setCareers] = useState<CareerOption[]>([]);
  const [selectedCareer, setSelectedCareer] = useState<CareerOption>();
  const [courses, setCourses] = useState<Course[]>([]);
  const [selectedCourses, setSelectedCourses] = useState<Course[]>([]);

  const [skills, setSkills] = useState<Skill>({ missingSkills: [], matchingSkills: [] });
  const [recommendCourses, setRecommendCourses] = useState<Course[]>([]);
  const [loading, setLoading] = useState<string>("");
  const dropdownToggle = (e: any) => {
    setDropdownOpen(!dropdownOpen);
  };

  useEffect(() => {
    (async () => {
      try {
        const { data } = await getAllCareers();
        const tmp: CareerOption[] = keysToCamel(data.items as CareerOptionDTO);
        setCareers(tmp);
      } catch (error) {
        console.error(error);
      }
    })();
  }, []);

  useEffect(() => {
    if (!selectedCareer) {
      return;
    }
    (async () => {
      try {
        setLoading("courses");
        const { data } = await getCoursesByCareer(selectedCareer.id, page, 10);
        const tmp: Course[] = keysToCamel(data.items as CourseDTO);
        setCourses(tmp);
        setTotal(data.total);
      } catch (error) {
        console.error(error);
      } finally {
        setLoading("");
      }
    })();
  }, [page, selectedCareer]);

  const isSelected = (id: number): boolean => {
    if (selectedCourses.findIndex((c) => c.id == id) > -1) {
      return true;
    }
    return false;
  };

  const updateSelectedCourses = (course: Course, remove: boolean) => {
    if (remove) {
      const tmp: Course[] = selectedCourses.filter((c) => c.id !== course.id);
      setSelectedCourses(tmp);
    } else setSelectedCourses([...selectedCourses, course]);
  };

  const analyseSkills = async () => {
    try {
      setLoading("skills");
      const coursesId: CourseItem[] = selectedCourses.map((c) => {
        return { courseId: c.id };
      });
      const { data } = await getSkills(coursesId, selectedCareer?.id || 0);
      const tmp: Skill = keysToCamel(data as SkillDTO);
      setSkills(tmp);
    } catch (error) {
      console.error(error);
    } finally {
      setLoading("");
    }
  };

  return (
    <div className="content">
      <Row className="d-flex align-items-center px-3 mb-2">
        <span className="mr-3">Search skills required in</span>
        <Dropdown isOpen={dropdownOpen} toggle={(e: any) => dropdownToggle(e)}>
          <DropdownToggle caret>{!selectedCareer ? "Career" : selectedCareer.careerPath} &nbsp;&nbsp;</DropdownToggle>
          <DropdownMenu right>
            {careers.map((career) => (
              <DropdownItem key={career.id} onClick={() => setSelectedCareer(career)}>
                {career.careerPath}
              </DropdownItem>
            ))}
          </DropdownMenu>
        </Dropdown>
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
                    <th>Action</th>
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
                    courses.map((course) => {
                      const selected: boolean = isSelected(course.id);
                      return (
                        <tr key={course.id}>
                          <td>{course.code}</td>
                          <td>{course.title}</td>
                          <td>{course.level === "ADVANCED" ? "Advanced" : "Basic"}</td>
                          <td>
                            <Button
                              title="Select course"
                              size="sm"
                              color={selected ? "danger" : "warning"}
                              className="p-1 ml-3"
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
                Completed Courses
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
              <div className="d-flex justify-content-end border-top pt-2">
                <Button
                  disabled={!selectedCourses[0]}
                  color="primary"
                  onClick={() => setSelectedCourses([])}
                  className="mr-3"
                >
                  Clear
                </Button>
                <Button disabled={!selectedCourses[0] || loading == "career"} color="primary" onClick={analyseSkills}>
                  Analyse
                </Button>
              </div>
            </CardFooter>
          </Card>
        </Col>
      </Row>
      <Row>
        <Col sm="4">
          <Card style={{ maxHeight: "70vh" }}>
            <CardHeader>
              <CardTitle className="mb-0" tag="h5">
                Matching Skills
              </CardTitle>
            </CardHeader>
            <CardBody style={{ overflowY: "auto", height: "95%", overflowX: "hidden" }}>
              {skills.matchingSkills.length == 0 ? (
                <div className="text-muted">No matching skills</div>
              ) : (
                skills.matchingSkills.map((skill, id) => (
                  <div
                    key={id}
                    className="selected-course"
                    onClick={() => setRecommendCourses(skill.recommendedCourses)}
                  >
                    <div role="button">{skill.name}</div>
                  </div>
                ))
              )}
            </CardBody>
          </Card>
        </Col>
        <Col sm="4">
          <Card style={{ maxHeight: "70vh" }}>
            <CardHeader>
              <CardTitle className="mb-0" tag="h5">
                Missing Skills
              </CardTitle>
            </CardHeader>
            <CardBody style={{ overflowY: "auto", height: "95%", overflowX: "hidden" }}>
              {skills.missingSkills.length == 0 ? (
                <div className="text-muted">No missing skills</div>
              ) : (
                skills.missingSkills.map((skill, id) => (
                  <div
                    key={id}
                    className="selected-course"
                    onClick={() => setRecommendCourses(skill.recommendedCourses)}
                  >
                    <div role="button">{skill.name}</div>
                  </div>
                ))
              )}
            </CardBody>
          </Card>
        </Col>
        <Col sm="4">
          <Card style={{ maxHeight: "70vh" }}>
            <CardHeader>
              <CardTitle className="mb-0" tag="h5">
                Recommend Courses
              </CardTitle>
            </CardHeader>
            <CardBody style={{ overflowY: "auto", height: "95%", overflowX: "hidden" }}>
              {recommendCourses.length == 0 ? (
                <div className="text-muted">No course available</div>
              ) : (
                recommendCourses.map((course, id) => (
                  <div key={id} className="py-1 px-2">
                    <div role="button">{course.outcome}</div>
                  </div>
                ))
              )}
            </CardBody>
          </Card>
        </Col>
      </Row>
    </div>
  );
}

export default StudyPath;
