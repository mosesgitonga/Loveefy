import React from 'react'
import { careerData } from '../data'


export default function LandingCareers() {
  return (
    <div className="mx-auto px-4">
        <h2 className="text-3xl font-bold text-center mb-8">Explore Careers</h2>
        <p className="text-xl text-gray-600 text-center max-w-3xl mx-auto mb-12">
            Discover professionals from various career paths who are looking for meaningful connections. Whether you're in tech, business, or healthcare, Loveefy helps you find a match that aligns with your career goals.
        </p>
        <div className="carousel carousel-center max-w-md p-4 space-x-4 bg-red-400 rounded-box mx-auto sm:max-w-xl md:max-w-2xl lg:max-w-4xl">
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
        <div className="flex justify-center mt-8">
        <a href="#" className="btn btn-error">Explore All Careers</a>
        </div>
    </div>
  )
}
