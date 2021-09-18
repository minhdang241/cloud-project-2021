import { useState, useEffect } from "react";
import { Pie } from "react-chartjs-2";
import { Card, CardHeader, CardBody, CardFooter, CardTitle, Row, Col, Table, Button } from "reactstrap";
import { getCourseLevel } from "services/statService";
import ChartDataLabels from "chartjs-plugin-datalabels";
import { CourseLevelDTO } from "utils/DTO";
import { keysToCamel } from "utils/functions";
import { CourseLevel } from "utils/Types";
import RequestTable from "components/Path/RequestTable";

export const LevelTable = ({ levels }: { levels: CourseLevel[] }) => {
  const total = levels[0].count + levels[1].count;
  return (
    <Table className="text-center mb-0 pb-0 mt-3" responsive>
      <thead className="text-primary">
        <tr>
          <th>Total</th>
          <th>Basic</th>
          <th>Advanced</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td>100%</td>
          {levels.map((le, i) => (
            <td key={i}>{(le.count * 100) / total}%</td>
          ))}
        </tr>
        <tr>
          <td>{total}</td>
          {levels.map((le, i) => (
            <td key={i}>{le.count}</td>
          ))}
        </tr>
      </tbody>
    </Table>
  );
};

function Dashboard() {
  const [levels, setLevels] = useState<CourseLevel[]>([]);
  const updateLevels = async () => {
    try {
      const { data } = await getCourseLevel();
      const tmp: CourseLevel[] = keysToCamel(data as CourseLevelDTO);
      setLevels(tmp);
    } catch (error) {
      console.error(error);
    }
  };
  useEffect(() => {
    updateLevels();
  }, []);
  return (
    <>
      <div className="content">
        <Row>
          <RequestTable />
        </Row>
        <Row>
          <Col sm={{ size: 4, offset: 4 }}>
            <Card>
              <CardHeader>
                <CardTitle tag="h5">Course Level Distribution</CardTitle>
              </CardHeader>
              <CardBody style={{ height: "250px" }}>
                <Pie
                  type="pie"
                  data={{
                    labels: ["Basic", "Advanced"],
                    datasets: [
                      {
                        label: "Levels",
                        pointRadius: 0,
                        pointHoverRadius: 0,
                        backgroundColor: ["#fcc468", "#ef8157"],
                        borderWidth: 0,
                        data: levels.map((l) => l.count),
                      },
                    ],
                  }}
                  options={{
                    plugins: {
                      legend: { display: false },
                      datalabels: {
                        formatter: (_: any, context: any) =>
                          (levels[context.dataIndex].count * 100) / (levels[0].count + levels[1].count) + "%",
                      },
                    },
                    maintainAspectRatio: false,
                  }}
                  plugins={[ChartDataLabels]}
                />
              </CardBody>
              <CardFooter>
                <div className="legend text-center">
                  <i className="fa fa-circle text-warning" /> Basic <i className="fa fa-circle text-danger ml-3" />{" "}
                  Advanced
                </div>
                {levels[0] && <LevelTable levels={levels} />}
                <div className="stats">
                  <div className="text-muted">Updated 3 minutes ago</div>
                </div>
              </CardFooter>
            </Card>
          </Col>
        </Row>
      </div>
    </>
  );
}

export default Dashboard;
