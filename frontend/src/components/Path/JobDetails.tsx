import { useState } from "react";
import { Button, Modal, ModalHeader, ModalBody } from "reactstrap";

const JobDetails = ({ job }: { job: string }) => {
  const [modal, setModal] = useState(false);
  const toggle = () => setModal(!modal);

  return (
    <>
      <Button size="sm" color="success" className="py-1 px-2" title="Job description" onClick={toggle}>
        <i className="fas fa-lg fa-info" />
      </Button>
      <Modal isOpen={modal} toggle={toggle}>
        <ModalHeader toggle={toggle}>Job Description</ModalHeader>
        <ModalBody style={{ height: "80vh" }}>
          <p className="p-3">{job}</p>
        </ModalBody>
      </Modal>
    </>
  );
};

export default JobDetails;
