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
  category: string;
  category_id: number;
  priority: string;
  status: string;
  tags: string[];
  created_at: string;
  updated_at: string;
}

interface Category {
  id: number;
  name: string;
}

interface Tag {
  id: number;
  name: string;
}

export default function Entries() {
  const location = useLocation();
  const navigate = useNavigate();
  const [entries, setEntries] = useState<Entry[]>([]);
  const [categories, setCategories] = useState<Category[]>([]);
  const [tags, setTags] = useState<Tag[]>([]);
  const [open, setOpen] = useState(false);
  const [editingEntry, setEditingEntry] = useState<Entry | null>(null);
  const [formData, setFormData] = useState({
    title: '',
    content: '',
    category_id: 0,
    priority: 'medium',
    status: 'published',
    tags: [] as string[],
  });
  const { user, refreshAuth } = useAuth();
  const [selectedCategory, setSelectedCategory] = useState<string>('all');
  const [selectedTags, setSelectedTags] = useState<string[]>([]);
  const [dateRange, setDateRange] = useState<{
    start: Date | null;
    end: Date | null;
  }>({
    start: null,
    end: null,
  });

  // First useEffect to fetch initial data
  useEffect(() => {
    fetchEntries();
    fetchCategories();
    fetchTags();
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

  const getCategoryName = (categoryId: number) => {
    const category = categories.find(cat => cat.id === categoryId);
    return category ? category.name : '';
  };

  const handleOpen = (entry?: Entry) => {
    fetchCategories();
    fetchTags();
    
    if (entry) {
      setEditingEntry(entry);
      const categoryObj = categories.find(cat => cat.name === entry.category);
      const category_id = categoryObj ? categoryObj.id : 0;
      
      setFormData({
        title: entry.title,
        content: entry.content,
        category_id: category_id,
        priority: entry.priority,
        status: entry.status,
        tags: entry.tags,
      });
    } else {
      setEditingEntry(null);
      setFormData({
        title: '',
        content: '',
        category_id: 0,
        priority: 'medium',
        status: 'published',
        tags: [],
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
      
      console.log('Sending data to backend:', formattedData);
      // Debug token
      const token = localStorage.getItem('token');
      console.log('Token exists:', !!token, 'Token (first 20 chars):', token ? token.substring(0, 20) : 'none');
      
      if (editingEntry) {
        await entriesService.update(editingEntry.id, formattedData);
      } else {
        await entriesService.create(formattedData);
      }
      fetchEntries();
      handleClose();
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

  const handleCategoryChange = (event: SelectChangeEvent) => {
    setSelectedCategory(event.target.value as string);
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
    // Filter by category
    if (selectedCategory !== 'all' && entry.category !== selectedCategory) {
      return false;
    }

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
          <Grid item xs={12} md={3}>
            <FormControl fullWidth>
              <InputLabel>Category</InputLabel>
              <Select
                value={selectedCategory}
                onChange={handleCategoryChange}
                label="Category"
              >
                <MenuItem value="all">All Categories</MenuItem>
                {categories.map((category) => (
                  <MenuItem key={category.id} value={category.name}>
                    {category.name}
                  </MenuItem>
                ))}
              </Select>
            </FormControl>
          </Grid>
          <Grid item xs={12} md={3}>
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
          <Grid item xs={12} md={3}>
            <TextField
              type="date"
              label="Start Date"
              fullWidth
              InputLabelProps={{ shrink: true }}
              value={dateRange.start ? dateRange.start.toISOString().split('T')[0] : ''}
              onChange={handleStartDateChange}
            />
          </Grid>
          <Grid item xs={12} md={3}>
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
                  <TableCell sx={{ 
                    maxWidth: '300px',
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
                  <TableCell>
                    {entry.category || getCategoryName(entry.category_id) || ''}
                  </TableCell>
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
              select
              margin="dense"
              label="Category"
              fullWidth
              value={formData.category_id}
              onChange={(e) =>
                setFormData({ ...formData, category_id: Number(e.target.value) })
              }
            >
              {categories && categories.length > 0 ? (
                categories.map((category) => (
                  <MenuItem key={category.id} value={category.id}>
                    {category.name}
                  </MenuItem>
                ))
              ) : (
                <MenuItem value={0}>No categories available</MenuItem>
              )}
            </TextField>
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