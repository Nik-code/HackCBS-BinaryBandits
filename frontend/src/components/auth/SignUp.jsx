
import { useContext, useState } from 'react';
import { Button, Input, Card, CardContent, CardActions, FormLabel, Link, Typography } from "@mui/material";
import { Img } from "react-image";
import { stateContext } from '../../context';
import { useNavigate } from 'react-router-dom';
import { ToastContainer, toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';

export default function SignUp() {
  // toast.configure({
  //   autoClose: 3000,
  //   draggable: false,
  //   style: {
  //     width: '300px',
  //     fontSize: '14px',
  //   },
  // });
  const [activeTab, setActiveTab] = useState("SignUp");
  // const {userId,setUserId}=useContext(stateContext);
  const [formData, setFormData] = useState({
    email: "",
    password: "",
    firstName: "",
    lastName: "",
    dateOfBirth: "",
    gender: "",
    contactNumber: "",
    address: {
      street: "",
      city: "",
      state: "",
      zipCode: "",
      country: "",
      coordinates: "",
    },
  });
const getCoordinates=async (location)=>{
  fetch(`https://api.opencagedata.com/geocode/v1/json?q=${location}&key=2140484258db4f4883e08c2ca82e059a`)
  .then(response => {
    if (!response.ok) {
      throw new Error('Network response was not ok ' + response.statusText);
    }
    return response.json();  // parse JSON response
  })
  .then(data => {
    console.log(data.results[0].annotations.DMS)
    return data.results[0].annotations.DMS;
  })
  .catch(error => {
    toast.error("We have an error")
    console.error('There was a problem with the fetch operation:', error);
  });
}
  // Handle input change
  const handleChange = (e) => {
    const { id, value } = e.target;
    if (id.includes("address.")) {
      setFormData({
        ...formData,
        address: {
          ...formData.address,
          [id.split(".")[1]]: value,
        },
      });
    } else {
      setFormData({
        ...formData,
        [id]: value,
      });
    }
  };
  const navigate=useNavigate();
  // Handle form submission
  const handleSubmit = async (e) => {
    e.preventDefault();
    const { email, password, firstName, lastName, dateOfBirth, gender, contactNumber, address } = formData;
    if (localStorage.getItem("userId")) {
        console.log("User is logged in with userId:", userId);
        toast.info("User is already logged in")
        // Use the userId as needed
        navigate("/");
        return
    }
    try {
        const endpoint = "http://127.0.0.1:8000/api/users/register";
        const coordinates=getCoordinates(`${address.street} ${address.city}, ${address.state}`)
        const strCoordinates=`${coordinates.lat} ${coordinates.lng}`
        const formDataToSend = {
          profile:{
            firstName,
            lastName,
            dateOfBirth,
            gender,
            contactNumber,
            address: {
              street: address.street,
              city: address.city,
              state: address.state,
              zipCode: address.zipCode,
              country: address.country,
              coordinates: strCoordinates
          }
          },
            email,
            // password,
            passwordHash:password,
            currentDiseases:[]
            
           
        };

        const response = await fetch(endpoint, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(formDataToSend)
        });

        if (response.ok) {
            alert("Registration successful! Please log in.");
            setActiveTab("login");
            const data = await response.json();
            // setUserId(data.userId);
            localStorage.setItem("userId", data.userId)
            console.log("REG IN ID",localStorage.getItem("userId"));
            toast.success("Registeration Done!");
        } else {
            toast.error("Invalid data or server error.");
            console.error("Invalid data or server error.");
        }
    } catch (error) {
        toast.error("Error during registration.");
        console.error("Error during registration:", error);
    }
};


  return (
    <>
    <ToastContainer />
    
    <div className="min-h-screen bg-neutral-50 flex items-center justify-center p-4">
      <Card className="w-full max-w-xl z-10 bg-white/80 backdrop-blur-sm mt-15"> {/* Changed max-w-md to max-w-xl */}
        <div className="flex items-center justify-center mb-4">
          <Img
            src="https://hebbkx1anhila5yf.public.blob.vercel-storage.com/CuraNet_Logo-v2ODPLpANeEXfPECK6GjnRCoVodV4z.png"
            alt="CuraNet Logo"
            className="w-auto h-12"
            height={100}
            width={199}
            style={{ paddingTop: '0.5rem' }}
          />
        </div>
        <Typography className="text-2xl font-bold text-center text-neutral-800">Welcome to CuraNet</Typography>
        <CardContent className="text-center text-neutral-600">
          Your AI-Powered Healthcare Companion
        </CardContent>
        
        <CardContent>
          <form onSubmit={handleSubmit}>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {/* Basic Info Fields */}
              <div>
                <FormLabel htmlFor="firstName">First Name</FormLabel>
                <Input id="firstName" value={formData.firstName} onChange={handleChange} fullWidth required />
              </div>
              <div>
                <FormLabel htmlFor="lastName">Last Name</FormLabel>
                <Input id="lastName" value={formData.lastName} onChange={handleChange} fullWidth required />
              </div>
              <div>
                <FormLabel htmlFor="dateOfBirth">Date of Birth</FormLabel>
                <Input id="dateOfBirth" type="date" value={formData.dateOfBirth} onChange={handleChange} fullWidth required />
              </div>
              <div>
                <FormLabel htmlFor="gender">Gender</FormLabel>
                <Input id="gender" value={formData.gender} onChange={handleChange} fullWidth required />
              </div>
              <div>
                <FormLabel htmlFor="contactNumber">Contact Number</FormLabel>
                <Input id="contactNumber" value={formData.contactNumber} onChange={handleChange} fullWidth required />
              </div>

              {/* Address Fields */}
              <div>
                <FormLabel htmlFor="address.street">Street</FormLabel>
                <Input id="address.street" value={formData.address.street} onChange={handleChange} fullWidth required />
              </div>
              <div>
                <FormLabel htmlFor="address.city">City</FormLabel>
                <Input id="address.city" value={formData.address.city} onChange={handleChange} fullWidth required />
              </div>
              <div>
                <FormLabel htmlFor="address.state">State</FormLabel>
                <Input id="address.state" value={formData.address.state} onChange={handleChange} fullWidth required />
              </div>
              <div>
                <FormLabel htmlFor="address.zipCode">Zip Code</FormLabel>
                <Input id="address.zipCode" type="number" value={formData.address.zipCode} onChange={handleChange} fullWidth required />
              </div>
              <div>
                <FormLabel htmlFor="address.country">Country</FormLabel>
                <Input id="address.country" value={formData.address.country} onChange={handleChange} fullWidth required />
              </div>
              <div>
                {/* <FormLabel htmlFor="address.coordinates">Coordinates</FormLabel> */}
                <Input id="address.coordinates" type="hidden" value={formData.address.coordinates} onChange={handleChange} />
              </div>

              {/* Email and Password */}
              <div className="col-span-2">
                <FormLabel htmlFor="email">Email</FormLabel>
                <Input id="email" type="email" value={formData.email} onChange={handleChange} fullWidth required />
              </div>
              <div className="col-span-2">
                <FormLabel htmlFor="password">Password</FormLabel>
                <Input id="password" type="password" value={formData.password} onChange={handleChange} fullWidth required />
              </div>

              <Button className="w-full bg-teal-400 hover:bg-teal-500 text-white col-span-2" type="submit">
                Sign Up
              </Button>
            </div>
          </form>
        </CardContent>

        <CardActions>
          <p className="text-sm text-center w-full text-neutral-600">
            
             
                Already have an account?{" "}
                <a href="/login" className="text-teal-500 hover:underline">
                  Log in
                </a>
            
            
          </p>
        </CardActions>
      </Card>
    </div>
    </>
  );
}
