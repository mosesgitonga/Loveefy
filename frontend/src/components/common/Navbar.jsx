import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import { AiOutlineMenu, AiOutlineClose } from 'react-icons/ai';
import { navLinks } from './data';

export default function Navbar() {
  const [isOpen, setIsOpen] = useState(false);

  const toggleMenu = () => {
    setIsOpen(!isOpen);
  };

  return (
    <nav className="bg-white shadow-md fixed top-0 w-full z-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between h-16">
          <div className="flex items-center">
            <Link to="/" className="flex-shrink-0 flex items-center">
              <img className="md:w-24 w-16" src="/loveefy.png" alt="Loveefy" />
            </Link>
          </div>

          {/* Desktop Menu */}
          <div className="hidden sm:flex sm:items-center">
            <div className="flex space-x-4">
              {navLinks.map(link => (
                <NavLink key={link.id} to={link.href}>
                  {link.name}
                </NavLink>
              ))}
            </div>
          </div>

          {/* Login/Register Links */}
          <div className="hidden sm:flex sm:items-center">
            <Link to="/login" className="text-gray-700 hover:bg-gray-100 px-3 py-2 rounded-md text-sm font-medium">
              Log in
            </Link>
            <Link to="/register" className="ml-3 inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-pink-600 hover:bg-pink-700">
              Register
            </Link>
          </div>

          {/* Mobile Menu Button */}
          <div className="-mr-2 flex items-center sm:hidden">
            <button
              onClick={toggleMenu}
              className="inline-flex items-center justify-center p-2 rounded-md text-gray-400 hover:text-gray-500 hover:bg-gray-100 focus:outline-none focus:ring-2 focus:ring-inset focus:ring-pink-500"
              aria-expanded="false"
            >
              <span className="sr-only">Open main menu</span>
              {isOpen ? (
                <AiOutlineClose className="block h-6 w-6" aria-hidden="true" />
              ) : (
                <AiOutlineMenu className="block h-6 w-6" aria-hidden="true" />
              )}
            </button>
          </div>
        </div>
      </div>

      {/* Mobile Menu */}
      {isOpen && (
        <div className="sm:hidden absolute top-16 inset-x-0 z-40 bg-white shadow-md">
          <ul className="pt-2 pb-3 space-y-1">
            {navLinks.map(link => (
              <MobileNavLink key={link.id} to={link.href}>
                {link.name}
              </MobileNavLink>
            ))}
          </ul>
          <div className="pt-4 pb-3 border-t border-gray-200">
            <div className="flex items-center px-4">
              <Link to="/login" className="block px-3 py-2 rounded-md text-base font-medium text-gray-700 hover:text-gray-900 hover:bg-gray-50">
                Log in
              </Link>
              <Link to="/register" className="ml-4 block px-3 py-2 rounded-md text-base font-medium text-white bg-pink-600 hover:bg-pink-700">
                Register
              </Link>
            </div>
          </div>
        </div>
      )}
    </nav>
  );
}

function NavLink({ to, children }) {
  return (
    <a
      href={to}
      className="text-gray-700 hover:bg-gray-100 px-3 py-2 rounded-md text-sm font-medium"
    >
      {children}
    </a>
  );
}

function MobileNavLink({ to, children }) {
  return (
    <a
      href={to}
      className="block px-3 py-2 rounded-md text-base font-medium text-gray-700 hover:text-gray-900 hover:bg-gray-50"
    >
      {children}
    </a>
  );
}
