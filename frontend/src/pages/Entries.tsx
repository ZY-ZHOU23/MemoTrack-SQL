import React, { useState, useEffect } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import {
  Container,
  Paper,
  Typography,
  Button,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  TextField,
  Box,
  IconButton,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Chip,
  MenuItem,
  Grid,
  Select,
  FormControl,
  InputLabel,
  OutlinedInput,
  SelectChangeEvent,
} from '@mui/material';
import { Edit as EditIcon, Delete as DeleteIcon, Add as AddIcon } from '@mui/icons-material';
import { entries as entriesService, categories as categoriesService, tags as tagsService } from '../services/api';
import { useAuth } from '../hooks/useAuth';

interface Entry {
  id: number;
  title: string;
  content: string;
  category?: string;
  category_id?: number;
  priority: string;
  status: string;
  tags: string[];
  created_at: string;
  updated_at: string;
  metrics?: Array<{
    id: number;
    category: string;
    metric_name: string;
    value: number;
    unit?: string;
    entry_id: number;
    created_at: string;
    updated_at: string;
  }>;
}

interface Category {
  id: number;
  name: string;
}

interface Tag {
  id: number;
  name: string;
}

interface EntryFormData {
  title: string;
  content: string;
  category_id?: number;
  priority: string;
  status: string;
  tags: string[];
  created_at: string;
  metrics: Array<{
    category: string;
    metric_name: string;
    value: number;
    unit: string;
  }>;
}

export default function Entries() {
  const location = useLocation();
  const navigate = useNavigate();
  const { user, refreshAuth } = useAuth();
  const [entries, setEntries] = useState<Entry[]>([]);
  const [categories, setCategories] = useState<Category[]>([]);
  const [tags, setTags] = useState<Tag[]>([]);
  const [selectedTags, setSelectedTags] = useState<string[]>([]);
  const [open, setOpen] = useState(false);
  const [editingEntry, setEditingEntry] = useState<Entry | null>(null);
  const [dateRange, setDateRange] = useState<{ start: Date | null, end: Date | null }>({
    start: null,
    end: null
  });
  const [pastMetrics, setPastMetrics] = useState<{
    categories: Record<string, number>,
    metricNames: Record<string, string[]>,
    units: Record<string, string[]>
  }>({
    categories: {},
    metricNames: {},
    units: {}
  });
  const [formData, setFormData] = useState<EntryFormData>({
    title: '',
    content: '',
    priority: 'medium',
    status: 'published',
    tags: [],
    created_at: new Date().toISOString(),
    metrics: []
  });

  // First useEffect to fetch initial data
  useEffect(() => {
    fetchEntries();
    fetchCategories();
    fetchTags();
    fetchPastMetrics();
  }, []);

  // Second useEffect to handle edit parameter after entries are loaded
  useEffect(() => {
    const params = new URLSearchParams(location.search);
    const editId = params.get('edit');
    if (editId && entries.length > 0) {
      const entry = entries.find(e => e.id === parseInt(editId));
      if (entry) {
        handleOpen(entry);
        // Remove the query parameter after opening the dialog
        navigate('/entries', { replace: true });
      }
    }
  }, [location.search, entries]);

  const fetchEntries = async () => {
    try {
      const response = await entriesService.getAll();
      console.log('Entries fetched:', response.data);
      setEntries(response.data);
    } catch (error) {
      console.error('Error fetching entries:', error);
    }
  };

  const fetchCategories = async () => {
    try {
      const response = await categoriesService.getAll();
      console.log('Categories fetched:', response.data);
      setCategories(response.data);
    } catch (error) {
      console.error('Error fetching categories:', error);
    }
  };

  const fetchTags = async () => {
    try {
      const response = await tagsService.getAll();
      setTags(response.data);
    } catch (error) {
      console.error('Error fetching tags:', error);
    }
  };

  const fetchPastMetrics = async () => {
    try {
      // Fetch all entries to extract metrics data
      const response = await entriesService.getAll();
      const entries = response.data;
      
      // Fetch all categories
      const categoriesResponse = await categoriesService.getAll();
      const categoriesList = categoriesResponse.data;
      
      const categories: Record<string, number> = {};
      const metricNames: Record<string, string[]> = {};
      const units: Record<string, string[]> = {};
      
      // Add categories from the Categories component
      categoriesList.forEach((category: Category) => {
        if (!categories.hasOwnProperty(category.name)) {
          categories[category.name] = category.id;
        }
      });
      
      // Extract unique metric categories, names, and units
      entries.forEach((entry: Entry) => {
        if (entry.metrics && entry.metrics.length > 0) {
          entry.metrics.forEach((metric) => {
            // Add category if it doesn't exist
            if (!categories.hasOwnProperty(metric.category)) {
              categories[metric.category] = 0;
            }
            
            // Initialize metricNames for this category if needed
            if (!metricNames.hasOwnProperty(metric.category)) {
              metricNames[metric.category] = [];
            }
            
            // Add metric name if it doesn't exist for this category
            if (!metricNames[metric.category].includes(metric.metric_name)) {
              metricNames[metric.category].push(metric.metric_name);
            }
            
            // Initialize units for this metric name if needed
            const nameKey = `${metric.category}:${metric.metric_name}`;
            if (!units.hasOwnProperty(nameKey)) {
              units[nameKey] = [];
            }
            
            // Add unit if it doesn't exist for this metric name
            if (metric.unit && !units[nameKey].includes(metric.unit)) {
              units[nameKey].push(metric.unit);
            }
          });
        }
      });
      
      setPastMetrics({ categories, metricNames, units });
    } catch (error) {
      console.error('Error fetching past metrics:', error);
    }
  };

  const getCategoryName = (categoryId: number) => {
    const category = categories.find(cat => cat.id === categoryId);
    return category ? category.name : '';
  };

  const handleOpen = (entry?: Entry) => {
    fetchCategories();
    fetchTags();
    fetchPastMetrics();
    
    if (entry) {
      setEditingEntry(entry);
      const categoryObj = categories.find(cat => cat.name === entry.category);
      const category_id = categoryObj ? categoryObj.id : undefined;
      
      // Convert metrics from the entry's format to the form's format
      const entryMetrics = entry.metrics ? entry.metrics.map(metric => ({
        category: metric.category,
        metric_name: metric.metric_name,
        value: metric.value,
        unit: metric.unit || '',
      })) : [];
      
      setFormData({
        title: entry.title,
        content: entry.content,
        category_id: category_id,
        priority: entry.priority,
        status: entry.status,
        tags: entry.tags,
        created_at: entry.created_at,
        metrics: entryMetrics
      });
    } else {
      setEditingEntry(null);
      
      // Check if there are any categories available
      if (categories.length === 0) {
        alert("Please create a category first before adding an entry.");
        setOpen(false);
        return;
      }
      
      setFormData({
        title: '',
        content: '',
        priority: 'medium',
        status: 'published',
        tags: [],
        created_at: new Date().toISOString(),
        metrics: []
      });
    }
    setOpen(true);
  };

  const handleClose = () => {
    setOpen(false);
    setEditingEntry(null);
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      // Ensure tags are properly formatted
      const formattedData = {
        ...formData,
        tags: formData.tags.filter(tag => tag.trim() !== '') // Remove empty tags
      };
      
      console.log('Category ID:', formattedData.category_id);
      console.log('Metrics:', formattedData.metrics);
      console.log('Sending data to backend:', formattedData);
      // Debug token
      const token = localStorage.getItem('token');
      console.log('Token exists:', !!token, 'Token (first 20 chars):', token ? token.substring(0, 20) : 'none');
      
      if (editingEntry) {
        await entriesService.update(editingEntry.id, formattedData);
      } else {
        await entriesService.create(formattedData);
      }
      
      // First close the dialog
      handleClose();
      
      // Then fetch updated entries
      fetchEntries();
    } catch (error) {
      console.error('Error saving entry:', error);
    }
  };

  const handleDelete = async (id: number) => {
    if (window.confirm('Are you sure you want to delete this entry?')) {
      try {
        await entriesService.delete(id);
        fetchEntries();
      } catch (error) {
        console.error('Error deleting entry:', error);
      }
    }
  };

  const handleTagsChange = (event: SelectChangeEvent<string[]>) => {
    const value = event.target.value;
    setSelectedTags(typeof value === 'string' ? value.split(',') : value);
  };

  const handleStartDateChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const date = event.target.value ? new Date(event.target.value) : null;
    setDateRange(prev => ({ ...prev, start: date }));
  };

  const handleEndDateChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const date = event.target.value ? new Date(event.target.value) : null;
    setDateRange(prev => ({ ...prev, end: date }));
  };

  const filteredEntries = entries.filter((entry) => {
    // Filter by tags
    if (selectedTags.length > 0) {
      const hasAllSelectedTags = selectedTags.every(tag => 
        entry.tags.includes(tag)
      );
      if (!hasAllSelectedTags) {
        return false;
      }
    }

    // Filter by date range
    if (dateRange.start || dateRange.end) {
      const entryDate = new Date(entry.created_at);
      if (dateRange.start && entryDate < dateRange.start) {
        return false;
      }
      if (dateRange.end) {
        const endOfDay = new Date(dateRange.end);
        endOfDay.setHours(23, 59, 59, 999);
        if (entryDate > endOfDay) {
          return false;
        }
      }
    }

    return true;
  });

  // Add metric to form
  const addMetric = () => {
    setFormData({
      ...formData,
      metrics: [
        ...formData.metrics,
        {
          category: '',
          metric_name: '',
          value: 0,
          unit: ''
        }
      ]
    });
  };

  // Get metric names for a given category
  const getMetricNamesForCategory = (category: string) => {
    return pastMetrics.metricNames[category] || [];
  };

  // Get units for a given metric name
  const getUnitsForMetricName = (category: string, metricName: string) => {
    const nameKey = `${category}:${metricName}`;
    return pastMetrics.units[nameKey] || [];
  };

  // Remove metric from form
  const removeMetric = (index: number) => {
    const updatedMetrics = [...formData.metrics];
    updatedMetrics.splice(index, 1);
    setFormData({
      ...formData,
      metrics: updatedMetrics
    });
  };

  // Update a metric field
  const updateMetric = (index: number, field: string, value: string | number) => {
    const updatedMetrics = [...formData.metrics];
    updatedMetrics[index] = {
      ...updatedMetrics[index],
      [field]: value
    };
    setFormData({
      ...formData,
      metrics: updatedMetrics
    });
  };

  const renderCategoryName = (entry: Entry) => {
    return entry.category || 'None';
  };

  return (
    <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
      <Box display="flex" justifyContent="space-between" alignItems="center" mb={3}>
        <Typography variant="h4" component="h1">
          Memo Entries
        </Typography>
        <Button
          variant="contained"
          color="primary"
          startIcon={<AddIcon />}
          onClick={() => handleOpen()}
        >
          New Entry
        </Button>
      </Box>

      {/* Filter Controls */}
      <Paper sx={{ p: 2, mb: 3 }}>
        <Grid container spacing={3} alignItems="center">
          <Grid item xs={12} md={4}>
            <FormControl fullWidth>
              <InputLabel>Tags</InputLabel>
              <Select
                multiple
                value={selectedTags}
                onChange={handleTagsChange}
                input={<OutlinedInput label="Tags" />}
                renderValue={(selected) => (
                  <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 0.5 }}>
                    {selected.map((value) => (
                      <Chip key={value} label={value} size="small" />
                    ))}
                  </Box>
                )}
              >
                {Array.from(new Set(entries.flatMap(entry => entry.tags))).map((tag) => (
                  <MenuItem key={tag} value={tag}>
                    {tag}
                  </MenuItem>
                ))}
              </Select>
            </FormControl>
          </Grid>
          <Grid item xs={12} md={4}>
            <TextField
              type="date"
              label="Start Date"
              fullWidth
              InputLabelProps={{ shrink: true }}
              value={dateRange.start ? dateRange.start.toISOString().split('T')[0] : ''}
              onChange={handleStartDateChange}
            />
          </Grid>
          <Grid item xs={12} md={4}>
            <TextField
              type="date"
              label="End Date"
              fullWidth
              InputLabelProps={{ shrink: true }}
              value={dateRange.end ? dateRange.end.toISOString().split('T')[0] : ''}
              onChange={handleEndDateChange}
            />
          </Grid>
        </Grid>
      </Paper>

      <TableContainer component={Paper}>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell>Title</TableCell>
              <TableCell>Content</TableCell>
              <TableCell>Category</TableCell>
              <TableCell>Tags</TableCell>
              <TableCell>Created At</TableCell>
              <TableCell>Actions</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {filteredEntries.length > 0 ? (
              filteredEntries.map((entry) => (
                <TableRow key={entry.id}>
                  <TableCell>{entry.title}</TableCell>
                  <TableCell>{entry.content.substring(0, 50)}...</TableCell>
                  <TableCell>{renderCategoryName(entry)}</TableCell>
                  <TableCell>
                    {entry.tags && Array.isArray(entry.tags) && entry.tags.length > 0 ? (
                      entry.tags.map((tag) => (
                        <Chip
                          key={tag}
                          label={tag}
                          size="small"
                          sx={{ mr: 0.5, mb: 0.5 }}
                        />
                      ))
                    ) : null}
                  </TableCell>
                  <TableCell>
                    {new Date(entry.created_at).toLocaleDateString()}
                  </TableCell>
                  <TableCell>
                    <IconButton
                      color="primary"
                      onClick={() => handleOpen(entry)}
                    >
                      <EditIcon />
                    </IconButton>
                    <IconButton
                      color="error"
                      onClick={() => handleDelete(entry.id)}
                    >
                      <DeleteIcon />
                    </IconButton>
                  </TableCell>
                </TableRow>
              ))
            ) : (
              <TableRow>
                <TableCell colSpan={6}>No entries found</TableCell>
              </TableRow>
            )}
          </TableBody>
        </Table>
      </TableContainer>

      <Dialog open={open} onClose={handleClose} maxWidth="md" fullWidth>
        <DialogTitle>
          {editingEntry ? 'Edit Entry' : 'New Entry'}
        </DialogTitle>
        <form onSubmit={handleSubmit}>
          <DialogContent>
            <TextField
              autoFocus
              margin="dense"
              label="Title"
              fullWidth
              value={formData.title}
              onChange={(e) =>
                setFormData({ ...formData, title: e.target.value })
              }
            />
            <TextField
              margin="dense"
              label="Content"
              fullWidth
              multiline
              rows={4}
              value={formData.content}
              onChange={(e) =>
                setFormData({ ...formData, content: e.target.value })
              }
            />
            <TextField
              margin="dense"
              label="Tags (comma-separated)"
              fullWidth
              value={(formData.tags && Array.isArray(formData.tags)) ? formData.tags.join(', ') : ''}
              onChange={(e) =>
                setFormData({
                  ...formData,
                  tags: e.target.value.split(',').map((tag) => tag.trim()),
                })
              }
            />
            <TextField
              type="datetime-local"
              margin="dense"
              label="Creation Date"
              fullWidth
              InputLabelProps={{ shrink: true }}
              value={formData.created_at ? new Date(formData.created_at).toISOString().slice(0, 16) : ''}
              onChange={(e) =>
                setFormData({
                  ...formData,
                  created_at: e.target.value ? new Date(e.target.value).toISOString() : new Date().toISOString(),
                })
              }
            />
            
            {/* Metrics Section */}
            <Box sx={{ mt: 3, mb: 2 }}>
              <Typography variant="h6" gutterBottom>
                Metrics
              </Typography>
              
              {/* Metrics List */}
              {formData.metrics.map((metric, index) => (
                <Box key={index} sx={{ mb: 2, p: 2, border: '1px solid #e0e0e0', borderRadius: 1 }}>
                  <Grid container spacing={2} alignItems="center">
                    <Grid item xs={12} sm={4}>
                      <TextField
                        select={categories.length > 0}
                        fullWidth
                        label="Category"
                        value={metric.category}
                        onChange={(e) => updateMetric(index, 'category', e.target.value)}
                      >
                        {/* Show all available categories */}
                        {categories.map(cat => (
                          <MenuItem key={cat.id} value={cat.name}>{cat.name}</MenuItem>
                        ))}
                        {/* Allow custom category input if not in the list */}
                        {metric.category && !categories.map(c => c.name).includes(metric.category) && (
                          <MenuItem value={metric.category}>{metric.category}</MenuItem>
                        )}
                        {/* Custom option */}
                        <MenuItem value="__custom">
                          <TextField
                            placeholder="Add custom category"
                            value={metric.category === '__custom' ? '' : ''}
                            onChange={(e) => {
                              e.stopPropagation();
                              updateMetric(index, 'category', e.target.value);
                            }}
                            onClick={(e) => e.stopPropagation()}
                            fullWidth
                            size="small"
                          />
                        </MenuItem>
                      </TextField>
                    </Grid>
                    <Grid item xs={12} sm={3}>
                      <TextField
                        select={getMetricNamesForCategory(metric.category).length > 0}
                        fullWidth
                        label="Metric Name"
                        value={metric.metric_name}
                        onChange={(e) => updateMetric(index, 'metric_name', e.target.value)}
                      >
                        {/* Show metric names for the selected category */}
                        {getMetricNamesForCategory(metric.category).map(name => (
                          <MenuItem key={name} value={name}>{name}</MenuItem>
                        ))}
                        {/* Allow custom metric name input if not in the list */}
                        {metric.metric_name && !getMetricNamesForCategory(metric.category).includes(metric.metric_name) && (
                          <MenuItem value={metric.metric_name}>{metric.metric_name}</MenuItem>
                        )}
                        {/* Only show custom option if there are predefined options */}
                        {getMetricNamesForCategory(metric.category).length > 0 && (
                          <MenuItem value="__custom">
                            <TextField
                              placeholder="Add custom metric name"
                              value={metric.metric_name === '__custom' ? '' : metric.metric_name}
                              onChange={(e) => {
                                e.stopPropagation();
                                updateMetric(index, 'metric_name', e.target.value);
                              }}
                              onClick={(e) => e.stopPropagation()}
                              fullWidth
                              size="small"
                            />
                          </MenuItem>
                        )}
                      </TextField>
                    </Grid>
                    <Grid item xs={12} sm={2}>
                      <TextField
                        fullWidth
                        label="Value"
                        type="number"
                        value={metric.value}
                        onChange={(e) => updateMetric(index, 'value', parseFloat(e.target.value))}
                      />
                    </Grid>
                    <Grid item xs={12} sm={2}>
                      <TextField
                        select={getUnitsForMetricName(metric.category, metric.metric_name).length > 0}
                        fullWidth
                        label="Unit (optional)"
                        value={metric.unit || ''}
                        onChange={(e) => updateMetric(index, 'unit', e.target.value)}
                      >
                        <MenuItem value="">None</MenuItem>
                        {/* Show units for the selected metric name */}
                        {getUnitsForMetricName(metric.category, metric.metric_name).map(unit => (
                          <MenuItem key={unit} value={unit}>{unit}</MenuItem>
                        ))}
                        {/* Allow custom unit input if not in the list */}
                        {metric.unit && !getUnitsForMetricName(metric.category, metric.metric_name).includes(metric.unit) && (
                          <MenuItem value={metric.unit}>{metric.unit}</MenuItem>
                        )}
                        {/* Only show custom option if there are predefined options */}
                        {getUnitsForMetricName(metric.category, metric.metric_name).length > 0 && (
                          <MenuItem value="__custom">
                            <TextField
                              placeholder="Add custom unit"
                              value={metric.unit === '__custom' ? '' : ''}
                              onChange={(e) => {
                                e.stopPropagation();
                                updateMetric(index, 'unit', e.target.value);
                              }}
                              onClick={(e) => e.stopPropagation()}
                              fullWidth
                              size="small"
                            />
                          </MenuItem>
                        )}
                      </TextField>
                    </Grid>
                    <Grid item xs={12} sm={1}>
                      <IconButton color="error" onClick={() => removeMetric(index)}>
                        <DeleteIcon />
                      </IconButton>
                    </Grid>
                  </Grid>
                </Box>
              ))}
              
              {/* Add Metric Button */}
              <Button 
                variant="outlined" 
                startIcon={<AddIcon />}
                onClick={addMetric}
                sx={{ mt: 1 }}
              >
                Add Metric
              </Button>
            </Box>
          </DialogContent>
          <DialogActions>
            <Button onClick={handleClose}>Cancel</Button>
            <Button type="submit" variant="contained" color="primary">
              {editingEntry ? 'Update' : 'Create'}
            </Button>
          </DialogActions>
        </form>
      </Dialog>
    </Container>
  );
} 