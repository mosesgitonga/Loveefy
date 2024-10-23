import React from 'react';

export default function ContactSection() {
  return (
    <section className="flex flex-col items-center md:py-20 py-12 bg-gray-100">
      <h2 className="text-3xl font-bold text-gray-800 mb-6">Contact Us</h2>
      <p className="text-gray-600 mb-6 text-center max-w-lg">
        If you have any inquiries or feedback, feel free to reach out to us. We're always here to help!
      </p>
      <div className="text-gray-700 space-y-4 text-center">
        <p>
          Email: <a href="mailto:support@loveefy.com" className="text-[#ff3366] hover:underline">support@loveefy.com</a>
        </p>
        <p>Phone: <span className="text-[#ff3366]">+2547 57 573 241</span></p>
        <p>Address: Nairobi, Kenya</p>
      </div>
    </section>
  );
}
