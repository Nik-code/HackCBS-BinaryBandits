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
import Analysis from './components/report_analysis/rep_anal'
import {stateContext} from "./context";
import Logout from './components/auth/Logout';

function App() {
  const [userId, setUserId] = useState()
  return (
    <>
    <stateContext.Provider value={{ userId, setUserId }}>
      <BrowserRouter>
      {/* <Navbar/> */}
      <Routes>
        <Route path="/" element={<Home/>}/>
        <Route path="/chatbot" element={<Chatbot/>}/>
        <Route path="/login" element={<Login/>}/>
        <Route path="/signup" element={<SignUp/>}/>
        <Route path="/logout" element={<Logout/>}/>
        <Route path="/reportanalysis" element={<Analysis/>}/>
      </Routes>
      {/* <Footer/> */}
      </BrowserRouter>
      </stateContext.Provider>
    </>
  )
}

export default App
