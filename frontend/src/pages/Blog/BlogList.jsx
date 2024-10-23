import React from 'react'
import blogs from './data'
import { Link } from 'react-router-dom'

export default function BlogList() {
  return (
    <div className='grid md:grid-cols-4 grid-cols-2 md:gap-8 gap-3'>
      {
        blogs.map(blog => (
          <Link to={`/articles/${blog.slug}`} key={blog.slug} className='md:text-base text-sm bg-white shadow-md rounded-lg p-4'>
            <h3 className='font-semibold text-gray-700 mb-2'>{blog.title}</h3>
            <p className='text-gray-500'>{blog.content}</p>
          </Link>
        ))
      }
    </div>
  )
}
