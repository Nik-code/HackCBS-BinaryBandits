import React, { useState } from 'react';
import FormControl from '@mui/material/FormControl';
import TextField from '@mui/material/TextField';
import Button from '@mui/material/Button';
import '../../../public/styles/login.css';
import { InputAdornment,IconButton } from '@mui/material';
import {Visibility,VisibilityOff} from '@mui/icons-material'
const Login = () => {
  // State to hold form data
  const [formData, setFormData] = useState({ email: '', password: '' });
  const [showPassword, setShowPassword] = useState(false);

  const handleTogglePasswordVisibility = () => {
    setShowPassword(!showPassword);
  };
  
  // Handle form submission
  const handleSubmit = async (e) => {
    e.preventDefault();
    // console.log("Form Submitted:", formData);
    const username=formData.email
    const password=formData.password
    // Add your form submission logic here, like sending the data to an API

    try {
      // Send POST request to FastAPI login endpoint
      const response = await fetch("http://127.0.0.1:8000/token", {
          method: "POST",
          body: `username:${username}&password:${password}`
      });

      // Handle the response
      if (response.ok) {
          const data = await response.json();
          message.textContent = "Login successful!";
          message.style.color = "green";

          // Save the token to localStorage (or session storage)
          localStorage.setItem("token", data.access_token);

          // Redirect to another page or fetch user data
          // For example:
          // window.location.href = "/dashboard.html";
      } else {
          message.textContent = "Invalid username or password";
          message.style.color = "red";
      }
  } catch (error) {
      message.textContent = "An error occurred. Please try again.";
      message.style.color = "red";
  }

  };

  // Handle input changes
  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData((prevData) => ({
      ...prevData,
      [name]: value,
    }));
  };

  return (
    <div className="form-holder">
      <h2> Login </h2>
      <form onSubmit={handleSubmit}>
        <FormControl fullWidth margin="normal" size="medium" color="info">
          <TextField
            required
            name="email"
            label="Email"
            type="text"
            autoComplete="email"
            value={formData.email}
            onChange={handleInputChange}
            fullWidth
          />
        </FormControl>

        <FormControl fullWidth margin="normal" size="medium" color="info">
          <TextField
            required
            name="password"
            label="Password"
            type={showPassword?"password":"text"}
            autoComplete="current-password"
            value={formData.password}
            onChange={handleInputChange}
            fullWidth
            InputProps={{
              endAdornment: (
                <InputAdornment position="end">
                  <IconButton
                    onClick={handleTogglePasswordVisibility}
                    edge="end"
                    aria-label="toggle password visibility"
                  >
                    {showPassword ? <VisibilityOff /> : <Visibility />}
                  </IconButton>
                </InputAdornment>
              ),
            }}
          />
        </FormControl>

        <Button
          type="submit"
          variant="contained"
          color="primary"
          fullWidth
          style={{ marginTop: '1rem', borderRadius:'2rem',padding:'1rem' ,fontSize:'1rem'}}
        >
          Submit
        </Button>
      </form>
    </div>
  );
};

export default Login;
