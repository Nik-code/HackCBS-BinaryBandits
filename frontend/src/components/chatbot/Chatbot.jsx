import React, { useState } from 'react';
import { TextField, Button, Box, Paper, Typography, Divider, outlinedInputClasses } from '@mui/material';
import SendIcon from '@mui/icons-material/Send';
import { color } from 'framer-motion';

const Chatbot = () => {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");

  const handleSend = () => {
    if (input.trim() === "") return;

    const newMessage = {
      text: input,
      from: "user",
      timestamp:Date.now()
    };

    setMessages([...messages, newMessage]);
    setInput("");

    // Simulate a bot response after a short delay
    setTimeout(() => {
      const botResponse = {
        text: "This is a bot response.",
        from: "bot",
        timestamp:Date.now()
      };
      setMessages((prevMessages) => [...prevMessages, botResponse]);
    }, 1000);
    console.log(messages);
    
  };

  return (
    <Box sx={{ display: 'flex', flexDirection: 'column', height: '100vh', background:"#aaaaaa",alignItems:"center"}}>
      <Paper elevation={3} sx={{ flex: 1, overflowY: 'auto', padding: 2, margin: 2 , width:"70%"}}>
        <Typography variant="h6" align="center" sx={{ marginBottom: 2 }}>
          Chatbot
        </Typography>
        <Divider sx={{ marginBottom: 2 }} />
        <Box sx={{ display: 'flex', flexDirection: 'column', gap: 1 }}>
          {messages.map((msg, index) => (
            <Box
              key={index}
              sx={{
                alignSelf: msg.from === 'user' ? 'flex-end' : 'flex-start',
                backgroundColor: msg.from === 'user' ? '#c8e6c9' : '#f1f1f1',
                padding: 1,
                borderRadius: 2,
                maxWidth: '100%',
                fontSize:"10rem"
              }}
            >
              <Typography variant="body1">{msg.text}</Typography>
            </Box>
          ))}
        </Box>
      </Paper>
      
      <Box sx={{ padding: 2, display: 'flex', alignItems: 'center', gap: 1 , background:"#2596be",width:"70%",borderRadius:"1.2rem"}}>
        <TextField
          label="Type a message"
          variant="outlined"
          fullWidth
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => e.key === 'Enter' && handleSend()}
            color="#34baeb"
          
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
    </Box>
  );
};

export default Chatbot;
