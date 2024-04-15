import * as d3 from "d3";
import { useEffect, useRef } from "react";

const Barchart = () => {
  const ref = useRef();

  useEffect(() => {
    // set the dimensions and margins of the graph
    const margin = { top: 30, right: 30, bottom: 70, left: 60 },
      width = 460 - margin.left - margin.right,
      height = 400 - margin.top - margin.bottom;

    // append the svg object to the body of the page
    const svg = d3
      .select(ref.current)
      .append("svg")
      .attr("width", width + margin.left + margin.right)
      .attr("height", height + margin.top + margin.bottom)
      .append("g")
      .attr("transform", `translate(${margin.left},${margin.top})`);

    // Parse the Data
    d3.csv(
      "https://raw.githubusercontent.com/0xHarrington/RocketInsight/main/frontend/h_supply_borrow5.csv"
    ).then(function (data) {
      // X axis
      const x = d3
      .scaleBand()
      .range([0, width])
      .domain(data.map((d) => d.Date))
      .padding(0.2);
      svg
        .append("g")
        .attr("transform", `translate(0, ${height})`)
        .call(d3.axisBottom(x))
        .selectAll("text")
        .attr("transform", "translate(-10,0)rotate(-45)")
        .style("text-anchor", "end");

      // Add Y axis
      const y = d3.scaleLinear().domain([0, 70000]).range([height, 0]);
      svg.append("g").call(d3.axisLeft(y));

      // Bars
      svg
        .selectAll("mybar")
        .data(data)
        .join("rect")
        .attr("x", (d) => x(d.Date))
        .attr("y", (d) => y(d.Total_Amount))
        .attr("width", x.bandwidth())
        .attr("height", (d) => height - y(d.Total_Amount))
        .attr("fill", "#5f0f40");
    });
  }, []);

  return <svg width={1000} height={600} id="barchart" ref={ref} />;
};

export default Barchart;