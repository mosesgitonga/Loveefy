import React from 'react';
import { featuresData } from '../data';

const LandingChoose = () => {
  return (
    <section className="mx-auto md:pt-16 md:pb-24 px-4 py-8">
      <h2 className="text-3xl font-bold text-center mb-8">Why Choose Loveefy?</h2>
      
      <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-8">
        {featuresData.map((feature) => (
          <div key={feature.id} className="bg-white shadow-lg rounded-lg p-6 text-center">
            <h3 className="text-xl font-bold mb-4">{feature.title}</h3>
            <p>{feature.description}</p>
          </div>
        ))}
      </div>
    </section>
  );
};

export default LandingChoose;
