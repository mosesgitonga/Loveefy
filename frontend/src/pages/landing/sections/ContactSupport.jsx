import React from 'react';
import { useNavigate } from 'react-router-dom';

export default function SupportSection() {
  const navigate = useNavigate();

  return (
    <section className="flex flex-col items-center md:py-32 py-12 bg-white text-center">
      <h2 className="text-3xl font-bold text-gray-800 mb-4">Customer Support</h2>
      <p className="text-gray-600 mb-6 max-w-lg">
        Our dedicated support team is here to help you with any issues or questions you may have. We offer 24/7 assistance to ensure your experience with Loveefy is smooth and enjoyable.
      </p>
      <button 
        className="bg-pink-600 text-white px-6 py-3 rounded-full shadow-md hover:bg-pink-700 transition duration-300"
        onClick={() => navigate('/support')}
      >
        Get Support
      </button>
    </section>
  );
}
