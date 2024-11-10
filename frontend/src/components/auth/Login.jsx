import { useState,useContext, useEffect } from 'react';
import { Button, Input, Card, CardContent, CardHeader,CardActions, FormLabel, Link, Tabs, Tab , Typography} from "@mui/material";
import { Img } from "react-image";
import { motion } from "framer-motion";
import { stateContext } from './../../context';
import { ToastContainer, toast } from 'react-toastify';
import { useNavigate } from "react-router-dom";
import 'react-toastify/dist/ReactToastify.css';

export default function LoginPage() {
  // toast.configure({
  //   autoClose: 3000,
  //   draggable: false,
  //   style: {
  //     width: '300px',
  //     fontSize: '14px',
  //   },
  // });
  const [activeTab, setActiveTab] = useState("login");
  const [formData, setFormData] = useState({
    email: "",
    password: "",
  });
  const navigate = useNavigate();
  // const[userId,setUserId]=useState();
  const {userId,setUserId}=useContext(stateContext);

  // Handle input change
  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.id]: e.target.value,
    });
  };

  // Handle form submission
  const handleSubmit = async (e) => {
    e.preventDefault();
    const email = formData.email;
    const password = formData.password;

    if(userId){
      toast.info("user already logged in!");
      console.log("Already logged in!");
      navigate("/");
      return
    }

    try {
      // Create form data
      const formDataToSend = new URLSearchParams();
      formDataToSend.append('email', email);
      formDataToSend.append('password', password);
      const formData={
        email,password
      };

      // Send POST request to FastAPI login endpoint
      const response = await fetch("http://127.0.0.1:8000/api/users/login", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        // body: formDataToSend.toString(), // Send the form data as a string
        body: JSON.stringify(formData)
     });

      if (response.ok) {
        const data = await response.json();
        // Save the token to localStorage (or session storage)
        // localStorage.setItem("token", data.access_token);
        setUserId(data.userId);
        toast.success("User logged in successfully!")
        // Redirect to another page or fetch user data
        // For example:
        // window.location.href = "/dashboard.html";
      } else {
        // Handle errors or invalid response
        toast.error("Wrong email or password")
        console.log("Invalid credentials or server error.");
      }
    } catch (error) {
      toast.error("Error in operation")
      console.error("Error during login:", error);
    }

  };

  return (
    <>
    <ToastContainer />
    
    <div className="min-h-screen bg-neutral-50 flex items-center justify-center p-4">
      <div className="absolute inset-0 overflow-hidden z-0">
        <motion.div
          className="absolute top-1/4 left-1/4 w-72 h-72 bg-teal-200 rounded-full mix-blend-multiply filter blur-xl opacity-70"
          animate={{
            scale: [1, 1.2, 1],
            x: [0, 50, 0],
            y: [0, 30, 0],
          }}
          transition={{
            duration: 8,
            repeat: Infinity,
            ease: "easeInOut",
          }}
        />
        <motion.div
          className="absolute top-1/3 right-1/4 w-96 h-96 bg-emerald-200 rounded-full mix-blend-multiply filter blur-xl opacity-70"
          animate={{
            scale: [1.2, 1, 1.2],
            x: [0, -30, 0],
            y: [0, 50, 0],
          }}
          transition={{
            duration: 10,
            repeat: Infinity,
            ease: "easeInOut",
          }}
        />
        <motion.div
          className="absolute bottom-1/4 left-1/3 w-80 h-80 bg-cyan-200 rounded-full mix-blend-multiply filter blur-xl opacity-70"
          animate={{
            scale: [1, 1.1, 1],
            x: [0, 40, 0],
            y: [0, -30, 0],
          }}
          transition={{
            duration: 9,
            repeat: Infinity,
            ease: "easeInOut",
          }}
        />
      </div>

      
      <Card className="w-full max-w-md z-10 bg-white/80 backdrop-blur-sm">
        <div>
        {/* <CardHeader className="space-y-1"> */}
          <div className="flex items-center justify-center mb-4">
            <Img 
              src="https://hebbkx1anhila5yf.public.blob.vercel-storage.com/CuraNet_Logo-v2ODPLpANeEXfPECK6GjnRCoVodV4z.png"
              alt="CuraNet Logo"
              className="w-auto h-12"
              height={100}
              width={199}
              style={{paddingTop:'0.5rem'}}
            />
          </div>
          <Typography className="text-2xl font-bold text-center text-neutral-800">Welcome to CuraNet</Typography>
          <CardContent className="text-center text-neutral-600">
            Your AI-Powered Healthcare Companion
          </CardContent>
        {/* </CardHeader> */}
        </div>
        

        <CardContent>
              <form onSubmit={handleSubmit}>
                <div className="space-y-4">
                  <div className="space-y-2">
                    <FormLabel htmlFor="email">Email</FormLabel>
                    <Input
                      id="email"
                      type="email"
                      placeholder="m@example.com"
                      required
                      value={formData.email}
                      onChange={handleChange}
                      style={{marginLeft:"2.8rem"}}
                    />
                  </div>
                  <div className="space-y-2">
                    <FormLabel htmlFor="password">Password</FormLabel>
                    <Input
                      id="password"
                      type="password"
                      required
                      value={formData.password}
                      onChange={handleChange}
                      style={{marginLeft:"1rem"}}
                    />
                  </div>
                  <Button className="w-full bg-teal-400 hover:bg-teal-500 text-white" type="submit">
                    Log In
                  </Button>
                </div>
              </form>
        </CardContent>

        <CardActions>
          <p className="text-sm text-center w-full text-neutral-600">
                Don't have an account?{" "}
                <a href="/signup" className="text-teal-500 hover:underline">
                  Sign up
                </a>
          </p>
        </CardActions>
      </Card>
    </div>
    </>
  );
}

