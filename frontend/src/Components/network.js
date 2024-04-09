import React, { useEffect, useRef } from 'react';
import * as d3 from 'd3';

const NetworkGraph = () => {
  const svgRef = useRef();

  useEffect(() => {
    fetchGitHubData();
  }, []);

  const fetchGitHubData = async () => {
    try {
      const response = await fetch('https://raw.githubusercontent.com/0xHarrington/RocketInsight/Visualization-testing/prototyping/network_graph_data.json');
      const data = await response.json();
      renderGraph(data);
    } catch (error) {
      console.error('Error fetching GitHub data:', error);
    }
  };

  const renderGraph = data => {
    const width = 600;
    const height = 800;

    const svg = d3.select(svgRef.current)
      .attr('width', width)
      .attr('height', height);

    // Extract nodes and edges from the data
    const nodes = data.nodes;
    const edges = data.edges;

    // Create a simulation
    const simulation = d3.forceSimulation(nodes)
      .force('link', d3.forceLink(edges).id(d => d.id).distance(200))
      .force('charge', d3.forceManyBody())
      .force('center', d3.forceCenter(width/2, height/2));

    // Render edges
    svg.selectAll('.link')
      .data(edges)
      .enter()
      .append('line')
      .attr('class', 'link')
      .style('stroke', '#999')
      .style('stroke-width', d => Math.sqrt(d.value));

    // Render nodes
    const node = svg.selectAll('.node')
      .data(nodes)
      .enter()
      .append('circle')
      .attr('class', 'node')
      .attr('r', 10)
      .style('fill', 'steelblue');

    // Add labels to nodes
    node.append('title')
      .text(d => d.id);

    // Update node positions during simulation
    simulation.on('tick', () => {
      node
        .attr('cx', d => d.x)
        .attr('cy', d => d.y);

      svg.selectAll('.link')
        .attr('x1', d => d.source.x)
        .attr('y1', d => d.source.y)
        .attr('x2', d => d.target.x)
        .attr('y2', d => d.target.y);
    });
  };

  return (
    <div>
      <br />
      <h3>Network Graph</h3>
      <svg ref={svgRef}></svg>
    </div>
  );
};

export default NetworkGraph;