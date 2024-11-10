import React, { useContext, useEffect, useState } from 'react';
import { 
  TextField, 
  Button, 
  Box, 
  Paper, 
  Typography, 
  Divider, 
  ThemeProvider, 
  createTheme,
  CssBaseline
} from '@mui/material';
import SendIcon from '@mui/icons-material/Send';
import { stateContext } from '../../context';

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
  const [input, setInput] = useState("");
  // const {userId,setUserId}=useContext(stateContext);
  const userId = localStorage.getItem("userId");

  const handleSend = () => {
    if (input.trim() === "") return;

    const newMessage = {
      text: input,
      from: "user",
      timestamp: Date.now()
    };

    setMessages([...messages, newMessage]);
    setInput("");

    // Simulate a bot response after a short delay
    setTimeout(() => {
      const botResponse = {
        text: "This is a bot response.",
        from: "bot",
        timestamp: Date.now()
      };
      setMessages((prevMessages) => [...prevMessages, botResponse]);
    }, 1000);
  };

  const getUserData=async ()=>{
    try {
      console.log("userId",userId);
      const response=await fetch(`http://127.0.0.1:8000/api/users/${userId}`,
        {
          method:"GET"
        }
      )
      if (response.ok) {
        const data = await response.json();
        console.log(data)
        return data
        // toast.success("User logged in successfully!")
      } else {
        // Handle errors or invalid response
        // toast.error("Wrong email or password")
        console.log("Invalid credentials or server error.");
        return ""
      }
    } catch (error) {
      console.log(error);
      return ""
    }
  }
  useEffect(() => {
    console.log(userId);
    const user_demographic=getUserData();
    // const user_history=getUserHistory();
    // Simulate a bot response after a short delay
    setTimeout(() => {
      const botResponse = {
        text: "This is a bot response.",
        from: "bot",
        timestamp: Date.now()
      };
      setMessages((prevMessages) => [...prevMessages, botResponse]);
    }, 1000);
  }, [])

  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Box sx={{ 
        display: 'flex', 
        flexDirection: 'column', 
        height: '100vh', 
        alignItems: "center", 
        justifyContent: "center", 
        bgcolor: 'background.default', 
        p: 2 
      }}>
        <Paper elevation={3} sx={{ 
          width: '100%', 
          maxWidth: 600, 
          height: '80vh', 
          display: 'flex', 
          flexDirection: 'column' 
        }}>
          <Typography variant="h5" align="center" sx={{ p: 2, bgcolor: 'primary.main', color: 'white' }}>
            Chatbot
          </Typography>
          <Box sx={{ 
            flex: 1, 
            overflowY: 'auto', 
            p: 2, 
            display: 'flex', 
            flexDirection: 'column', 
            gap: 1 
          }}>
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
            <Button
              variant="contained"
              color="primary"
              endIcon={<SendIcon />}
              onClick={handleSend}
            >
              Send
            </Button>
          </Box>
        </Paper>
      </Box>
    </ThemeProvider>
  );
}