import React from 'react';
import { testimonialsData } from '../data';

const LandingTestimonials = () => {
  return (
    <section className="bg-white mx-auto md:py-32 px-4 py-8">
      <h2 className="text-3xl font-bold text-center mb-8 text-[#ff3366]">What Our Users Say</h2>
      
      <div className="grid md:grid-cols-2 gap-6">
        {testimonialsData.map((testimonial) => (
          <div 
            key={testimonial.id} 
            className="bg-gray-50 shadow-md rounded-lg p-6 border-l-4 border-[#ff3366]"
          >
            <p className="italic text-lg mb-4">"{testimonial.content}"</p>
            <cite className="font-bold text-gray-600">- {testimonial.author}</cite>
          </div>
        ))}
      </div>
    </section>
  );
};

export default LandingTestimonials;
