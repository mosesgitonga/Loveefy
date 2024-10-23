import React, { useRef } from 'react';
import { careerData } from '../data';
import { FaArrowLeft, FaArrowRight } from 'react-icons/fa'; // Import icons from React Icons

export default function LandingCareers() {
  const carouselRef = useRef(null);

  // Function to handle scrolling to the left
  const scrollLeft = () => {
    carouselRef.current.scrollBy({
      left: -300, // Adjust scroll amount as needed
      behavior: 'smooth',
    });
  };

  // Function to handle scrolling to the right
  const scrollRight = () => {
    carouselRef.current.scrollBy({
      left: 300, // Adjust scroll amount as needed
      behavior: 'smooth',
    });
  };

  return (
    <div className="mx-auto px-4 relative">
      <h2 className="text-3xl font-bold text-center mb-8">Explore Careers</h2>
      <p className="text-xl text-gray-600 text-center max-w-3xl mx-auto mb-12">
        Discover professionals from various career paths who are looking for meaningful connections. Whether you're in tech, business, or healthcare, Loveefy helps you find a match that aligns with your career goals.
      </p>

      <div className="relative">
        <div onClick={scrollLeft} className="cursor absolute left-0 top-1/2 transform -translate-y-1/2 bg-gray-200 p-2 rounded-full z-10">
          <FaArrowLeft className="h-6 w-6 text-gray-600" />
        </div>
        <div onClick={scrollRight} className="cursor- absolute right-0 top-1/2 transform -translate-y-1/2 bg-gray-200 p-2 rounded-full z-10">
          <FaArrowRight className="h-6 w-6 text-gray-600" />
        </div>

        {/* Carousel */}
        <div ref={carouselRef} className="carousel flex space-x-4 overflow-x-auto snap-x snap-mandatory scrollbar-hide p-4 bg-[#ff3366ec] rounded-box mx-auto max-w-md sm:max-w-xl md:max-w-2xl lg:max-w-4xl">
          {careerData.map((career) => (
            <div key={career.id} className="carousel-item">
              <div className="card w-64 bg-base-100 shadow-xl">
                <figure className="px-4 pt-4">
                  <img src={career.image} alt={career.title} className="rounded-xl h-40 w-full object-cover" />
                </figure>
                <div className="card-body items-center text-center p-4">
                  <h3 className="card-title text-lg font-semibold mb-2">{career.title}</h3>
                  <p className="text-sm text-gray-600">{career.description}</p>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>

      <div className="flex justify-center mt-8">
        <a href="#" className="btn bg-[#ff3366]">Explore All Careers</a>
      </div>
    </div>
  );
}
