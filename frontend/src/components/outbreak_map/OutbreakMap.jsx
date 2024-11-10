import React from 'react'

const OutbreakMap = () => {
  return (
    <div>
       <iframe
      src={`http://127.0.0.1:5500/frontend/src/components/outbreak_map/outbreak_map_demo.html`} // Place your HTML file in the public directory
      title="Embedded HTML"
      style={{ width: '100%', height: '100vh', border: 'none' }}
    />
    </div>
  )
}

export default OutbreakMap
