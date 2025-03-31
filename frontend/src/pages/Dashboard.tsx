import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Container,
  Grid,
  Paper,
  Typography,
  Box,
  CircularProgress,
  Table,
  TableHead,
  TableBody,
  TableRow,
  TableCell,
  Tooltip,
} from '@mui/material';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip as ChartTooltip,
  Legend,
  ArcElement,
} from 'chart.js';
import { Line, Doughnut } from 'react-chartjs-2';
import { analytics } from '../services/api';
import { useAuth } from '../hooks/useAuth';

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  ChartTooltip,
  Legend,
  ArcElement
);

interface DashboardStats {
  totalEntries: number;
  totalCategories: number;
  totalTags: number;
  recentEntries: Array<{
    id: number;
    title: string;
    content: string;
    created_at: string;
  }>;
  entriesByCategory: Array<{
    category: string;
    count: number;
  }>;
  entriesByDate: Array<{
    date: string;
    count: number;
  }>;
}

export default function Dashboard() {
  const [stats, setStats] = useState<DashboardStats | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const { user } = useAuth();
  const navigate = useNavigate();

  useEffect(() => {
    const fetchDashboardStats = async () => {
      try {
        console.log('Fetching dashboard stats...');
        const response = await analytics.getDashboard();
        
        console.log('Dashboard API response:', response.data);
        setStats(response.data);
        setError(null);
      } catch (error: any) {
        console.error('Error fetching dashboard stats:', error);
        setError(error.response?.data?.detail || 'Failed to load dashboard data');
        setStats({
          totalEntries: 0,
          totalCategories: 0,
          totalTags: 0,
          recentEntries: [],
          entriesByCategory: [],
          entriesByDate: []
        });
      } finally {
        setLoading(false);
      }
    };

    fetchDashboardStats();
  }, []);

  const handleEntryDoubleClick = (entryId: number) => {
    navigate(`/entries?edit=${entryId}`);
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
    labels: stats?.entriesByCategory.map((item) => item.category) || [],
    datasets: [
      {
        data: stats?.entriesByCategory.map((item) => item.count) || [],
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
    labels: stats?.entriesByDate.map((item) => item.date) || [],
    datasets: [
      {
        label: 'Entries',
        data: stats?.entriesByDate.map((item) => item.count) || [],
        borderColor: '#36A2EB',
        tension: 0.1,
      },
    ],
  };

  return (
    <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
      <Grid container spacing={3}>
        {/* Overview Cards */}
        <Grid item xs={12} md={4}>
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
              {stats?.totalEntries || 0}
            </Typography>
          </Paper>
        </Grid>
        <Grid item xs={12} md={4}>
          <Paper
            sx={{
              p: 2,
              display: 'flex',
              flexDirection: 'column',
              height: 140,
            }}
          >
            <Typography component="h2" variant="h6" color="primary" gutterBottom>
              Categories
            </Typography>
            <Typography component="p" variant="h4">
              {stats?.totalCategories || 0}
            </Typography>
          </Paper>
        </Grid>
        <Grid item xs={12} md={4}>
          <Paper
            sx={{
              p: 2,
              display: 'flex',
              flexDirection: 'column',
              height: 140,
            }}
          >
            <Typography component="h2" variant="h6" color="primary" gutterBottom>
              Tags
            </Typography>
            <Typography component="p" variant="h4">
              {stats?.totalTags || 0}
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

        {/* Recent Entries */}
        <Grid item xs={12}>
          <Paper sx={{ p: 2, display: 'flex', flexDirection: 'column' }}>
            <Typography component="h2" variant="h6" color="primary" gutterBottom>
              Recent Entries
            </Typography>
            <Box sx={{ overflowX: 'auto' }}>
              <Table size="medium">
                <TableHead>
                  <TableRow>
                    <TableCell width="25%" sx={{ fontWeight: 'bold' }}>Title</TableCell>
                    <TableCell width="15%" sx={{ fontWeight: 'bold' }}>Created At</TableCell>
                    <TableCell width="60%" sx={{ fontWeight: 'bold' }}>Content</TableCell>
                  </TableRow>
                </TableHead>
                <TableBody>
                  {stats?.recentEntries.map((entry) => (
                    <Tooltip title="Double click to edit" arrow placement="top">
                      <TableRow 
                        key={entry.id}
                        onDoubleClick={() => handleEntryDoubleClick(entry.id)}
                        sx={{
                          cursor: 'pointer',
                          '&:hover': {
                            backgroundColor: 'rgba(0, 0, 0, 0.04)',
                          },
                          transition: 'background-color 0.2s ease',
                        }}
                      >
                        <TableCell>{entry.title}</TableCell>
                        <TableCell>{new Date(entry.created_at).toLocaleDateString()}</TableCell>
                        <TableCell sx={{
                          maxWidth: '600px',
                          whiteSpace: 'nowrap',
                          overflow: 'hidden',
                          textOverflow: 'ellipsis',
                          '&:hover': {
                            whiteSpace: 'normal',
                            overflow: 'visible',
                            backgroundColor: 'rgba(0, 0, 0, 0.04)',
                          }
                        }}>
                          {entry.content}
                        </TableCell>
                      </TableRow>
                    </Tooltip>
                  ))}
                </TableBody>
              </Table>
            </Box>
          </Paper>
        </Grid>
      </Grid>
    </Container>
  );
} 