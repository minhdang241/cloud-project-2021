import React, { useState } from "react";
import {
  Button,
  Modal,
  ModalHeader,
  ModalBody,
  TabContent,
  TabPane,
  Nav,
  NavItem,
  NavLink,
  Row,
  Col,
} from "reactstrap";
import classnames from "classnames";
import { Course } from "utils/Types";

const CourseDetails = ({ course }: { course: Course }) => {
  const [modal, setModal] = useState(false);

  const toggle = () => setModal(!modal);
  const [activeTab, setActiveTab] = useState<string>("des");

  const toggleTab = (tab: string) => {
    if (activeTab !== tab) setActiveTab(tab);
  };
  return (
    <>
      <Button size="sm" color="success" className="py-1 px-2" title="Course details" onClick={toggle}>
        <i className="fas fa-lg fa-info" />
      </Button>
      <Modal isOpen={modal} toggle={toggle}>
        <ModalHeader toggle={toggle}>Course Details</ModalHeader>
        <ModalBody style={{ height: "80vh" }}>
          <Nav tabs>
            <NavItem>
              <NavLink
                role="button"
                className={classnames({ active: activeTab === "des" })}
                onClick={() => {
                  toggleTab("des");
                }}
              >
                Description
              </NavLink>
            </NavItem>
            <NavItem>
              <NavLink
                role="button"
                className={classnames({ active: activeTab === "out" })}
                onClick={() => {
                  toggleTab("out");
                }}
              >
                Learning outcomes
              </NavLink>
            </NavItem>
          </Nav>
          <TabContent
            className="px-2 py-3"
            activeTab={activeTab}
            style={{ overflowY: "auto", height: "95%", overflowX: "hidden" }}
          >
            <TabPane tabId="des">
              <Row>
                <Col sm="12">
                  <p>{course.description}</p>
                </Col>
              </Row>
            </TabPane>
            <TabPane tabId="out">
              <Row>
                <Col sm="12">
                  <p>{course.outcome}</p>
                </Col>
              </Row>
            </TabPane>
          </TabContent>
        </ModalBody>
      </Modal>
    </>
  );
};

export default CourseDetails;
