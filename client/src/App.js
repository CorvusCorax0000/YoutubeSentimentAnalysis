// App.js
import React, { useState, useEffect } from 'react';
import LineChart from './LineChart';

const App = () => {
  const [formData, setFormData] = useState('');
  const [csrfToken, setCsrfToken] = useState('');
  const [isSubmitted, setIsSubmitted] = useState(false);
  const [submissionStatus, setSubmissionStatus] = useState(null);

  const getCsrfToken = async () => {
    const response = await fetch('http://localhost:8000/csrf_token/');
    const data = await response.json();
    setCsrfToken(data.csrfToken);
  };

  useEffect(() => {
    getCsrfToken();
  }, []);

  const handleSubmit = async (event) => {
    event.preventDefault();
    setIsSubmitted(false);
    const response = await fetch('http://localhost:8000/process/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': csrfToken,
      },
      body: JSON.stringify({ data: formData }),
    });

    if (response.status === 200) {
      setIsSubmitted(true);
    }

    const responseBody = await response.json();
    console.log(responseBody);
  };

  return (
    <div className="flex justify-center items-center h-screen font-jetbrains">
      <form onSubmit={handleSubmit} className="w-full max-w-md">
        <div className='flex items-center'>
          <input
            type="text"
            className="input input-bordered rounded w-full max-w-md h-10 border-2 border-slate-200 focus:border-black outline-offset-8 outline-slate-200 px-2 py-4 transition duration-150 ease-in-out"
            value={formData}
            onChange={(e) => setFormData(e.target.value)}
          />
          {isSubmitted && <span className="ml-4 font-medium text-[#508D4E]">Sent</span>}
        </div>
        <button type="submit" className="btn btn-primary block mx-auto mt-4 text-white bg-black border-2 border-white px-4 py-2 rounded hover:bg-white hover:text-black hover:border-black transition duration-150 ease-in-out">
          Submit
        </button>
      </form>
      {isSubmitted && <LineChart fetchTrigger={isSubmitted} />}
    </div>
  )
}

export default App;
