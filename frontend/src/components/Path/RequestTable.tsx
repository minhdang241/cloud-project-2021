import { useState, useEffect } from "react";
import Pagination from "react-js-pagination";
// reactstrap components
import { Card, CardHeader, CardBody, CardTitle, Table, Row, Col, Spinner, Button } from "reactstrap";
import { RequestDTO } from "utils/DTO";
import { keysToCamel } from "utils/functions";
import { Request } from "utils/Types";

function RequestTable() {
  const [page, setPage] = useState<number>(1);
  const [total, setTotal] = useState<number>(0);
  const [requests, setRequests] = useState<Request[]>([]);
  const [loading, setLoading] = useState<boolean>(false);

  useEffect(() => {
    (async () => {
      try {
        setLoading(true);
        console.log("object");
      } catch (error) {
        console.error(error);
      } finally {
        setLoading(false);
      }
    })();
  }, [page]);

  return (
    <Col sm="12">
      <Card>
        <CardHeader className="d-flex justify-content-between">
          <CardTitle tag="h5" className="mb-0">
            Request Table
          </CardTitle>
          <Button title="Update chart" size="sm" color="primary" className="p-1">
            update
          </Button>
        </CardHeader>
        <CardBody>
          <Table responsive>
            <thead className="text-primary">
              <tr>
                <th>ID</th>
                <th>Created at</th>
                <th>Updated at</th>
                <th>Status</th>
              </tr>
            </thead>
            <tbody>
              {loading ? (
                <tr>
                  <td colSpan={5} className="text-center py-9">
                    <Spinner
                      color="warning"
                      style={{
                        width: "3rem",
                        height: "3rem",
                      }}
                    />
                  </td>
                </tr>
              ) : requests.length == 0 ? (
                <tr>
                  <td colSpan={5} className="text-muted">
                    Your requests display here
                  </td>
                </tr>
              ) : (
                requests.map((req) => (
                  <tr key={req.requestId}>
                    <td>{req.requestId}</td>
                    <td>{req.createdAt}</td>
                    <td>{req.updatedAt}</td>
                    <td>{req.status}</td>
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
  );
}

export default RequestTable;
