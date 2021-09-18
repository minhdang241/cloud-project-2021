import Choropleth from "react-leaflet-choropleth";
import { Map } from "react-leaflet";
import "leaflet/dist/leaflet.css";
import { useEffect } from "react";

const style = {
  fillColor: "#ede7f6",
  weight: 1,
  opacity: 1,
  color: "white",
  dashArray: "2",
  fillOpacity: 1,
};

type LegendItem = {
  title: string;
  color: string;
  textColor: string;
};

const Legends = ({ items }: { items: LegendItem[] }) => {
  return (
    <div
      style={{
        display: "flex",
        alignItems: "stretch",
      }}
    >
      {items.map((item) => (
        <div
          key={item.title}
          style={{
            backgroundColor: item.color,
            flex: 1,
            display: "flex",
            alignItems: "center", // vertical
            justifyContent: "center", // horiztontal
            color: item.textColor != null ? item.textColor : "black",
            fontWeight: "bolder",
            fontSize: "1em",
            height: "6vh",
          }}
        >
          <span>{item.title}</span>
        </div>
      ))}
    </div>
  );
};
const Maps = ({ geojson, maxCount }: { geojson: any; maxCount: number }) => {
  const step = Math.round(maxCount / 4);
  const calulateColor = (value: number) => {
    let opacity;
    if (value >= maxCount - step) opacity = 0.9;
    else if (value >= maxCount - step * 2) opacity = 0.5;
    else if (value >= maxCount - step * 3) opacity = 0.3;
    else opacity = 0.1;
    return `rgba(239,129,87, ${opacity})`;
  };
  const items = [
    {
      title: `${maxCount - step}+`,
      color: `rgba(239,129,87,0.9)`,
      textColor: "white",
    },
    {
      title: `${maxCount - step * 2} - ${maxCount - step}`,
      color: `rgba(239,129,87,0.5)`,
      textColor: "white",
    },
    {
      title: `${maxCount - step * 3} - ${maxCount - step * 2}`,
      color: `rgba(239,129,87,0.3)`,
      textColor: "black",
    },
    {
      title: `0 - ${maxCount - step * 3}`,
      color: `rgba(239,129,87,0.1)`,
      textColor: "black",
    },
  ];
  const onEachCountry = (feature: any, layer: any) => {
    const color = calulateColor(feature.properties.value);
    const name = `${feature.properties.localname}: ${feature.properties.value} jobs`;
    layer.options.fillColor = color;
    layer.on({
      mouseout: function (event: any) {
        event.target.setStyle({
          fillColor: color,
          transition: "2",
        });
        event.target.closePopup();
      },
      mouseover: function (event: any): void {
        event.target.setStyle({
          transition: "0.5s",
          fillColor: "#a9a2a2",
        });
        event.target.openPopup();
      },
    });
    layer.bindPopup(name);
  };

  return (
    <>
      <Map style={{ height: "700px" }} zoom={10} center={[10.81739623891044, 106.69106344134427]}>
        <Choropleth
          data={geojson}
          valueProperty={(feature: any) => feature.properties.localname}
          steps={7}
          mode="e"
          style={style}
          onEachFeature={onEachCountry}
        />
      </Map>
      <Legends items={items} />
    </>
  );
};

export default Maps;
