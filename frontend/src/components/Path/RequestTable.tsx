import { useState, useEffect, useContext } from "react";
import Pagination from "react-js-pagination";
import Loader from "react-loader-spinner";
// reactstrap components
import { Card, CardHeader, CardBody, CardTitle, Table, Row, Col, Spinner, Button } from "reactstrap";
import { getRequests } from "services/requestService";
import { RequestDTO } from "utils/DTO";
import { keysToCamel } from "utils/functions";
import { Request } from "utils/Types";
import moment from "moment";
import { UserContext } from "App";
import { crawl } from "services/statService";

function RequestTable() {
  const { username } = useContext(UserContext);
  const [page, setPage] = useState<number>(1);
  const [total, setTotal] = useState<number>(0);
  const [requests, setRequests] = useState<Request[]>([]);
  const [loading, setLoading] = useState<boolean>(false);

  useEffect(() => {
    (async () => {
      try {
        setLoading(true);
        const { data: requestData } = await getRequests(username || "", page, 10);
        const temp: Request[] = keysToCamel(requestData.items as RequestDTO);
        setRequests(temp);
        setTotal(requestData.total);
      } catch (error) {
        console.error(error);
      } finally {
        setLoading(false);
      }
    })();
  }, [page]);

  const getDiff = (dateStr1?: string, dateStr2?: string): string => {
    if (dateStr1 == null || dateStr2 == null) {
      return "";
    }
    const diff = new Date(dateStr1).getTime() - new Date(dateStr2).getTime();
    const elements = moment
      .utc(diff * 1000)
      .format("mm:ss")
      .split(":");
    return `${elements[0]} minutes ${elements[1]} seconds`;
  };

  const updateData = async () => {
    try {
      const res = await crawl(username || "");
      const temp: Request = keysToCamel(res.data.created_object as RequestDTO);
      setRequests([temp, ...requests]);
    } catch (error) {
      console.error(error);
    }
  };

  return (
    <Col sm="12">
      <Card>
        <CardHeader className="d-flex justify-content-between">
          <CardTitle tag="h5" className="mb-0">
            Request Table
          </CardTitle>
          <Button
            title="Update chart"
            disabled={requests[0]?.status === "RUNNING"}
            size="sm"
            color="primary"
            className="p-1"
            onClick={updateData}
          >
            update
          </Button>
        </CardHeader>
        <CardBody>
          <Table responsive>
            <thead className="text-primary">
              <tr>
                <th>ID</th>
                <th>Created at</th>
                <th>Elapse time</th>
                <th>Status</th>
                <th>Total Item</th>
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
                  <tr key={req.id}>
                    <td>{req.id}</td>
                    <td>{moment(req.createdAt).calendar()}</td>
                    <td>{getDiff(req.updatedAt, req.createdAt)}</td>
                    <td>
                      <div className="d-flex align-items-center">
                        <span className="mr-3">{req.status === "RUNNING" ? "Running" : "Finished"}</span>
                        {req.status === "RUNNING" && <Loader type="ThreeDots" color="#38b9bb" height={40} width={40} />}
                      </div>
                    </td>
                    <td>{req.requestMetadata?.totalItem}</td>
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
