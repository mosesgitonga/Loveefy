import React from 'react';
import blogs from './data';
import { Link } from 'react-router-dom';

export default function BlogList() {
  return (
    <div className='grid md:grid-cols-3 grid-cols-1 md:gap-8 gap-4'>
      {
        blogs.map(blog => (
          <Link to={`/articles/${blog.slug}`} key={blog.slug} className='p-1 md:text-base text-sm bg-white shadow-md rounded-lg '>
            <img src={blog.image} alt={blog.title} className='w-full md:h-60 rounded-lg mb-2' /> {/* Image added */}
            <div className='p-4'>
            <h3 className='font-semibold text-gray-700 mb-2'>{blog.title}</h3>
            <p className='text-gray-500'>{blog.content.split(' ').slice(0, 12).join(' ')}...</p>
            </div>
          </Link>
        ))
      }
    </div>
  );
}
