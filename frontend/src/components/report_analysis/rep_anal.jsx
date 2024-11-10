import React, { useState } from 'react';
import {
  Box,
  Button,
  Container,
  Paper,
  Typography,
  TextField,
  CircularProgress,
  List,
  ListItem,
  ListItemText,
  ThemeProvider,
  createTheme,
  CssBaseline,
} from '@mui/material';
import { CloudUpload, Send } from '@mui/icons-material';

const theme = createTheme({
  palette: {
    primary: {
      main: '#2596be',
    },
    background: {
      default: '#f0f2f5',
    },
  },
});

export default function Analysis() {
  const [files, setFiles] = useState([]);
  const [llmOutput, setLlmOutput] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  const handleFileUpload = (event) => {
    setFiles(Array.from(event.target.files));
  };

  const handleSubmit = async () => {
    setIsLoading(true);
    setLlmOutput(''); // Clear previous output
    const formData = new FormData();

    files.forEach((file) => {
      formData.append('files', file);
    });

    try {
      const response = await fetch('https://your-api-endpoint.com/upload', {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        throw new Error('Failed to upload files');
      }

      const data = await response.json();
      setLlmOutput(data.llmOutput || 'No output received from the server.');
    } catch (error) {
      setLlmOutput(`Error: ${error.message}`);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Container maxWidth="md" >
        <Box >
          <Typography variant="h4" component="h1" gutterBottom align="center" className="pt-20">
            AI Powered Report Analysis
          </Typography>
          <Paper elevation={3} sx={{ p: 3, mt: 4 }}>
            <Box sx={{ display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 2 }}>
              <Button
                variant="contained"
                component="label"
                startIcon={<CloudUpload />}
              >
                Upload Files
                <input
                  type="file"
                  hidden
                  multiple
                  onChange={handleFileUpload}
                />
              </Button>
              {files.length > 0 && (
                <List>
                  {files.map((file, index) => (
                    <ListItem key={index}>
                      <ListItemText primary={file.name} secondary={`${(file.size / 1024).toFixed(2)} KB`} />
                    </ListItem>
                  ))}
                </List>
              )}
              <Button
                variant="contained"
                color="primary"
                onClick={handleSubmit}
                disabled={files.length === 0 || isLoading}
                startIcon={<Send />}
              >
                Process Files
              </Button>
            </Box>
          </Paper>
          {isLoading && (
            <Box sx={{ display: 'flex', justifyContent: 'center', mt: 4 }}>
              <CircularProgress />
            </Box>
          )}
          {llmOutput && (
            <Paper elevation={3} sx={{ p: 3, mt: 4 }}>
              <Typography variant="h6" gutterBottom>
                Analyzed report
              </Typography>
              <TextField
                multiline
                fullWidth
                rows={6}
                value={llmOutput}
                variant="outlined"
                InputProps={{
                  readOnly: true,
                }}
              />
            </Paper>
          )}
        </Box>
      </Container>
    </ThemeProvider>
  );
}
