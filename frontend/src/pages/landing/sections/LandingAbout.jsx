import React from 'react';
import { FaBullseye, FaLightbulb } from 'react-icons/fa';

const LandingAbout = () => {
  return (
    <section className="mx-auto md:py-32 px-4 py-8">
      <div className="grid md:grid-cols-2 md:gap-24 gap-12">
        <div className="relative w-full md:h-auto h-96">
          <img 
            src="tech.avif" 
            alt="Tech Professionals" 
            className="w-full h-full object-cover rounded-lg"
          />
          <div className="absolute inset-0 bg-black bg-opacity-50 flex flex-col justify-center items-center text-white p-6">
            <h2 className="text-2xl text-[#ff3366] font-bold mb-4">About Loveefy</h2>
            <p className="text-center">
              Loveefy is dedicated to creating meaningful connections by matching individuals based on career and location. Our platform is designed to help professionals find love without compromising their career goals. Learn more about our mission and values.
            </p>
          </div>
        </div>

        <div className="flex flex-col items-start gap-8">
          <div className="bg-gray-50 shadow-lg rounded-lg p-6 gap-4">
          <div className='flex items-start gap-2'>
              <FaLightbulb className="bg-[#ff3366] p-2 rounded-full md:text-4xl text-3xl text-white" />
              <h3 className="md:text-2xl text-xl font-bold mb-4">Our Vision</h3>
            </div>
            <div>
              <p className='md:text-base text-sm'>
                At Loveefy, we aim to revolutionize dating by focusing on career-driven individuals, who mostly do not have much time.
              </p>
            </div>
          </div>

          <div className="bg-gray-50 shadow-lg rounded-lg p-6 gap-4">
            <div className='flex items-start gap-2'>
              <FaBullseye className="bg-[#ff3366] p-2 rounded-full md:text-4xl text-3xl text-white" />
              <h3 className="md:text-2xl text-xl font-bold mb-4">Our Mission</h3>
            </div>
            <div>
              <p className='md:text-base text-sm'>
                Our mission is to provide a platform where professionals can connect with like-minded people who understand and share their career ambitions.
              </p>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
};

export default LandingAbout;
