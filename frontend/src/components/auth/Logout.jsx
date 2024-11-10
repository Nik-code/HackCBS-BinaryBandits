import React from 'react'
import { useNavigate } from 'react-router-dom';
import { toast,ToastContainer } from 'react-toastify';

const Logout = () => {
    const navigate=useNavigate();
    try{
        localStorage.removeItem("userId");
        toast.success("Logged out successfully!")
        setTimeout(() => {
            navigate("/login")
        }, 500);
    }catch(error){
        toast.error("Some error occured!")
    }
    
  return (
    <>
    <ToastContainer/>
    <div className='container'>Logging you out</div>
    </>
  )
}

export default Logout