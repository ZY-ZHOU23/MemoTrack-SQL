import React, { useState, useEffect } from 'react';
import {
  Container,
  Grid,
  Paper,
  Typography,
  Box,
  CircularProgress,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Alert,
} from '@mui/material';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  Title,
  Tooltip,
  Legend,
  ArcElement,
} from 'chart.js';
import { Line, Bar, Doughnut } from 'react-chartjs-2';
import { analytics } from '../services/api';
import { useAuth } from '../hooks/useAuth';

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  Title,
  Tooltip,
  Legend,
  ArcElement
);

interface AnalyticsData {
  entriesByCategory: Array<{
    category: string;
    count: number;
  }>;
  entriesByDate: Array<{
    date: string;
    count: number;
  }>;
  entriesByTag: Array<{
    tag: string;
    count: number;
  }>;
  totalEntries: number;
  totalCategories: number;
  totalTags: number;
  averageEntriesPerDay: number;
  mostActiveDay: string;
  mostUsedCategory: string;
  mostUsedTag: string;
}

export default function Analytics() {
  const [data, setData] = useState<AnalyticsData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [timeRange, setTimeRange] = useState('7d');
  const { user } = useAuth();

  useEffect(() => {
    fetchAnalytics();
  }, [timeRange]);

  const fetchAnalytics = async () => {
    try {
      setLoading(true);
      console.log(`Fetching analytics with time range: ${timeRange}`);
      const response = await analytics.getAnalytics(timeRange);
      console.log('Analytics data received:', response.data);
      setData(response.data);
      setError(null);
    } catch (error: any) {
      console.error('Error fetching analytics:', error);
      setError(error.response?.data?.detail || 'Failed to load analytics data');
      // Provide empty data as fallback
      setData({
        totalEntries: 0,
        totalCategories: 0,
        totalTags: 0,
        averageEntriesPerDay: 0,
        mostActiveDay: 'N/A',
        mostUsedCategory: 'N/A',
        mostUsedTag: 'N/A',
        entriesByCategory: [],
        entriesByDate: [],
        entriesByTag: []
      });
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <Box
        display="flex"
        justifyContent="center"
        alignItems="center"
        minHeight="80vh"
      >
        <CircularProgress />
      </Box>
    );
  }

  const entriesByCategoryData = {
    labels: data?.entriesByCategory.map((item) => item.category) || [],
    datasets: [
      {
        data: data?.entriesByCategory.map((item) => item.count) || [],
        backgroundColor: [
          '#FF6384',
          '#36A2EB',
          '#FFCE56',
          '#4BC0C0',
          '#9966FF',
        ],
      },
    ],
  };

  const entriesByDateData = {
    labels: data?.entriesByDate.map((item) => item.date) || [],
    datasets: [
      {
        label: 'Entries',
        data: data?.entriesByDate.map((item) => item.count) || [],
        borderColor: '#36A2EB',
        tension: 0.1,
      },
    ],
  };

  const entriesByTagData = {
    labels: data?.entriesByTag.map((item) => item.tag) || [],
    datasets: [
      {
        label: 'Entries by Tag',
        data: data?.entriesByTag.map((item) => item.count) || [],
        backgroundColor: '#4BC0C0',
      },
    ],
  };

  return (
    <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
      <Box display="flex" justifyContent="space-between" alignItems="center" mb={3}>
        <Typography variant="h4" component="h1">
          Analytics
        </Typography>
        <FormControl sx={{ minWidth: 120 }}>
          <InputLabel>Time Range</InputLabel>
          <Select
            value={timeRange}
            label="Time Range"
            onChange={(e) => setTimeRange(e.target.value)}
          >
            <MenuItem value="7d">Last 7 Days</MenuItem>
            <MenuItem value="30d">Last 30 Days</MenuItem>
            <MenuItem value="90d">Last 90 Days</MenuItem>
            <MenuItem value="all">All Time</MenuItem>
          </Select>
        </FormControl>
      </Box>

      <Grid container spacing={3}>
        {/* Overview Cards */}
        <Grid item xs={12} md={3}>
          <Paper
            sx={{
              p: 2,
              display: 'flex',
              flexDirection: 'column',
              height: 140,
            }}
          >
            <Typography component="h2" variant="h6" color="primary" gutterBottom>
              Total Entries
            </Typography>
            <Typography component="p" variant="h4">
              {data?.totalEntries || 0}
            </Typography>
          </Paper>
        </Grid>
        <Grid item xs={12} md={3}>
          <Paper
            sx={{
              p: 2,
              display: 'flex',
              flexDirection: 'column',
              height: 140,
            }}
          >
            <Typography component="h2" variant="h6" color="primary" gutterBottom>
              Entry Frequency
            </Typography>
            <Typography component="p" variant="h4">
              {data?.averageEntriesPerDay.toFixed(1) || 0}
            </Typography>
          </Paper>
        </Grid>
        <Grid item xs={12} md={3}>
          <Paper
            sx={{
              p: 2,
              display: 'flex',
              flexDirection: 'column',
              height: 140,
            }}
          >
            <Typography component="h2" variant="h6" color="primary" gutterBottom>
              Most Active Day
            </Typography>
            <Typography component="p" variant="h4">
              {data?.mostActiveDay || 'N/A'}
            </Typography>
          </Paper>
        </Grid>
        <Grid item xs={12} md={3}>
          <Paper
            sx={{
              p: 2,
              display: 'flex',
              flexDirection: 'column',
              height: 140,
            }}
          >
            <Typography component="h2" variant="h6" color="primary" gutterBottom>
              Most Used Category
            </Typography>
            <Typography component="p" variant="h4">
              {data?.mostUsedCategory || 'N/A'}
            </Typography>
          </Paper>
        </Grid>

        {/* Charts */}
        <Grid item xs={12} md={6}>
          <Paper sx={{ p: 2, display: 'flex', flexDirection: 'column' }}>
            <Typography component="h2" variant="h6" color="primary" gutterBottom>
              Entries by Category
            </Typography>
            <Box sx={{ height: 300 }}>
              <Doughnut data={entriesByCategoryData} />
            </Box>
          </Paper>
        </Grid>
        <Grid item xs={12} md={6}>
          <Paper sx={{ p: 2, display: 'flex', flexDirection: 'column' }}>
            <Typography component="h2" variant="h6" color="primary" gutterBottom>
              Entries Over Time
            </Typography>
            <Box sx={{ height: 300 }}>
              <Line data={entriesByDateData} />
            </Box>
          </Paper>
        </Grid>
        <Grid item xs={12}>
          <Paper sx={{ p: 2, display: 'flex', flexDirection: 'column' }}>
            <Typography component="h2" variant="h6" color="primary" gutterBottom>
              Entries by Tag
            </Typography>
            <Box sx={{ height: 300 }}>
              <Bar data={entriesByTagData} />
            </Box>
          </Paper>
        </Grid>
      </Grid>
    </Container>
  );
} 