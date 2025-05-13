import React, { useState, useEffect, useCallback } from 'react';
import {
  Grid,
  Card,
  CardMedia,
  CardContent,
  Typography,
  Button,
  Container,
  Box,
  IconButton,
  Dialog,
  DialogContent,
} from '@mui/material';
import { Delete as DeleteIcon, Add as AddIcon } from '@mui/icons-material';
import { useNavigate } from 'react-router-dom';

interface Photo {
  id: number;
  filename: string;
  description: string;
  uploaded_at: string;
}

const PhotoGallery: React.FC = () => {
  const [photos, setPhotos] = useState<Photo[]>([]);
  const [selectedPhoto, setSelectedPhoto] = useState<string | null>(null);
  const [uploadDialogOpen, setUploadDialogOpen] = useState(false);
  const navigate = useNavigate();

  const fetchPhotos = useCallback(async () => {
    try {
      const response = await fetch('http://localhost:5001/api/photos/', {
        credentials: 'include',
      });

      if (response.status === 401) {
        navigate('/login');
        return;
      }

      if (!response.ok) {
        throw new Error('Failed to fetch photos');
      }

      const data = await response.json();
      setPhotos(data);
    } catch (error) {
      console.error('Error fetching photos:', error);
    }
  }, [navigate]);

  useEffect(() => {
    fetchPhotos();
  }, [fetchPhotos]);

  const handlePhotoUpload = async (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (!file) return;

    const formData = new FormData();
    formData.append('photo', file);
    formData.append('description', '');

    try {
      const response = await fetch('http://localhost:5001/api/photos/upload', {
        method: 'POST',
        body: formData,
        credentials: 'include',
      });

      if (!response.ok) {
        throw new Error('Failed to upload photo');
      }

      fetchPhotos();
      setUploadDialogOpen(false);
    } catch (error) {
      console.error('Error uploading photo:', error);
    }
  };

  const handleDeletePhoto = async (id: number) => {
    try {
      const response = await fetch(`http://localhost:5001/api/photos/${id}`, {
        method: 'DELETE',
        credentials: 'include',
      });

      if (!response.ok) {
        throw new Error('Failed to delete photo');
      }

      setPhotos(photos.filter(photo => photo.id !== id));
    } catch (error) {
      console.error('Error deleting photo:', error);
    }
  };

  return (
    <Container>
      <Box sx={{ my: 4 }}>
        <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 3 }}>
          <Typography variant="h4" component="h1">
            Photo Gallery
          </Typography>
          <Button
            variant="contained"
            startIcon={<AddIcon />}
            onClick={() => setUploadDialogOpen(true)}
          >
            Upload Photo
          </Button>
        </Box>

        <Grid container spacing={3}>
          {photos.map((photo) => (
            <Grid key={photo.id} sx={{ gridColumn: { xs: 12, sm: 6, md: 4 } }}>
              <Card>
                <CardMedia
                  component="img"
                  height="200"
                  image={`http://localhost:5001/api/photos/${photo.id}`}
                  alt={photo.description || 'Gallery item'}
                  sx={{ cursor: 'pointer', objectFit: 'cover' }}
                  onClick={() => setSelectedPhoto(`http://localhost:5001/api/photos/${photo.id}`)}
                />
                <CardContent sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                  <Typography variant="body2" color="text.secondary">
                    {new Date(photo.uploaded_at).toLocaleDateString()}
                  </Typography>
                  <IconButton
                    onClick={() => handleDeletePhoto(photo.id)}
                    color="error"
                    size="small"
                  >
                    <DeleteIcon />
                  </IconButton>
                </CardContent>
              </Card>
            </Grid>
          ))}
        </Grid>

        <Dialog
          open={uploadDialogOpen}
          onClose={() => setUploadDialogOpen(false)}
          maxWidth="sm"
          fullWidth
        >
          <DialogContent>
            <Box sx={{ textAlign: 'center', py: 2 }}>
              <input
                accept="image/*"
                style={{ display: 'none' }}
                id="photo-upload"
                type="file"
                onChange={handlePhotoUpload}
              />
              <label htmlFor="photo-upload">
                <Button variant="contained" component="span">
                  Choose Photo
                </Button>
              </label>
            </Box>
          </DialogContent>
        </Dialog>

        <Dialog
          open={!!selectedPhoto}
          onClose={() => setSelectedPhoto(null)}
          maxWidth="lg"
          fullWidth
        >
          <DialogContent>
            {selectedPhoto && (
              <img
                src={selectedPhoto}
                alt="Selected gallery item"
                style={{ width: '100%', height: 'auto' }}
              />
            )}
          </DialogContent>
        </Dialog>
      </Box>
    </Container>
  );
};

export default PhotoGallery; 