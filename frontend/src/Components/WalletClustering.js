import React, { useState, useEffect, useRef } from 'react';
import * as d3 from 'd3';
import axios from 'axios';

const WalletClustering = ({ market = 'AAVE', timeframe = 365 }) => {
    const [data, setData] = useState([]);
    const svgRef = useRef();

    useEffect(() => {
        fetchData(market, timeframe);
    }, [market, timeframe]);

    const fetchData = (market, timeframe) => {
        axios.get(`/historical_data?market=${market}&timeframe=${timeframe}`)
            .then(response => {
                setData(response.data);
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

        // Define x and y scales
        const xScale = d3.scaleLinear()
            .domain(d3.extent(data, d => d.x))
            .range([0, width]);

        const yScale = d3.scaleLinear()
            .domain([0, d3.max(data, d => d.y)])
            .range([height, 0]);

        // Define line generator
        const line = d3.line()
            .x(d => xScale(d.x))
            .y(d => yScale(d.y));

        // Clear previous contents
        svg.selectAll("*").remove();

        // Draw line
        svg.append('path')
            .datum(data)
            .attr('class', 'line')
            .attr('d', line)
            .attr('fill', 'none')
            .attr('stroke', 'steelblue')
            .attr('stroke-width', 2);

        // Draw x and y axes
        svg.append('g')
            .attr('transform', `translate(0,${height})`)
            .call(d3.axisBottom(xScale));

        svg.append('g')
            .call(d3.axisLeft(yScale));
    }, [data]);

    return (
        <div>
            <h2>Wallet Clustering Visualization</h2>
            <svg ref={svgRef} width={600} height={400}></svg>
        </div>
    );
};

export default WalletClustering;
