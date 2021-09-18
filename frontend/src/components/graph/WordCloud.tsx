import { useState, useEffect } from "react";
import { Card, CardHeader, CardBody, CardTitle } from "reactstrap";
import { WordFrquenciesDTO } from "utils/DTO";
import { keysToCamel } from "utils/functions";
import { WordFreq, WordFrquencies } from "utils/Types";
import { TagCloud } from "react-tagcloud";
import { AxiosResponse } from "axios";

const WordCloud = ({
  title,
  getWordCloud,
  subtitle,
}: {
  title: string;
  getWordCloud: () => Promise<AxiosResponse<WordFrquenciesDTO>>;
  subtitle?: string;
}) => {
  const [wordFreqData, setWordFreqData] = useState<WordFreq[]>([]);

  const updateCourseWordCloud = async () => {
    try {
      const res: AxiosResponse<WordFrquenciesDTO> = await getWordCloud();
      const wordList: WordFrquencies = keysToCamel(res.data);
      setWordFreqData(wordList.words);
    } catch (error) {
      console.error(error);
    }
  };
  useEffect(() => {
    updateCourseWordCloud();
  }, []);
  return (
    <>
      <h5 className="font-weight-bolder">{title}</h5>
      <Card className="border shadow-none" style={{ borderColor: "#d0d0d0" }}>
        <CardBody>
          {wordFreqData && (
            <TagCloud
              minSize={12}
              maxSize={50}
              tags={wordFreqData}
              colorOptions={{
                luminosity: "dark",
                hue: "blue",
              }}
            />
          )}
        </CardBody>
      </Card>
    </>
  );
};

export default WordCloud;
