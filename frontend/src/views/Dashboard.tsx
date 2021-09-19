import { useState, useEffect, useMemo } from "react";
import { Pie, Bar } from "react-chartjs-2";
import { Card, CardHeader, CardBody, CardFooter, CardTitle, Row, Col, Table, Button } from "reactstrap";
import {
  getCounts,
  getCourseLevel,
  getCourseWordCloud,
  getJobCompany,
  getJobDistrict,
  getJobWordCloud,
} from "services/statService";
import ChartDataLabels from "chartjs-plugin-datalabels";
import { CareerOptionDTO, CourseLevelDTO, JobDistrictDTO } from "utils/DTO";
import { keysToCamel } from "utils/functions";
import { CareerOption, Count, CourseLevel, JobDistrict } from "utils/Types";
import WordCloud from "components/graph/WordCloud";
import { getAllCareers } from "services/studyService";
import Chart from "chart.js";
import Maps from "components/graph/Map";
import RequestTable from "components/Path/RequestTable";

const Header = ({ title, subtitle }: { title: string; subtitle?: string }) => {
  return (
    <>
      <h5 className="font-weight-bolder">{title}</h5>
    </>
  );
};

const MapCharts = () => {
  const [geojson, setGeojson] = useState(null);
  const [maxCount, setMaxCount] = useState<number>();

  async function fetchDistrictJobCount() {
    return Promise.all([
      getJobDistrict(),
      fetch("../district.json", {
        headers: {
          "Content-Type": "application/json",
          Accept: "application/json",
        },
      }),
    ]).then(([jobDistrinctCount, file]) => {
      return { jobDistrinctCount, file };
    });
  }
  const promise = fetchDistrictJobCount();

  useEffect(() => {
    promise.then((response) => {
      const jobs: JobDistrict[] = keysToCamel(response.jobDistrinctCount.data as JobDistrictDTO);

      response.file.json().then((json) => {
        const dictionary: { [key: number]: number } = {};
        let max = 0;
        jobs.forEach((job) => {
          dictionary[job.companyDistrict] = job.count;
          if (job.count > max) {
            max = job.count;
          }
        });
        setMaxCount(max);
        json.features.forEach((feature: any) => {
          feature.properties.value = dictionary[parseInt(feature.id)];
        });
        setGeojson(json.features);
      });
    });
  }, []);

  return (
    <>
      <div>{geojson && maxCount && <Maps geojson={geojson} maxCount={maxCount} />}</div>
    </>
  );
};

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

const CourseLevelChart = () => {
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
      <Header title="Course Level Distribution" />
      <Card className="border shadow-none" style={{ borderColor: "#d0d0d0" }}>
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
                legend: { position: "bottom" },
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
          {/* <div className="legend text-center">
            <i className="fa fa-circle text-warning" /> Basic <i className="fa fa-circle text-danger ml-3" /> Advanced
          </div> */}
          {levels[0] && <LevelTable levels={levels} />}
        </CardFooter>
      </Card>
    </>
  );
};

const DistributionCareers = () => {
  const [graphData, setGraphData] = useState<Chart.ChartData>();
  const [careers, setCareers] = useState<CareerOption[]>([]);

  const updateCareerCount = async () => {
    try {
      // Load career
      const { data: careerData } = await getAllCareers();
      const tmpCareerOptions: CareerOption[] = keysToCamel(careerData.items as CareerOptionDTO);
      setCareers(tmpCareerOptions);
    } catch (error) {
      console.error(error);
    }
  };

  useEffect(() => {
    updateCareerCount();
  }, []);

  useEffect(() => {
    const labels = [];
    const counts = [];
    for (const obj of careers) {
      labels.push(obj.careerPath);
      counts.push(obj.totalJobs);
    }

    setGraphData({
      labels: labels,
      datasets: [
        {
          label: "# of jobs",
          data: counts,
          borderColor: "#fcc468",
          backgroundColor: "rgba(255, 206, 86, 0.2)",
          hoverBackgroundColor: "#fcc469",
          borderWidth: 1,
        },
      ],
    });
  }, [careers]);

  return (
    <div>
      {graphData && (
        <Bar
          data={graphData}
          options={{
            responsive: true,
            scales: {
              yAxes: [
                {
                  scaleLabel: {
                    display: true,
                    labelString: "# of Jobs",
                  },
                },
              ],
              xAxes: [
                {
                  ticks: {
                    beginAtZero: true,
                  },
                },
              ],
            },
            legend: {
              display: false,
            },
          }}
        />
      )}
    </div>
  );
};

const SubInfo = ({ label, value }: { label: string; value: string }) => {
  return (
    <Col className="d-flex flex-column align-items-center">
      <div className="text-center">
        <h2 className="display-4 m-0 font-weight-normal text-primary">{value}</h2>
        <p className="ls-1 mt-1 mb-0 ">{label}</p>
      </div>
    </Col>
  );
};

function Dashboard() {
  const [count, setCount] = useState<Count>();
  const getStatisticCount = async () => {
    try {
      const { data: countData } = await getCounts();
      const temp: Count = keysToCamel(countData);
      setCount(temp);
    } catch (error) {
      console.error(error);
    }
  };
  useEffect(() => {
    getStatisticCount();
  }, []);
  return (
    <>
      <div className="content container-fluid w-xl-80 w-90">
        <Row className="border-top border-bottom">
          <Col sm="1"></Col>
          <SubInfo label="courses from RMIT" value={count?.courseCount.toString() || ""} />
          <SubInfo label={`jobs from ${count?.companyCount} companies`} value={count?.jobCount.toString() || ""} />
          <SubInfo label="career path" value={count?.careerCount.toString() || ""} />
          <Col sm="1"></Col>
        </Row>
        <Row className="mt-5">
          <RequestTable />
        </Row>
        <div className="my-5">
          <Header title="Career Distribution" subtitle="Number of Jobs per Career" />
          <Card className="border shadow-none" style={{ borderColor: "#d0d0d0" }}>
            <CardBody>
              <DistributionCareers />
            </CardBody>
          </Card>
        </div>
        <Row className="my-5">
          <Col>
            <Header title="Map of Jobs in HCM city" />
            <MapCharts />
          </Col>
          <Col>
            <WordCloud
              title="Jobs from Companies"
              subtitle="Describe the amount of jobs each company offers"
              getWordCloud={getJobCompany}
            />
            <WordCloud
              title="Job Description"
              subtitle="Word Frequencies in Job Description"
              getWordCloud={getJobWordCloud}
            />
          </Col>
        </Row>
        <Row>
          <Col>
            <CourseLevelChart />
          </Col>
          <Col>
            <WordCloud
              title="Course Description"
              subtitle="Word Frequencies in Course Description"
              getWordCloud={getCourseWordCloud}
            />
          </Col>
        </Row>
      </div>
    </>
  );
}

export default Dashboard;
