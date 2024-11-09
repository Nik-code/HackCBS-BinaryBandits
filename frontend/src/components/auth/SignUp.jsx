
import { useState } from 'react';
import { Button, Input, Card, CardContent, CardActions, FormLabel, Link, Typography } from "@mui/material";
import { Img } from "react-image";

export default function SignUp() {
  const [activeTab, setActiveTab] = useState("SignUp");
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

  // Handle form submission
  const handleSubmit = async (e) => {
    e.preventDefault();
    const { email, password, firstName, lastName, dateOfBirth, gender, contactNumber, address } = formData;

    try {
        const endpoint = "http://127.0.0.1:8000/api/users/register";
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
              coordinates: address.coordinates
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
        } else {
            console.error("Invalid data or server error.");
        }
    } catch (error) {
        console.error("Error during registration:", error);
    }
};

  return (
    <div className="min-h-screen bg-neutral-50 flex items-center justify-center p-4">
      <Card className="w-full max-w-xl z-10 bg-white/80 backdrop-blur-sm"> {/* Changed max-w-md to max-w-xl */}
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
                <Input id="address.zipCode" value={formData.address.zipCode} onChange={handleChange} fullWidth required />
              </div>
              <div>
                <FormLabel htmlFor="address.country">Country</FormLabel>
                <Input id="address.country" value={formData.address.country} onChange={handleChange} fullWidth required />
              </div>
              <div>
                <FormLabel htmlFor="address.coordinates">Coordinates</FormLabel>
                <Input id="address.coordinates" value={formData.address.coordinates} onChange={handleChange} fullWidth required />
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
            {activeTab === "login" ? (
              <>
                Don't have an account?{" "}
                <Link href="/SignUp" className="text-teal-500 hover:underline" onClick={() => setActiveTab("signup")}>
                  Sign up
                </Link>
              </>
            ) : (
              <>
                Already have an account?{" "}
                <Link href="#" className="text-teal-500 hover:underline" onClick={() => setActiveTab("login")}>
                  Log in
                </Link>
              </>
            )}
          </p>
        </CardActions>
      </Card>
    </div>
  );
}
