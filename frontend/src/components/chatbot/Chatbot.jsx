
import React, { useState } from 'react';
import {
  TextField,
  Button,
  Box,
  Paper,
  Typography,
  Divider,
  ThemeProvider,
  createTheme,
  CssBaseline,
  CircularProgress,
} from '@mui/material';
import SendIcon from '@mui/icons-material/Send';

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

export default function Component() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  const handleSend = async () => {
    if (input.trim() === '') return;

    const newMessage = {
      text: input,
      from: 'user',
      timestamp: Date.now(),
    };

    setMessages([...messages, newMessage]);
    setInput('');

    setIsLoading(true);

    // Send the user input to an API endpoint and get the LLM response
    try {
      const response = await fetch('/api/chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ userMessage: input }),
      });

      if (!response.ok) {
        throw new Error('Failed to get response from the LLM');
      }

      const data = await response.json();
      const botResponse = {
        text: data.llmOutput || 'No response from the LLM.',
        from: 'bot',
        timestamp: Date.now(),
      };

      setMessages((prevMessages) => [...prevMessages, botResponse]);
    } catch (error) {
      const errorMessage = {
        text: `Error: ${error.message}`,
        from: 'bot',
        timestamp: Date.now(),
      };
      setMessages((prevMessages) => [...prevMessages, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Box
        sx={{
          display: 'flex',
          flexDirection: 'column',
          height: '100vh',
          alignItems: 'center',
          justifyContent: 'center',
          bgcolor: 'background.default',
          p: 2,
        }}
      >
        <Paper
          elevation={3}
          sx={{
            width: '100%',
            maxWidth: 600,
            height: '80vh',
            display: 'flex',
            flexDirection: 'column',
          }}
        >
          <Typography variant="h5" align="center" sx={{ p: 2, bgcolor: 'primary.main', color: 'white' }}>
            Chatbot
          </Typography>
          <Box
            sx={{
              flex: 1,
              overflowY: 'auto',
              p: 2,
              display: 'flex',
              flexDirection: 'column',
              gap: 1,
            }}
          >
            {messages.map((msg, index) => (
              <Box
                key={index}
                sx={{
                  alignSelf: msg.from === 'user' ? 'flex-end' : 'flex-start',
                  bgcolor: msg.from === 'user' ? 'primary.light' : 'grey.200',
                  color: msg.from === 'user' ? 'white' : 'text.primary',
                  p: 1,
                  px: 2,
                  borderRadius: 2,
                  maxWidth: '70%',
                }}
              >
                <Typography variant="body2">{msg.text}</Typography>
                <Typography variant="caption" sx={{ opacity: 0.7 }}>
                  {new Date(msg.timestamp).toLocaleTimeString()}
                </Typography>
              </Box>
            ))}
            {isLoading && (
              <Box sx={{ alignSelf: 'center', mt: 2 }}>
                <CircularProgress />
              </Box>
            )}
          </Box>
          <Divider />
          <Box sx={{ p: 2, display: 'flex', alignItems: 'center', gap: 1 }}>
            <TextField
              placeholder="Type a message"
              variant="outlined"
              fullWidth
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={(e) => e.key === 'Enter' && handleSend()}
              size="small"
            />
            <Button variant="contained" color="primary" endIcon={<SendIcon />} onClick={handleSend}>
              Send
            </Button>
          </Box>
        </Paper>
      </Box>
    </ThemeProvider>
  );
}
