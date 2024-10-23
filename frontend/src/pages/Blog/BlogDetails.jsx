import React from 'react'
import { useParams } from 'react-router-dom'
import blogs from './data'

export default function BlogDetails() {
  const { slug } = useParams()

  const article = blogs.find((blog) => blog.slug == slug) || {}

  
  return (
    <div className='md:p-8'>
      <h1>{article.title}</h1>
      <p>{article.content}</p>
    </div>
  )
}
