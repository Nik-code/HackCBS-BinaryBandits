import React from 'react'
import { Link } from 'react-router-dom';

const Navbar = () => {
  return (
<header className="bg-white/80 backdrop-blur-sm fixed w-full z-50 shadow-sm mb-9">
        <div className="container mx-auto px-6 py-4 flex justify-between items-center">
          <div className="flex items-center gap-2">
            {/* <Image 
              src="https://hebbkx1anhila5yf.public.blob.vercel-storage.com/CuraNet_Logo-v2ODPLpANeEXfPECK6GjnRCoVodV4z.png"
              alt="CuraNet Logo"
              width={40}
              height={40}
              className="w-auto h-8"
            /> */}
            <span className="text-2xl font-bold text-teal-500">CuraNet</span>
          </div>
          <nav>
            <ul className="flex space-x-6">
              <li><Link to="/login" className="text-neutral-600 hover:text-teal-500 transition-colors">Login</Link></li>
              <li><Link to="/signup" className="text-neutral-600 hover:text-teal-500 transition-colors">SignUp</Link></li>
              <li><Link to="/chatbot" className="text-neutral-600 hover:text-teal-500 transition-colors">Chatbot</Link></li>
              <li><Link to="/doctor-list" className="text-neutral-600 hover:text-teal-500 transition-colors">Doctors Recommended</Link></li>
              <li><Link to="/reportanalysis" className="text-neutral-600 hover:text-teal-500 transition-colors">Report Analysis</Link></li>
              <li><Link to="/outbreak-map" className="text-neutral-600 hover:text-teal-500 transition-colors">Disease Outbreak</Link></li>
            </ul>
          </nav>
        </div>
      </header>

  )
}

export default Navbar