import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'
import { BrowserRouter, Route, Routes } from "react-router-dom";
import Register from './pages/Register';
import Login from './components/auth/Login'
import Navbar from './components/Navbar';
import Footer from './components/Footer';
import Home from './pages/Home';
import SignUp from './components/auth/SignUp'
import Chatbot from './components/chatbot/Chatbot';

function App() {
  const [count, setCount] = useState(0)
  return (
    <>
      <BrowserRouter>
      {/* <Navbar/> */}
      <Routes>
        <Route path="/" element={<Home/>}/>
        <Route path="/chatbot" element={<Chatbot/>}/>
        <Route path="/login" element={<Login/>}/>
        <Route path="/signup" element={<SignUp/>}/>
      </Routes>
      {/* <Footer/> */}
      </BrowserRouter>
    </>
  )
}

export default App
