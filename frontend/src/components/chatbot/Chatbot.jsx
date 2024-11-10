
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
  const userId = localStorage.getItem("userId");
  const [isLoading, setIsLoading] = useState(false);

  const addBotResponse=async (message,thread_id)=>{
    const input={message,thread_id}
    try{
      const response=await fetch("http://127.0.0.1:8000/api/chat",{
        method:"POST",
        headers: {
          "Content-Type": "application/json"
      },
      body: JSON.stringify({
          message: JSON.stringify(message), // Ensure `userMessage` is defined and in the expected format,
          thread_id:thread_id
      })
      })
      console.log("RES",response)
      if (response.ok) {
        const data = await response.json();
        // Save the token to localStorage (or session storage)
        // localStorage.setItem("token", data.access_token);
        console.log(data);
        localStorage.setItem("thread_id", data.thread_id);
        setTimeout(() => {
          const botResponse = {
            text: data.response,
            from: "bot",
            timestamp: Date.now()
          };
          setMessages((prevMessages) => [...prevMessages, botResponse]);
        }, 1000);
      } else {
        console.log(response)
        console.log("Invalid credentials or server error.");
      }
    }
    catch(error){
      console.log(error);
    }
  }

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
    // setTimeout(() => {
    //   const botResponse = {
    //     text: "This is a bot response.",
    //     from: "bot",
    //     timestamp: Date.now()
    //   };
    //   setMessages((prevMessages) => [...prevMessages, botResponse]);
    // }, 1000);
    addBotResponse(input,localStorage.getItem("thread_id"));
  };

  function formatText(input) {
    // Bold words surrounded by * or ** by replacing with <b> tags
    let formatted = input.replace(/\*\*([^\*]+)\*\*/g, "<b>$1</b>"); // for **bold**
    formatted = formatted.replace(/\*([^\*]+)\*/g, "<b>$1</b>"); // for *bold*

    // Put each list item on a new line for numbered items and bullet points
    formatted = formatted.replace(/(\d+\.)\s/g, "<br/>$1 "); // Numbered lists
    formatted = formatted.replace(/(-)\s/g, "<br/>$1 "); // Bullet points

    return formatted;
}

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
    addBotResponse(`I am just giving you some data as base for further anlysis. My data is this ${JSON.stringify(user_demographic)}. Hi There! lets greet each other`,null)

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
          flexDirection: 'column' ,
          mt:5
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
                {/* <Typography variant="body2">{msg.text}</Typography> */}
                {/* <Typography variant="body2">{formatText(msg.text)}</Typography> */}
                <div dangerouslySetInnerHTML={{__html:formatText(msg.text) }} />
                
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