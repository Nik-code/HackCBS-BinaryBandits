import React from 'react'
import {doctorMockData} from './mock_data_doctor'
import { Card , CardMedia, CardContent, Typography, Button} from '@mui/material';
import {Box} from '@mui/material';
import {Slider} from '@mui/material';
import {FormControl} from '@mui/material';
import {InputLabel} from '@mui/material';
import { useState } from 'react';
import {Select} from '@mui/material';
import {MenuItem} from '@mui/material';

function DoctorCard({ doctor }) {
    return (
        <div>
      <Card sx={{ maxWidth: 345, marginBottom: 2, maxHeight:500 }}>
        <CardMedia
          component="img"
          
          image="https://img.freepik.com/premium-vector/doctor-profile-with-medical-service-icon_617655-48.jpg"
          alt={`${doctor.name}'s photo`}
          style={{maxHeight:"18rem"}}
          
        />
        <CardContent>
          <Typography variant="h5" component="div">
            {doctor.name}
          </Typography>

          <Typography variant="body2" color="text.secondary">
            <b className='text-md'>Contact:</b> {doctor.phone}
          </Typography>

          <Typography variant="body2" color="text.secondary">
          <b className='text-md'>Rating:</b> {doctor.rating} ⭐
          </Typography>

          <Typography variant="body2" color="text.secondary">
            <b className='text-md'>Address:</b> {doctor.address}
          </Typography>

        </CardContent>
        <Button size="small" href={doctor.website} target="_blank">
          Visit Website
        </Button>
      </Card>
      </div>
    );
  }
const DoctorList = () => {

    const [rating, setRating] = useState([0, 5]); // Default range for the rating slider
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
    // You can implement the logic to filter the data based on the selected rating and location.
    console.log('Filter Applied:', { rating, location });
  };

  return (
    <>
    <h1 className='text-center p-4 text-4xl'>Recommended Doctors</h1>
      <Typography variant="h5" style={{textAlign:"center", paddingTop:"2rem"}}>Filter Options</Typography>

      {/* Rating Filter */}
      <Box sx={{ marginTop: '20px' , marginLeft:"40%"}}>
        <Typography>Select Rating Range</Typography>
        <Slider
          value={rating}
          onChange={handleRatingChange}
          valueLabelDisplay="auto"
          valueLabelFormat={(value) => `${value}★`}
          min={0}
          max={5}
          step={0.1}
          style={{width:"20rem", display:"flex", alignItems:"center",justifyContent:"center"}}
        />
      </Box>

      {/* Location Filter */}
      <Box sx={{ marginTop: '20px', maxWidth:"16rem" ,marginLeft:"40%"}}>
        <FormControl fullWidth>
          <InputLabel style={{color:"white"}}>Location</InputLabel>
          <Select value={location} onChange={handleLocationChange} label="Location" color='primary'
          sx={{
            '& .MuiOutlinedInput-root': {
              '& fieldset': { borderColor: 'green' }, // Change the outline (border) color
            },
            '&:hover .MuiOutlinedInput-root': {
              '& fieldset': { borderColor: 'blue' }, // Change border color on hover
            },
            '&.Mui-focused .MuiOutlinedInput-root': {
              '& fieldset': { borderColor: 'purple' }, // Change border color when focused
            },
            '& .MuiMenuItem-root': {
                color: 'darkgreen',
            }
          }}>
            <MenuItem value="New York">New York</MenuItem>
            <MenuItem value="Los Angeles">Los Angeles</MenuItem>
            <MenuItem value="San Francisco">San Francisco</MenuItem>
            <MenuItem value="Chicago">Chicago</MenuItem>
            <MenuItem value="Miami">Miami</MenuItem>
          </Select>
        </FormControl>
      </Box>

      {/* Submit Filter */}
      <Box sx={{ marginTop: '20px' }}>
        <Button variant="contained" color="primary" onClick={handleFilterSubmit} style={{marginLeft:"40%"}}>
          Apply Filter
        </Button>
      </Box>

    
    <div className="grid grid-cols-3 gap-4 p-4">
     
      {doctorMockData.map((doctor, index) => (
        
          <DoctorCard doctor={doctor} />
          
    
      ))}
      {/* <DoctorCard doctor={doctorMockData[0]}/> */}
      
    </div>
    </>
  )
}

export default DoctorList
