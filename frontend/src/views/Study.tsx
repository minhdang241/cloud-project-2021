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
import { getAllCareers, getSkills } from "services/studyService";
import { getAllCourses } from "services/careerService";
import { CareerOptionDTO, CourseDTO, SkillDTO } from "utils/DTO";
import { keysToCamel } from "utils/functions";
import { CareerOption, Course, Skill } from "utils/Types";
import useDebounce from "utils/useDebounce";
import CourseDetails from "components/Path/CourseDetails";
import SortHeader, { Sort } from "components/Path/SortHeader";

function StudyPath() {
  const [dropdownOpen, setDropdownOpen] = useState(false);
  const [page, setPage] = useState<number>(1);
  const [total, setTotal] = useState<number>(0);
  const [sort, setSort] = useState<Sort>({ by: "", order: "" });
  const [search, setSearch] = useState<string>("");
  const [isSearch, setIsSearch] = useState<boolean>(false);
  const [clear, setClear] = useState<boolean>(false);
  const debounceSort = useDebounce(sort);

  const [careers, setCareers] = useState<CareerOption[]>([]);
  const [selectedCareer, setSelectedCareer] = useState<CareerOption>();
  const [courses, setCourses] = useState<Course[]>([]);
  const [selectedCourses, setSelectedCourses] = useState<Course[]>([]);

  const [skills, setSkills] = useState<Skill>({ missingSkills: [], matchingSkills: [] });
  const [loading, setLoading] = useState<string>("");
  const dropdownToggle = (e: any) => {
    setDropdownOpen(!dropdownOpen);
  };

  useEffect(() => {
    (async () => {
      try {
        // Load career
        const { data: careerData } = await getAllCareers();
        const tmpCareerOptions: CareerOption[] = keysToCamel(careerData.items as CareerOptionDTO);
        setCareers(tmpCareerOptions);
        setSelectedCareer(tmpCareerOptions[0]);
      } catch (error) {
        console.error(error);
      }
    })();
  }, []);

  useEffect(() => {
    if (isSearch) {
      setIsSearch(false);
      return;
    }
    (async () => {
      try {
        setLoading("courses");
        const { data } = await getAllCourses(page, 10, sort.by, sort.order, search);
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

  const analyseSkills = async () => {
    try {
      setLoading("skills");
      const coursesId: number[] = selectedCourses.map((c) => {
        return c.id;
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
      const { data } = await getAllCourses(1, 10, sort.by, sort.order, reset ? "" : search);
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
              <div className="d-flex justify-content-end justify-content-xl-around border-top pt-2">
                <Button
                  disabled={!selectedCourses[0]}
                  color="primary"
                  onClick={() => setSelectedCourses([])}
                  className="mr-3 m-xl-0"
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
        <Col sm="12" xl="6">
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
                  <div key={id}>
                    <span>{skill.name}</span>
                  </div>
                ))
              )}
            </CardBody>
          </Card>
        </Col>
        <Col sm="12" xl="6">
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
                  <div key={id}>
                    <span>{skill.name}</span>
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
