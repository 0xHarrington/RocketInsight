import React, { useEffect, useRef } from 'react';
import * as d3 from 'd3';
import axios from 'axios';
import '../styles/style.css';

const NetworkGraph = ({ userAddress, market }) => {
  const svgRef = useRef();

  useEffect(() => {
    fetchApiData();
  }, [userAddress, market]);  // Re-fetch data when userAddress or market changes

  const fetchApiData = async () => {
    try {
      const endpoint = `http://localhost:5000/api/user_history`;
      const response = await axios.get(endpoint);
      const data = response.data;
      renderGraph(data);
    } catch (error) {
      console.error('Error fetching data from API:', error);
    }
  };

  const renderGraph = data => {
    const width = window.innerWidth - 100;
    const height = window.innerHeight - 100;

    const svg = d3.select(svgRef.current)
      .attr('width', width)
      .attr('height', height)
      .html('');  // Clear previous SVG contents before rendering new graph

    // Extract nodes and edges from the data
    const nodes = data.nodes;
    const edges = data.edges;
    nodes.forEach(node => {
      if (node.id === 'AAVE: POOL' || node.id === 'COMPOUND: POOL' || node.id === 'PRISMA: POOL') {
        node.radius = 35;
      } else if (node.id.startsWith('AAVE: ')) {
        node.radius = 20;
      } else {
        node.radius = 10;
      }
    });

    const simulation = d3.forceSimulation(nodes)
      // ensure that the nodes do not overlap
      .force('link', d3.forceLink(edges).id(d => d.id).distance(100).strength(0.2))
      .force('collide', d3.forceCollide().radius(d => d.radius + 4.2))
      .force('charge', d3.forceManyBody().strength(d => -2 * d.radius))
      .force('center', d3.forceCenter(width / 2, height / 2).strength(0.420));

    const link = svg.selectAll('line')
      .data(edges)
      .enter().append('line')
      .attr('stroke', '#EBDBB2')
      .attr('stroke-width', 4.2);

    link.append('title')
      .text(d => d["Event Type"]);

    const node = svg.selectAll('circle')
      .data(nodes)
      .enter().append('circle')
      .attr('r', d => d.radius)
      .attr('fill', 'steelblue')
      .attr('class', d => {
        if (d.id === 'AAVE: POOL' || d.id === 'COMPOUND: POOL' || d.id === 'PRISMA: POOL') {
          return 'specific-node';
        } else if (d.id.startsWith('AAVE: ')) {
          return 'aave-node';
        } else {
          return 'normal-node';
        }
      });

    simulation.on('tick', () => {
      node.attr('cx', d => d.x)
        .attr('cy', d => d.y);
      link.attr('x1', d => d.source.x)
        .attr('y1', d => d.source.y)
        .attr('x2', d => d.target.x)
        .attr('y2', d => d.target.y);
    });

    node.append('title')
      .text(d => d.id);
  };

  return (
    <div className="viz">
      <svg ref={svgRef}></svg>
    </div>
  );
};

export default NetworkGraph;
