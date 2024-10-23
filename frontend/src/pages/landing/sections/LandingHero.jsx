import React from 'react';
import { useNavigate } from 'react-router-dom';
import { FaArrowRight } from 'react-icons/fa'; // Importing react-icons

export default function LandingHero() {
  const navigate = useNavigate();

  return (
    <section className="relative text-white">
      <div className="absolute inset-0 bg-[#ff3366ec] opacity-80"></div>
      <div className="relative mx-auto px-4 py-24 md:py-24 flex flex-col md:flex-row items-center md:gap-12">
        <div className="md:w-1/2 text-center md:text-left mb-10 md:mb-0">
          <h1 className="text-4xl md:text-5xl font-bold mb-6">Find Love Through Career</h1>
          <p className="text-xl mb-8">
            Join millions of singles and find your soulmate with Loveefy. Our advanced matching system connects you with professionals in your area who share your career ambitions and values.
          </p>
          <button
            onClick={() => navigate('/register')}
            className="bg-white text-gray-800 font-bold py-3 px-8 rounded-full hover:bg-purple-100 transition duration-300 flex items-center justify-center"
          >
            Join For Free
            <FaArrowRight className="ml-2 h-5 w-5" /> {/* Replacing ArrowRight with react-icons */}
          </button>
        </div>

        <div className="md:w-1/2 flex justify-center">
          <div className="grid grid-cols-2 gap-4">
            <img
              src="https://images.unsplash.com/photo-1529626455594-4ff0802cfb7e?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=687&q=80"
              alt="Happy couple"
              className="rounded-lg shadow-lg transform hover:scale-105 transition duration-300"
            />
            <img
              src="https://images.unsplash.com/photo-1516726817505-f5ed825624d8?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=687&q=80"
              alt="Professional couple"
              className="rounded-lg shadow-lg transform hover:scale-105 transition duration-300 mt-10"
            />
          </div>
        </div>
      </div>
    </section>
  );
}
