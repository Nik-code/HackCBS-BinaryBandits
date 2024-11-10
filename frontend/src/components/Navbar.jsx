import React from 'react'

const Navbar = () => {
  return (
<nav>
            <ul className="flex space-x-6">
              <li><a href="/login" className="text-neutral-600 hover:text-teal-500 transition-colors">Login</a></li>
              <li><a href="/signup" className="text-neutral-600 hover:text-teal-500 transition-colors">SignUp</a></li>
              <li><a href="/chatbot" className="text-neutral-600 hover:text-teal-500 transition-colors">Chatbot</a></li>
              <li><a href="/reportanalysis" className="text-neutral-600 hover:text-teal-500 transition-colors">Report Analysis</a></li>
            </ul>
          </nav>

  )
}

export default Navbar