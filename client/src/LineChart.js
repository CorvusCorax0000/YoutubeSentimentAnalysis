// LineChart.js
import React, { useEffect, useState } from 'react';
import axios from 'axios';

const LineChart = ({ fetchTrigger }) => {
    const [chartSrc, setChartSrc] = useState('');

    const fetchChart = async () => {
        try {
            const response = await axios.get('http://localhost:8000/visualize/');
            setChartSrc(`data:image/png;base64,${response.data.chart}`);
        } catch (error) {
            console.error('Error fetching chart', error);
        }
    };

    useEffect(() => {
        if (fetchTrigger) {
            fetchChart();
            const interval = setInterval(fetchChart, 5000); // Update every 5 seconds
            return () => clearInterval(interval);
        }
    }, [fetchTrigger]);

    return (
        <div>
            {chartSrc && <img src={chartSrc} alt="Line Chart" />}
        </div>
    );
};

export default LineChart;
