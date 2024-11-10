// import React from 'react'
// import {doctorMockData} from './mock_data_doctor'
// import { Card , CardMedia, CardContent, Typography, Button} from '@mui/material';
// import {Box} from '@mui/material';
// import {Slider} from '@mui/material';
// import {FormControl} from '@mui/material';
// import {InputLabel} from '@mui/material';
// import { useState } from 'react';
// import {Select} from '@mui/material';
// import {MenuItem} from '@mui/material';

// function DoctorCard({ doctor }) {
//     return (
//         <div>
//       <Card sx={{ maxWidth: 345, marginBottom: 2, maxHeight:500 }}>
//         <CardMedia
//           component="img"
          
//           image="https://img.freepik.com/premium-vector/doctor-profile-with-medical-service-icon_617655-48.jpg"
//           alt={`${doctor.name}'s photo`}
//           style={{maxHeight:"18rem"}}
          
//         />
//         <CardContent>
//           <Typography variant="h5" component="div">
//             {doctor.name}
//           </Typography>

//           <Typography variant="body2" color="text.secondary">
//             <b className='text-md'>Contact:</b> {doctor.phone}
//           </Typography>

//           <Typography variant="body2" color="text.secondary">
//           <b className='text-md'>Rating:</b> {doctor.rating} ⭐
//           </Typography>

//           <Typography variant="body2" color="text.secondary">
//             <b className='text-md'>Address:</b> {doctor.address}
//           </Typography>

//         </CardContent>
//         <Button size="small" href={doctor.website} target="_blank">
//           Visit Website
//         </Button>
//       </Card>
//       </div>
//     );
//   }
// const DoctorList = () => {

//     const [rating, setRating] = useState([0, 5]); // Default range for the rating slider
//   const [location, setLocation] = useState('');
//   const [filterApplied, setFilterApplied] = useState(false);


//   const handleRatingChange = (event, newValue) => {
//     setRating(newValue);
//   };

//   const handleLocationChange = (event) => {
//     setLocation(event.target.value);
//   };

//   const handleFilterSubmit = () => {
//     setFilterApplied(true);
//     // You can implement the logic to filter the data based on the selected rating and location.
//     console.log('Filter Applied:', { rating, location });
//   };

//   return (
//     <>
//     <h1 className='text-center p-4 text-4xl'>Recommended Doctors</h1>
//       <Typography variant="h5" style={{textAlign:"center", paddingTop:"2rem"}}>Filter Options</Typography>

//       {/* Rating Filter */}
//       <Box sx={{ marginTop: '20px' , marginLeft:"40%"}}>
//         <Typography>Select Rating Range</Typography>
//         <Slider
//           value={rating}
//           onChange={handleRatingChange}
//           valueLabelDisplay="auto"
//           valueLabelFormat={(value) => `${value}★`}
//           min={0}
//           max={5}
//           step={0.1}
//           style={{width:"20rem", display:"flex", alignItems:"center",justifyContent:"center"}}
//         />
//       </Box>

//       {/* Location Filter */}
//       <Box sx={{ marginTop: '20px', maxWidth:"16rem" ,marginLeft:"40%"}}>
//         <FormControl fullWidth>
//           <InputLabel style={{color:"white"}}>Location</InputLabel>
//           <Select value={location} onChange={handleLocationChange} label="Location" color='primary'
//           sx={{
//             '& .MuiOutlinedInput-root': {
//               '& fieldset': { borderColor: 'green' }, // Change the outline (border) color
//             },
//             '&:hover .MuiOutlinedInput-root': {
//               '& fieldset': { borderColor: 'blue' }, // Change border color on hover
//             },
//             '&.Mui-focused .MuiOutlinedInput-root': {
//               '& fieldset': { borderColor: 'purple' }, // Change border color when focused
//             },
//             '& .MuiMenuItem-root': {
//                 color: 'darkgreen',
//             }
//           }}>
//             <MenuItem value="New York">New York</MenuItem>
//             <MenuItem value="Los Angeles">Los Angeles</MenuItem>
//             <MenuItem value="San Francisco">San Francisco</MenuItem>
//             <MenuItem value="Chicago">Chicago</MenuItem>
//             <MenuItem value="Miami">Miami</MenuItem>
//           </Select>
//         </FormControl>
//       </Box>

//       {/* Submit Filter */}
//       <Box sx={{ marginTop: '20px' }}>
//         <Button variant="contained" color="primary" onClick={handleFilterSubmit} style={{marginLeft:"40%"}}>
//           Apply Filter
//         </Button>
//       </Box>

    
//     <div className="grid grid-cols-3 gap-4 p-4">
     
//       {doctorMockData.map((doctor, index) => (
        
//           <DoctorCard doctor={doctor} />
          
    
//       ))}
//       {/* <DoctorCard doctor={doctorMockData[0]}/> */}
      
//     </div>
//     </>
//   )
// }

// export default DoctorList


import React, { useState } from 'react';
import {
  Card,
  CardMedia,
  CardContent,
  Typography,
  Button,
  Box,
  Slider,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Grid,
  Container,
  AppBar,
  Toolbar,
  IconButton,
  Chip,
  Rating,
  ThemeProvider,
  createTheme,
} from '@mui/material';
import { LocalHospital, Phone, Language, LocationOn } from '@mui/icons-material';
import { motion } from 'framer-motion';

// Assuming doctorMockData is imported from './mock_data_doctor'
const doctorMockData = [
  {
    name: "Dr. John Doe",
    phone: "123-456-7890",
    rating: 4.5,
    address: "123 Main St, New York, NY 10001",
    website: "https://example.com",
    specialty: "Cardiologist"
  },
  {
    name: "Dr. Jane Smith",
    phone: "987-654-3210",
    rating: 4.8,
    address: "456 Elm St, Los Angeles, CA 90001",
    website: "https://example.com",
    specialty: "Pediatrician"
  },
  {
    name: "Dr. Mike Johnson",
    phone: "555-123-4567",
    rating: 4.2,
    address: "789 Oak St, Chicago, IL 60601",
    website: "https://example.com",
    specialty: "Dermatologist"
  },
  // Add more mock data as needed
];

const theme = createTheme({
  palette: {
    primary: {
      main: '#1976d2',
    },
    secondary: {
      main: '#f50057',
    },
    background: {
      default: '#e3f2fd',
      paper: '#ffffff',
    },
  },
  typography: {
    fontFamily: 'Roboto, Arial, sans-serif',
  },
  components: {
    MuiSelect: {
      styleOverrides: {
        select: {
          backgroundColor: '#ffffff',
        },
      },
    },
    MuiOutlinedInput: {
      styleOverrides: {
        root: {
          '&:hover .MuiOutlinedInput-notchedOutline': {
            borderColor: '#1976d2',
          },
          '&.Mui-focused .MuiOutlinedInput-notchedOutline': {
            borderColor: '#1976d2',
          },
        },
      },
    },
  },
});

function DoctorCard({ doctor }) {
  const cardVariants = {
    hidden: { opacity: 0, y: 50 },
    visible: { opacity: 1, y: 0, transition: { duration: 0.5 } },
  };

  return (
    <motion.div variants={cardVariants} initial="hidden" animate="visible">
      <Card sx={{ height: '100%', display: 'flex', flexDirection: 'column', boxShadow: 3 }}>
        <CardMedia
          component="img"
          height="200"
          image="https://img.freepik.com/premium-vector/doctor-profile-with-medical-service-icon_617655-48.jpg"
          alt={`${doctor.name}'s photo`}
        />
        <CardContent sx={{ flexGrow: 1 }}>
          <Typography variant="h5" component="div" gutterBottom>
            {doctor.name}
          </Typography>
          <Typography variant="subtitle1" color="text.secondary" gutterBottom>
            {doctor.specialty}
          </Typography>
          <Box display="flex" alignItems="center" mb={1}>
            <Rating name="read-only" value={doctor.rating} readOnly precision={0.5} />
            <Typography variant="body2" color="text.secondary" ml={1}>
              ({doctor.rating})
            </Typography>
          </Box>
          <Box display="flex" alignItems="center" mb={1}>
            <Phone fontSize="small" color="action" />
            <Typography variant="body2" color="text.secondary" ml={1}>
              {doctor.phone}
            </Typography>
          </Box>
          <Box display="flex" alignItems="center">
            <LocationOn fontSize="small" color="action" />
            <Typography variant="body2" color="text.secondary" ml={1}>
              {doctor.address}
            </Typography>
          </Box>
        </CardContent>
        <Box sx={{ p: 2, pt: 0 }}>
          <Button
            variant="contained"
            color="primary"
            fullWidth
            startIcon={<Language />}
            href={doctor.website}
            target="_blank"
          >
            Visit Website
          </Button>
        </Box>
      </Card>
    </motion.div>
  );
}

export default function DoctorList() {
  const [rating, setRating] = useState([0, 5]);
  const [location, setLocation] = useState('');
  const [filterApplied, setFilterApplied] = useState(false);

  const handleRatingChange = (event, newValue) => {
    setRating(newValue);
  };

  const handleLocationChange = (event) => {
    setLocation(event.target.value);
  };

  const handleFilterSubmit = () => {
    setFilterApplied(true);
    console.log('Filter Applied:', { rating, location });
  };

  return (
    <ThemeProvider theme={theme}>
      <Box sx={{ flexGrow: 1, bgcolor: 'background.default', minHeight: '100vh' }}>
        <AppBar position="static" color="primary" elevation={0}>
          <Toolbar>
            <IconButton edge="start" color="inherit" aria-label="menu" sx={{ mr: 2 }}>
              <LocalHospital />
            </IconButton>
            <Typography variant="h6" component="div" sx={{ flexGrow: 1 }} 
            >
              Doctor Finder
            </Typography>
          </Toolbar>
        </AppBar>
        <Container maxWidth="lg" sx={{ mt: 4 }}>
          <Typography variant="h4" gutterBottom align="center" sx={{ color: '#3f51b5' }}>
            Find Your Perfect Doctor
          </Typography>
          <Box sx={{ my: 4, p: 3, bgcolor: 'background.paper', borderRadius: 2, boxShadow: 1 }}>
            <Grid container spacing={4} alignItems="center">
              <Grid item xs={12} md={4}>
                <Typography gutterBottom>Rating Range</Typography>
                <Slider
                  value={rating}
                  onChange={handleRatingChange}
                  valueLabelDisplay="auto"
                  valueLabelFormat={(value) => `${value}★`}
                  min={0}
                  max={5}
                  step={0.5}
                />
              </Grid>
              <Grid item xs={12} md={4}>
                <FormControl fullWidth variant="outlined">
                  <InputLabel>Location</InputLabel>
                  <Select
                    value={location}
                    onChange={handleLocationChange}
                    label="Location"
                    sx={{ bgcolor: 'background.paper' }}
                  >
                    <MenuItem value="New York">New York</MenuItem>
                    <MenuItem value="Los Angeles">Los Angeles</MenuItem>
                    <MenuItem value="San Francisco">San Francisco</MenuItem>
                    <MenuItem value="Chicago">Chicago</MenuItem>
                    <MenuItem value="Miami">Miami</MenuItem>
                  </Select>
                </FormControl>
              </Grid>
              <Grid item xs={12} md={4}>
                <Button
                  variant="contained"
                  color="primary"
                  onClick={handleFilterSubmit}
                  fullWidth
                  size="large"
                >
                  Apply Filter
                </Button>
              </Grid>
            </Grid>
          </Box>
          {filterApplied && (
            <Box sx={{ mb: 2 }}>
              <Typography variant="subtitle1" gutterBottom>
                Applied Filters:
              </Typography>
              <Chip
                label={`Rating: ${rating[0]}★ - ${rating[1]}★`}
                onDelete={() => setRating([0, 5])}
                sx={{ mr: 1, mb: 1 }}
              />
              {location && (
                <Chip label={`Location: ${location}`} onDelete={() => setLocation('')} sx={{ mb: 1 }} />
              )}
            </Box>
          )}
          <Grid container spacing={4}>
            {doctorMockData.map((doctor, index) => (
              <Grid item key={index} xs={12} sm={6} md={4}>
                <DoctorCard doctor={doctor} />
              </Grid>
            ))}
          </Grid>
        </Container>
      </Box>
    </ThemeProvider>
  );
}