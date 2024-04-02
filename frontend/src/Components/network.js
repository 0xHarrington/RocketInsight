import React, { useState, useEffect, useRef } from 'react';
import * as d3 from 'd3';

const NetworkGraph = () => {
  const [data, setData] = useState([]);
  const svgRef = useRef();

  useEffect(() => {
    if (data.length === 0) return;

    const svg = d3.select(svgRef.current);
    const width = +svg.attr('width');
    const height = +svg.attr('height');

    const simulation = d3.forceSimulation(data.nodes)
      .force('link', d3.forceLink(data.links).id(d => d.id))
      .force('charge', d3.forceManyBody())
      .force('center', d3.forceCenter(width / 2, height / 2));

    const link = svg.append('g')
      .attr('stroke', '#999')
      .attr('stroke-opacity', 0.6)
      .selectAll('line')
      .data(data.links)
      .join('line')
      .attr('stroke-width', d => Math.sqrt(d.value));

    const node = svg.append('g')
      .attr('stroke', '#fff')
      .attr('stroke-width', 1.5)
      .selectAll('circle')
      .data(data.nodes)
      .join('circle')
      .attr('r', 5)
      .attr('fill', '#1f77b4');

    node.append('title')
      .text(d => d.id);

    simulation.on('tick', () => {
      link
        .attr('x1', d => d.source.x)
        .attr('y1', d => d.source.y)
        .attr('x2', d => d.target.x)
        .attr('y2', d => d.target.y);

      node
        .attr('cx', d => d.x)
        .attr('cy', d => d.y);
    });
  }, [data]);

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = () => {
    d3.json('./graphdata.json').then(data => {
      setData(data);
    }).catch(error => {
      console.error('Error fetching data:', error);
    });
  };

  return (
    <div>
      <h2>Network Graph</h2>
      <svg ref={svgRef} width={600} height={400}></svg>
    </div>
  );
};

export default NetworkGraph;
