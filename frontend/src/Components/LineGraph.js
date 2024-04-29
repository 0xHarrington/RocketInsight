import React, { useState, useEffect, useRef } from 'react';
import * as d3 from 'd3';
import axios from 'axios';
import '../styles/style.css';

const LineGraph = ({ market, timeframe }) => {
  const [data, setData] = useState([]);
  const svgRef = useRef();
  const tooltipRef = useRef();

  useEffect(() => {
    fetchData(market, timeframe);
  }, [market, timeframe]);

  const fetchData = (market, timeframe) => {
    axios.get(`http://localhost:5000/api/historical_data?market=${market}&timeframe=${timeframe}`)
      .then(response => {
        console.log('Before sort:', response.data);
        const groupedData = d3.groups(response.data, d => d.Data_Type)
          .map(([key, values]) => {
            // Convert Timestamp from seconds to milliseconds and sort
            const sortedValues = values.map(d => ({
              ...d,
              Timestamp: d.Timestamp * 1000  // Convert to milliseconds
            })).sort((a, b) => a.Timestamp - b.Timestamp);  // Sort by Timestamp
            return {
              type: key,
              values: sortedValues.map(d => ({ x: new Date(d.Timestamp), y: d.Value }))
            };
          });
        console.log('After sort:', groupedData);
        setData(groupedData);
      })
      .catch(error => {
        console.error('Error fetching data:', error);
      });
  };

  useEffect(() => {
    if (data.length === 0) return;

    const svg = d3.select(svgRef.current);
    const margin = { top: 20, right: 30, bottom: 60, left: 80 }; // Increased bottom and left margin for labels
    const width = +svg.attr('width') - margin.left - margin.right;
    const height = +svg.attr('height') - margin.top - margin.bottom;
    svg.selectAll("*").remove(); // Clear previous contents

    const xScale = d3.scaleTime()
      .domain([
        d3.min(data, series => d3.min(series.values, d => d.x)),
        d3.max(data, series => d3.max(series.values, d => d.x))
      ])
      .range([margin.left, width + margin.left]); // Adjust range to include margins

    const yScale = d3.scaleLinear()
      .domain([
        0, // Minimum y-value (could be adjusted if necessary)
        d3.max(data, series => d3.max(series.values, d => d.y))
      ])
      .nice() // Round the y-axis domain for better readability
      .range([height + margin.top, margin.top]); // Adjust range to include margins

    const colors = d3.scaleOrdinal(d3.schemeCategory10); // Color scale for different lines

    const xAxis = d3.axisBottom(xScale)
      .tickSizeOuter(0) // Remove outer ticks
      .tickPadding(10) // Padding between ticks and labels
      .tickFormat(d3.timeFormat("%B")); // Format tick labels as month names

    const yAxis = d3.axisLeft(yScale)
      .tickSizeOuter(0) // Remove outer ticks
      .tickPadding(10); // Padding between ticks and labels

    svg.append('g')
      .attr('transform', `translate(0,${height + margin.top})`) // Adjusted translation
      .call(xAxis)
      .append('text') // X-axis label
      .attr('x', width / 2 + margin.left) // Adjusted position
      .attr('y', margin.bottom - 10)
      .attr('text-anchor', 'middle')
      .style('fill', 'white')
      .style('font-size', '18px')
      .text('Month');

    svg.append('g')
      .attr('transform', `translate(${margin.left},${margin.top})`)
      .call(yAxis)
      .append('text') // Y-axis label
      .attr('transform', 'rotate(-90)')
      .attr('x', -height / 2 - margin.top) // Adjusted position
      .attr('y', -margin.left + 15)
      .attr('text-anchor', 'middle')
      .style('fill', 'white')
      .style('font-size', '18px')
      .text('Value');

    const line = d3.line()
      .x(d => xScale(d.x))
      .y(d => yScale(d.y));

    data.forEach((series, i) => {
      svg.append('path')
        .datum(series.values)
        .attr('fill', 'none')
        .attr('stroke', colors(i))
        .attr('stroke-width', 2)
        .attr('d', line);
      svg.selectAll(`.dot-${i}`)
        .data(series.values)
        .enter().append('circle')
        .attr('class', `dot-${i}`)
        .attr('cx', d => xScale(d.x))
        .attr('cy', d => yScale(d.y))
        .attr('r', 2.5)
        .attr('fill', colors(i))
        .on("mouseover", (event, d) => {
          const tooltip = d3.select(tooltipRef.current);
          const formattedY = (d.y).toFixed(2);
          tooltip.style('visibility', 'visible')
            .style('opacity', 1)  // Make sure to set opacity to 1
            .html(`<strong>${series.type}</strong><br/>Time: ${d3.timeFormat('%B %d, %Y')(d.x)}, Amount: ${formattedY}`)
            .style('left', `${event.pageX + 10}px`)
            .style('top', `${event.pageY + 10}px`);
        })
        .on("mouseout", () => {
          d3.select(tooltipRef.current)
            .style('visibility', 'hidden')
            .style('opacity', 0);  // Reset opacity
        });
    });
  }, [data]);

  return (
    <div className="viz">
      <h2>Line Graph</h2>
      <svg ref={svgRef} width={1200} height={750} ></svg>
      <div ref={tooltipRef} className="tooltip"></div>
    </div>
  );
};

export default LineGraph;
