import React, { useState, useEffect, useRef } from 'react';
import * as d3 from 'd3';
import axios from 'axios';

const LineGraph = ({ market = 'AAVE', timeframe = 365 }) => {
  const [data, setData] = useState([]);
  const svgRef = useRef();

  useEffect(() => {
    fetchData(market, timeframe);
  }, [market, timeframe]);

  const fetchData = (market, timeframe) => {
    axios.get(`http://localhost:5000/api/historical_data?market=${market}&timeframe=${timeframe}`)
      .then(response => {
        const groupedData = d3.groups(response.data, d => d.Data_Type)
          .map(([key, values]) => {
            const sortedValues = values.sort((a, b) => a.Timestamp - b.Timestamp); // Sort by Timestamp
            return {
              type: key,
              values: sortedValues.map(d => ({ x: d.Timestamp, y: d.Value }))
            };
          });
        console.log('Grouped data:', groupedData); // Debugging output
        setData(groupedData);
      })
      .catch(error => {
        console.error('Error fetching data:', error);
      });
  };


  useEffect(() => {
    if (data.length === 0) return;

    const svg = d3.select(svgRef.current);
    const width = +svg.attr('width');
    const height = +svg.attr('height');
    svg.selectAll("*").remove(); // Clear previous contents

    const xScale = d3.scaleLinear()
      .domain([d3.min(data, series => d3.min(series.values, d => d.x)),
      d3.max(data, series => d3.max(series.values, d => d.x))])
      .range([0, width]);

    const yScale = d3.scaleLinear()
      .domain([0, d3.max(data, series => d3.max(series.values, d => d.y))])
      .range([height, 0]);

    const colors = d3.scaleOrdinal(d3.schemeCategory10); // Color scale for different lines


    data.forEach((series, i) => {
      const line = d3.line()
        .x(d => xScale(d.x))
        .y(d => yScale(d.y));

      svg.append('path')
        .datum(series.values)
        .attr('fill', 'none')
        .attr('stroke', colors(i))
        .attr('stroke-width', 2)
        .attr('d', line);

      // Optional: Add labels or other elements per series
    });

    // Draw x and y axes
    svg.append('g')
      .attr('transform', `translate(0,${height})`)
      .call(d3.axisBottom(xScale));

    svg.append('g')
      .call(d3.axisLeft(yScale));
  }, [data]);


  return (
    <div class="viz">
        <h2>Line Graph</h2>
        <br />
        <svg ref={svgRef} width={600} height={400}></svg>
        <br />
    </div>
  );
};

export default LineGraph;
