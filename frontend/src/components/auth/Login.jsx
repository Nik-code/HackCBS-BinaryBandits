// import React, { useState } from 'react';
// import FormControl from '@mui/material/FormControl';
// import TextField from '@mui/material/TextField';
// import Button from '@mui/material/Button';
// import '../../../public/styles/login.css';
// import { InputAdornment,IconButton } from '@mui/material';
// import {Visibility,VisibilityOff} from '@mui/icons-material'
// const Login = () => {
//   // State to hold form data
//   const [formData, setFormData] = useState({ email: '', password: '' });
//   const [showPassword, setShowPassword] = useState(false);

//   const handleTogglePasswordVisibility = () => {
//     setShowPassword(!showPassword);
//   };
  
//   // Handle form submission
//   const handleSubmit = async (e) => {
//     e.preventDefault();
//     const username = formData.email;
//     const password = formData.password;

//     try {
//       // Create form data
//       const formDataToSend = new URLSearchParams();
//       formDataToSend.append('username', username);
//       formDataToSend.append('password', password);

//       // Send POST request to FastAPI login endpoint
//       const response = await fetch("http://127.0.0.1:8000/token", {
//         method: "POST",
//         headers: {
//           "Content-Type": "application/x-www-form-urlencoded",
//         },
//         body: formDataToSend.toString(), // Send the form data as a string
//       });

//       if (response.ok) {
//           const data = await response.json();
//           // Save the token to localStorage (or session storage)
//           localStorage.setItem("token", data.access_token);
//           // Redirect to another page or fetch user data
//           // For example:
//           // window.location.href = "/dashboard.html";
//       } else {
//           // Handle errors or invalid response
//           console.error("Invalid credentials or server error.");
//       }
//     } catch (error) {
//       console.error("Error during login:", error);
//     }
// };


//   // Handle input changes
//   const handleInputChange = (e) => {
//     const { name, value } = e.target;
//     setFormData((prevData) => ({
//       ...prevData,
//       [name]: value,
//     }));
//   };

//   return (
//     <div className="form-holder">
//       <h2> Login </h2>
//       <form onSubmit={handleSubmit}>
//         <FormControl fullWidth margin="normal" size="medium" color="info">
//           <TextField
//             required
//             name="email"
//             FormInputLabel="Email"
//             type="text"
//             autoComplete="email"
//             value={formData.email}
//             onChange={handleInputChange}
//             fullWidth
//           />
//         </FormControl>

//         <FormControl fullWidth margin="normal" size="medium" color="info">
//           <TextField
//             required
//             name="password"
//             FormInputLabel="Password"
//             type={showPassword?"password":"text"}
//             autoComplete="current-password"
//             value={formData.password}
//             onChange={handleInputChange}
//             fullWidth
//             InputProps={{
//               endAdornment: (
//                 <InputAdornment position="end">
//                   <IconButton
//                     onClick={handleTogglePasswordVisibility}
//                     edge="end"
//                     aria-FormInputLabel="toggle password visibility"
//                   >
//                     {showPassword ? <VisibilityOff /> : <Visibility />}
//                   </IconButton>
//                 </InputAdornment>
//               ),
//             }}
//           />
//         </FormControl>

//         <Button
//           type="submit"
//           variant="contained"
//           color="primary"
//           fullWidth
//           style={{ marginTop: '1rem', borderRadius:'2rem',padding:'1rem' ,fontSize:'1rem'}}
//         >
//           Submit
//         </Button>
//       </form>
//     </div>
//   );
// };

// export default Login;






// import { useState } from 'react'
// import { Button } from "@mui/material"
// import { Input } from "@mui/material";
// import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@mui/material";
// import { Tabs, Tab, TabPanel, TabList, TabPanels } from "@mui/material";
// import { FormInputLabel } from "@mui/material";

// // import Image from "next/image"
// import Link from '@mui/material/Link';
// import {Img} from "react-image"
// // import { motion } from "framer-motion"
// import { motion } from "framer-motion"

// export default function LoginPage() {
//   const [activeTab, setActiveTab] = useState("login")
//   const [formData, setFormData] = useState({
//     email: "",
//     password: ""
//   })
  
//   // Handle input change
//   const handleChange = (e) => {
//     setFormData({
//       ...formData,
//       [e.target.id]: e.target.value
//     })
//   }

//   // Handle form submission
//   const handleSubmit = async (e) => {
//     e.preventDefault();
//     const username = formData.email;
//     const password = formData.password;

//     try {
//       // Create form data
//       const formDataToSend = new URLSearchParams();
//       formDataToSend.append('username', username);
//       formDataToSend.append('password', password);

//       // Send POST request to FastAPI login endpoint
//       const response = await fetch("http://127.0.0.1:8000/token", {
//         method: "POST",
//         headers: {
//           "Content-Type": "application/x-www-form-urlencoded",
//         },
//         body: formDataToSend.toString(), // Send the form data as a string
//       });

//       if (response.ok) {
//         const data = await response.json();
//         // Save the token to localStorage (or session storage)
//         localStorage.setItem("token", data.access_token);
//         // Redirect to another page or fetch user data
//         // For example:
//         // window.location.href = "/dashboard.html";
//       } else {
//         // Handle errors or invalid response
//         console.error("Invalid credentials or server error.");
//       }
//     } catch (error) {
//       console.error("Error during login:", error);
//     }
//   }

//   return (
//     <div className="min-h-screen bg-neutral-50 flex items-center justify-center p-4">
//       <div className="absolute inset-0 overflow-hidden z-0">
//         <motion.div
//           className="absolute top-1/4 left-1/4 w-72 h-72 bg-teal-200 rounded-full mix-blend-multiply filter blur-xl opacity-70"
//           animate={{
//             scale: [1, 1.2, 1],
//             x: [0, 50, 0],
//             y: [0, 30, 0],
//           }}
//           transition={{
//             duration: 8,
//             repeat: Infinity,
//             ease: "easeInOut",
//           }}
//         />
//         <motion.div
//           className="absolute top-1/3 right-1/4 w-96 h-96 bg-emerald-200 rounded-full mix-blend-multiply filter blur-xl opacity-70"
//           animate={{
//             scale: [1.2, 1, 1.2],
//             x: [0, -30, 0],
//             y: [0, 50, 0],
//           }}
//           transition={{
//             duration: 10,
//             repeat: Infinity,
//             ease: "easeInOut",
//           }}
//         />
//         <motion.div
//           className="absolute bottom-1/4 left-1/3 w-80 h-80 bg-cyan-200 rounded-full mix-blend-multiply filter blur-xl opacity-70"
//           animate={{
//             scale: [1, 1.1, 1],
//             x: [0, 40, 0],
//             y: [0, -30, 0],
//           }}
//           transition={{
//             duration: 9,
//             repeat: Infinity,
//             ease: "easeInOut",
//           }}
//         />
//       </div>

//       <Card className="w-full max-w-md z-10 bg-white/80 backdrop-blur-sm">
//         <CardHeader className="space-y-1">
//           <div className="flex items-center justify-center mb-4">
//           <Img 
//             src="https://hebbkx1anhila5yf.public.blob.vercel-storage.com/CuraNet_Logo-v2ODPLpANeEXfPECK6GjnRCoVodV4z.png"
//             alt="CuraNet Logo"
//             className="w-auto h-12"
//           />

//           </div>
//           <CardTitle className="text-2xl font-bold text-center text-neutral-800">Welcome to CuraNet</CardTitle>
//           <CardDescription className="text-center text-neutral-600">
//             Your AI-Powered Healthcare Companion
//           </CardDescription>
//         </CardHeader>
//         <CardContent>
//           <Tabs defaultValue="login" className="w-full" onValueChange={setActiveTab}>
//             <TabsList className="grid w-full grid-cols-2 mb-4">
//               <TabsTrigger value="login">Log In</TabsTrigger>
//               <TabsTrigger value="signup">Sign Up</TabsTrigger>
//             </TabsList>
//             <TabsContent value="login">
//               <form onSubmit={handleSubmit}>
//                 <div className="space-y-4">
//                   <div className="space-y-2">
//                     <FormInputLabel htmlFor="email">Email</FormInputLabel>
//                     <Input 
//                       id="email" 
//                       type="email" 
//                       placeholder="m@example.com" 
//                       required 
//                       value={formData.email}
//                       onChange={handleChange}
//                     />
//                   </div>
//                   <div className="space-y-2">
//                     <FormInputLabel htmlFor="password">Password</FormInputLabel>
//                     <Input 
//                       id="password" 
//                       type="password" 
//                       required 
//                       value={formData.password}
//                       onChange={handleChange}
//                     />
//                   </div>
//                   <Button 
//                     className="w-full bg-teal-400 hover:bg-teal-500 text-white"
//                     type="submit"
//                   >
//                     Log In
//                   </Button>
//                 </div>
//               </form>
//             </TabsContent>
//             <TabsContent value="signup">
//               <form>
//                 <div className="space-y-4">
//                   <div className="space-y-2">
//                     <FormInputLabel htmlFor="signup-name">Full Name</FormInputLabel>
//                     <Input id="signup-name" type="text" required />
//                   </div>
//                   <div className="space-y-2">
//                     <FormInputLabel htmlFor="signup-email">Email</FormInputLabel>
//                     <Input id="signup-email" type="email" placeholder="m@example.com" required />
//                   </div>
//                   <div className="space-y-2">
//                     <FormInputLabel htmlFor="signup-password">Password</FormInputLabel>
//                     <Input id="signup-password" type="password" required />
//                   </div>
//                   <Button className="w-full bg-teal-400 hover:bg-teal-500 text-white">
//                     Sign Up
//                   </Button>
//                 </div>
//               </form>
//             </TabsContent>
//           </Tabs>
//         </CardContent>
//         <CardFooter>
//           <p className="text-sm text-center w-full text-neutral-600">
//             {activeTab === "login" ? (
//               <>
//                 Don't have an account?{" "}
//                 <Link href="#" className="text-teal-500 hover:underline" onClick={() => setActiveTab("signup")}>
//                   Sign up
//                 </Link>
//               </>
//             ) : (
//               <>
//                 Already have an account?{" "}
//                 <Link href="#" className="text-teal-500 hover:underline" onClick={() => setActiveTab("login")}>
//                   Log in
//                 </Link>
//               </>
//             )}
//           </p>
//         </CardFooter>
//       </Card>
//     </div>
//   )
// }





import { useState } from 'react';
import { Button, Input, Card, CardContent, CardHeader,CardActions, FormLabel, Link, Tabs, Tab , Typography} from "@mui/material";
import { Img } from "react-image";
import { motion } from "framer-motion";

export default function LoginPage() {
  const [activeTab, setActiveTab] = useState("login");
  const [formData, setFormData] = useState({
    email: "",
    password: "",
  });

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
    const username = formData.email;
    const password = formData.password;

    try {
      // Create form data
      const formDataToSend = new URLSearchParams();
      formDataToSend.append('username', username);
      formDataToSend.append('password', password);

      // Send POST request to FastAPI login endpoint
      const response = await fetch("http://127.0.0.1:8000/token", {
        method: "POST",
        headers: {
          "Content-Type": "application/x-www-form-urlencoded",
        },
        body: formDataToSend.toString(), // Send the form data as a string
      });

      if (response.ok) {
        const data = await response.json();
        // Save the token to localStorage (or session storage)
        localStorage.setItem("token", data.access_token);
        // Redirect to another page or fetch user data
        // For example:
        // window.location.href = "/dashboard.html";
      } else {
        // Handle errors or invalid response
        console.error("Invalid credentials or server error.");
      }
    } catch (error) {
      console.error("Error during login:", error);
    }
  };

  return (
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
            {activeTab === "login" ? (
              <>
                Don't have an account?{" "}
                <Link href="#" className="text-teal-500 hover:underline" onClick={() => setActiveTab("signup")}>
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

