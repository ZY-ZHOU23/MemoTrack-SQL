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
  TablePagination,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  ToggleButtonGroup,
  ToggleButton,
} from '@mui/material';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  Title,
  Tooltip as ChartTooltip,
  Legend,
  ArcElement,
  TimeScale,
} from 'chart.js';
import { Line, Doughnut, Bar, Scatter } from 'react-chartjs-2';
import 'chartjs-adapter-date-fns';
import { analytics } from '../services/api';
import { useAuth } from '../hooks/useAuth';

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  Title,
  ChartTooltip,
  Legend,
  ArcElement,
  TimeScale
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

interface MetricData {
  metric_name: string;
  avg_value: number;
  min_value: number;
  max_value: number;
  count: number;
  unit: string;
}

interface CategoryMetrics {
  category: string;
  metrics: MetricData[];
}

interface MetricsByCategory {
  metrics_by_category: CategoryMetrics[];
}

interface MetricValue {
  id: number;
  value: number;
  unit: string;
  created_at: string;
}

interface MetricValues {
  metric_values: {
    [category: string]: {
      [metricName: string]: MetricValue[];
    };
  };
}

export default function Dashboard() {
  const [stats, setStats] = useState<DashboardStats | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const { user } = useAuth();
  const navigate = useNavigate();
  
  // Add pagination state
  const [page, setPage] = useState(0);
  const [rowsPerPage, setRowsPerPage] = useState(5);
  
  // Add metrics state
  const [metricsData, setMetricsData] = useState<MetricsByCategory | null>(null);
  const [loadingMetrics, setLoadingMetrics] = useState(true);
  const [selectedCategory, setSelectedCategory] = useState<string>('');
  const [metricViewType, setMetricViewType] = useState<'average' | 'min' | 'max'>('average');
  
  // Add raw metric values state
  const [metricValues, setMetricValues] = useState<MetricValues | null>(null);
  const [loadingMetricValues, setLoadingMetricValues] = useState(true);
  const [selectedMetricName, setSelectedMetricName] = useState<string>('');
  const [chartType, setChartType] = useState<'scatter' | 'line'>('scatter');

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

    const fetchMetricsData = async () => {
      try {
        setLoadingMetrics(true);
        const response = await analytics.getMetricsByCategory();
        console.log('Metrics by category response:', response.data);
        setMetricsData(response.data);
        
        // Set default selected category if available
        if (response.data.metrics_by_category && response.data.metrics_by_category.length > 0) {
          setSelectedCategory(response.data.metrics_by_category[0].category);
        }
      } catch (error: any) {
        console.error('Error fetching metrics data:', error);
      } finally {
        setLoadingMetrics(false);
      }
    };

    const fetchMetricValues = async () => {
      try {
        setLoadingMetricValues(true);
        const response = await analytics.getMetricValues();
        console.log('Metric values response:', response.data);
        setMetricValues(response.data);
      } catch (error: any) {
        console.error('Error fetching metric values:', error);
      } finally {
        setLoadingMetricValues(false);
      }
    };

    fetchDashboardStats();
    fetchMetricsData();
    fetchMetricValues();
  }, []);

  // Effect to set default selected metric name when category changes
  useEffect(() => {
    if (metricValues?.metric_values && selectedCategory) {
      const categoryMetrics = metricValues.metric_values[selectedCategory];
      if (categoryMetrics) {
        const metricNames = Object.keys(categoryMetrics);
        if (metricNames.length > 0) {
          setSelectedMetricName(metricNames[0]);
        } else {
          setSelectedMetricName('');
        }
      }
    }
  }, [selectedCategory, metricValues]);

  const handleEntryDoubleClick = (entryId: number) => {
    navigate(`/entries?edit=${entryId}`);
  };

  const handleChangePage = (
    event: React.MouseEvent<HTMLButtonElement> | null,
    newPage: number,
  ) => {
    setPage(newPage);
  };

  const handleChangeRowsPerPage = (
    event: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>,
  ) => {
    setRowsPerPage(parseInt(event.target.value, 10));
    setPage(0);
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

  // Prepare metrics chart data
  const getSelectedCategoryData = () => {
    if (!metricsData || !selectedCategory) return null;
    
    const categoryData = metricsData.metrics_by_category.find(
      item => item.category === selectedCategory
    );
    
    return categoryData;
  };
  
  const getMetricsChartData = () => {
    const categoryData = getSelectedCategoryData();
    if (!categoryData) return null;
    
    const valueKey = metricViewType === 'average' ? 'avg_value' : 
                    metricViewType === 'min' ? 'min_value' : 'max_value';
    
    return {
      labels: categoryData.metrics.map(m => m.metric_name),
      datasets: [
        {
          label: `${metricViewType} value`,
          data: categoryData.metrics.map(m => m[valueKey]),
          backgroundColor: [
            '#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0', '#9966FF',
            '#FF9F40', '#8EB695', '#4D5360', '#7B68EE'
          ],
          borderWidth: 1,
        },
      ],
    };
  };

  // Get available metric names for selected category
  const getMetricNamesForCategory = () => {
    if (!metricValues?.metric_values || !selectedCategory) return [];
    
    const categoryMetrics = metricValues.metric_values[selectedCategory];
    return categoryMetrics ? Object.keys(categoryMetrics) : [];
  };
  
  // Get metric values for selected category and metric name
  const getMetricValues = () => {
    if (!metricValues?.metric_values || !selectedCategory || !selectedMetricName) return [];
    
    const categoryMetrics = metricValues.metric_values[selectedCategory];
    if (!categoryMetrics) return [];
    
    return categoryMetrics[selectedMetricName] || [];
  };
  
  // Prepare raw metric values chart data
  const getMetricValuesChartData = () => {
    const values = getMetricValues();
    if (values.length === 0) return null;
    
    // Get the unit from the first value (assuming consistent units)
    const unit = values[0].unit || '';
    
    if (chartType === 'scatter') {
      return {
        datasets: [{
          label: `${selectedMetricName} (${unit})`,
          data: values.map(v => ({
            x: new Date(v.created_at),
            y: v.value
          })),
          backgroundColor: '#36A2EB',
          pointRadius: 6,
          pointHoverRadius: 8,
        }]
      };
    } else {
      // Line chart for trends
      return {
        labels: values.map(v => new Date(v.created_at)),
        datasets: [{
          label: `${selectedMetricName} (${unit})`,
          data: values.map(v => v.value),
          borderColor: '#36A2EB',
          backgroundColor: 'rgba(54, 162, 235, 0.2)',
          tension: 0.1,
          fill: true,
        }]
      };
    }
  };
  
  const getChartOptions = () => {
    const values = getMetricValues();
    const unit = values.length > 0 ? values[0].unit || '' : '';
    
    return {
      responsive: true,
      scales: {
        x: {
          type: 'time',
          time: {
            unit: 'day',
            tooltipFormat: 'PP',
          },
          title: {
            display: true,
            text: 'Date'
          }
        },
        y: {
          title: {
            display: true,
            text: unit ? `Value (${unit})` : 'Value'
          }
        }
      },
      plugins: {
        tooltip: {
          callbacks: {
            label: (context: any) => {
              const value = chartType === 'scatter' 
                ? context.raw.y 
                : context.raw;
              return `${selectedMetricName}: ${value} ${unit}`;
            }
          }
        }
      }
    };
  };

  return (
    <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
      <Grid container spacing={3}>
        {/* Recent Entries - Moved to the top */}
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
                  {stats?.recentEntries
                    .slice(page * rowsPerPage, page * rowsPerPage + rowsPerPage)
                    .map((entry) => (
                    <Tooltip key={entry.id} title="Double click to edit" arrow placement="top">
                      <TableRow 
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
              <TablePagination
                component="div"
                count={stats?.recentEntries.length || 0}
                page={page}
                onPageChange={handleChangePage}
                rowsPerPage={rowsPerPage}
                onRowsPerPageChange={handleChangeRowsPerPage}
                rowsPerPageOptions={[5, 10, 25]}
              />
            </Box>
          </Paper>
        </Grid>

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

        {/* Metrics Visualization Section */}
        <Grid item xs={12}>
          <Paper sx={{ p: 2, display: 'flex', flexDirection: 'column' }}>
            <Typography component="h2" variant="h6" color="primary" gutterBottom>
              Metrics Visualization
            </Typography>
            
            {loadingMetrics ? (
              <Box sx={{ display: 'flex', justifyContent: 'center', p: 3 }}>
                <CircularProgress />
              </Box>
            ) : metricsData && metricsData.metrics_by_category && metricsData.metrics_by_category.length > 0 ? (
              <>
                <Grid container spacing={2} sx={{ mb: 3 }}>
                  <Grid item xs={12} sm={6}>
                    <FormControl fullWidth>
                      <InputLabel>Category</InputLabel>
                      <Select
                        value={selectedCategory}
                        label="Category"
                        onChange={(e) => setSelectedCategory(e.target.value)}
                      >
                        {metricsData.metrics_by_category.map((category) => (
                          <MenuItem key={category.category} value={category.category}>
                            {category.category}
                          </MenuItem>
                        ))}
                      </Select>
                    </FormControl>
                  </Grid>
                  <Grid item xs={12} sm={6}>
                    <FormControl fullWidth>
                      <InputLabel>View Type</InputLabel>
                      <Select
                        value={metricViewType}
                        label="View Type"
                        onChange={(e) => setMetricViewType(e.target.value as 'average' | 'min' | 'max')}
                      >
                        <MenuItem value="average">Average Value</MenuItem>
                        <MenuItem value="min">Minimum Value</MenuItem>
                        <MenuItem value="max">Maximum Value</MenuItem>
                      </Select>
                    </FormControl>
                  </Grid>
                </Grid>
                
                <Box sx={{ height: 300 }}>
                  {getMetricsChartData() ? (
                    <Bar data={getMetricsChartData() as any} />
                  ) : (
                    <Typography align="center">No metrics data available for this category</Typography>
                  )}
                </Box>
                
                {getSelectedCategoryData() && (
                  <Box sx={{ mt: 2 }}>
                    <Typography variant="subtitle2" gutterBottom>
                      Metrics Details for {selectedCategory}
                    </Typography>
                    <Table size="small">
                      <TableHead>
                        <TableRow>
                          <TableCell>Metric Name</TableCell>
                          <TableCell>Average Value</TableCell>
                          <TableCell>Min Value</TableCell>
                          <TableCell>Max Value</TableCell>
                          <TableCell>Count</TableCell>
                          <TableCell>Unit</TableCell>
                        </TableRow>
                      </TableHead>
                      <TableBody>
                        {getSelectedCategoryData()?.metrics.map((metric) => (
                          <TableRow key={metric.metric_name}>
                            <TableCell>{metric.metric_name}</TableCell>
                            <TableCell>{metric.avg_value.toFixed(2)}</TableCell>
                            <TableCell>{metric.min_value.toFixed(2)}</TableCell>
                            <TableCell>{metric.max_value.toFixed(2)}</TableCell>
                            <TableCell>{metric.count}</TableCell>
                            <TableCell>{metric.unit}</TableCell>
                          </TableRow>
                        ))}
                      </TableBody>
                    </Table>
                  </Box>
                )}
              </>
            ) : (
              <Typography align="center" sx={{ p: 3 }}>
                No metrics data available. Add metrics to your entries to see visualizations.
              </Typography>
            )}
          </Paper>
        </Grid>

        {/* Raw Metrics Visualization Section */}
        <Grid item xs={12}>
          <Paper sx={{ p: 2, display: 'flex', flexDirection: 'column' }}>
            <Typography component="h2" variant="h6" color="primary" gutterBottom>
              Raw Metric Values Visualization
            </Typography>
            
            {loadingMetricValues ? (
              <Box sx={{ display: 'flex', justifyContent: 'center', p: 3 }}>
                <CircularProgress />
              </Box>
            ) : metricValues && metricValues.metric_values && Object.keys(metricValues.metric_values).length > 0 ? (
              <>
                <Grid container spacing={2} sx={{ mb: 3 }}>
                  <Grid item xs={12} sm={4}>
                    <FormControl fullWidth>
                      <InputLabel>Category</InputLabel>
                      <Select
                        value={selectedCategory}
                        label="Category"
                        onChange={(e) => setSelectedCategory(e.target.value)}
                      >
                        {Object.keys(metricValues.metric_values).map((category) => (
                          <MenuItem key={category} value={category}>
                            {category}
                          </MenuItem>
                        ))}
                      </Select>
                    </FormControl>
                  </Grid>
                  <Grid item xs={12} sm={4}>
                    <FormControl fullWidth>
                      <InputLabel>Metric Name</InputLabel>
                      <Select
                        value={selectedMetricName}
                        label="Metric Name"
                        onChange={(e) => setSelectedMetricName(e.target.value)}
                        disabled={getMetricNamesForCategory().length === 0}
                      >
                        {getMetricNamesForCategory().map((name) => (
                          <MenuItem key={name} value={name}>
                            {name}
                          </MenuItem>
                        ))}
                      </Select>
                    </FormControl>
                  </Grid>
                  <Grid item xs={12} sm={4}>
                    <ToggleButtonGroup
                      value={chartType}
                      exclusive
                      onChange={(e, newValue) => {
                        if (newValue) setChartType(newValue);
                      }}
                      aria-label="chart type"
                      sx={{ height: '100%' }}
                    >
                      <ToggleButton value="scatter" aria-label="scatter plot">
                        Scatter Plot
                      </ToggleButton>
                      <ToggleButton value="line" aria-label="line chart">
                        Trend Line
                      </ToggleButton>
                    </ToggleButtonGroup>
                  </Grid>
                </Grid>
                
                <Box sx={{ height: 400 }}>
                  {getMetricValuesChartData() ? (
                    chartType === 'scatter' ? (
                      <Scatter 
                        data={getMetricValuesChartData() as any}
                        options={getChartOptions() as any}
                      />
                    ) : (
                      <Line 
                        data={getMetricValuesChartData() as any}
                        options={getChartOptions() as any}
                      />
                    )
                  ) : (
                    <Typography align="center">No metric values available for this selection</Typography>
                  )}
                </Box>
                
                {getMetricValues().length > 0 && (
                  <Box sx={{ mt: 2 }}>
                    <Typography variant="subtitle2" gutterBottom>
                      Individual Values for {selectedCategory} - {selectedMetricName}
                    </Typography>
                    <Box sx={{ maxHeight: 200, overflow: 'auto' }}>
                      <Table size="small">
                        <TableHead>
                          <TableRow>
                            <TableCell>Date</TableCell>
                            <TableCell>Value</TableCell>
                            <TableCell>Unit</TableCell>
                          </TableRow>
                        </TableHead>
                        <TableBody>
                          {getMetricValues().map((metric) => (
                            <TableRow key={metric.id}>
                              <TableCell>{new Date(metric.created_at).toLocaleString()}</TableCell>
                              <TableCell>{metric.value}</TableCell>
                              <TableCell>{metric.unit}</TableCell>
                            </TableRow>
                          ))}
                        </TableBody>
                      </Table>
                    </Box>
                  </Box>
                )}
              </>
            ) : (
              <Typography align="center" sx={{ p: 3 }}>
                No metric values available. Add metrics to your entries to see raw value visualizations.
              </Typography>
            )}
          </Paper>
        </Grid>
      </Grid>
    </Container>
  );
} 