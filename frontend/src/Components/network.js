import React, { useEffect, useRef } from 'react';
import * as d3 from 'd3';
import '../styles/style.css';

const NetworkGraph = () => {
  const svgRef = useRef();

  useEffect(() => {
    fetchGitHubData();
  }, []);

  const fetchGitHubData = async () => {
    try {
      const response = await fetch('https://raw.githubusercontent.com/0xHarrington/RocketInsight/main/backend/network_graph.json');
      const data = await response.json();
      renderGraph(data);
    } catch (error) {
      console.error('Error fetching GitHub data:', error);
    }
  };

  const renderGraph = data => {
    const width = 800;
    const height = 800;

    const svg = d3.select(svgRef.current)
      .attr('width', width)
      .attr('height', height);

    // Extract nodes and edges from the data
    const nodes = data.nodes;
    const edges = data.edges;
    nodes.forEach(node => {
      if (node.id === 'AAVE: POOL' || node.id === 'COMPOUND: POOL' || node.id === 'PRISMA: POOL') {
        node.radius = 30;
      }
      else if (node.id.startsWith('AAVE: ')) {
        node.radius = 15;
      } 
      else {
        node.radius = 7.5;
      }
    });

    const simulation = d3.forceSimulation(nodes)
      .force('link', d3.forceLink(edges).id(d => d.id).distance(100).strength(.1))
      .force('collide', d3.forceCollide().radius(d => d.radius + 15))
      .force('charge', d3.forceManyBody().strength(d => -10 * d.radius))
      .force('center', d3.forceCenter(width / 2, height / 2));

    const link = svg.selectAll('line')
      .data(edges)
      .enter().append('line')
      .attr('stroke', '#999')
      .attr('stroke-width', 2.5);

    link.append('title')
      .text(d => d["Event Type"]);  

    simulation.on('tick', function () {
      node.attr('cx', d => d.x)
        .attr('cy', d => d.y);
      link.attr('x1', d => d.source.x)
        .attr('y1', d => d.source.y)
        .attr('x2', d => d.target.x)
        .attr('y2', d => d.target.y);
    });

    const node = svg.selectAll('circle')
      .data(nodes)
      .enter().append('circle')
      .attr('r', d => d.radius)
      .attr('fill', 'steelblue')
      .attr('class', d => {
        if (d.id === 'AAVE: POOL' || d.id === 'COMPOUND: POOL' || d.id === 'PRISMA: POOL') {
          return 'specific-node';
        }

        else if (d.id.startsWith('AAVE: ')) {
          return 'aave-node';
        }
        else {
          return 'normal-node';
        }
      });

    // Add labels to nodes
    node.append('title')
      .text(d => d.id);
      
  };

  return (
    <div class="viz">
      <svg ref={svgRef}></svg>
    </div>
  );
};

export default NetworkGraph;