import React from 'react';
import { motion } from 'framer-motion';

export const Navbar = ({ onLogout }) => {
  const [isOpen, setIsOpen] = React.useState(false);

  return (
    <nav className="glass sticky top-0 z-50 border-b border-white/10">
      <div className="max-w-7xl mx-auto px-4 py-4 flex items-center justify-between">
        <motion.div
          initial={{ opacity: 0, x: -20 }}
          animate={{ opacity: 1, x: 0 }}
          className="text-2xl font-bold gradient-text"
        >
          AI Career Assistant
        </motion.div>

        <div className="hidden md:flex gap-6">
          <NavLink href="/dashboard">Dashboard</NavLink>
          <NavLink href="/resume">Resume</NavLink>
          <NavLink href="/career">Career</NavLink>
          <NavLink href="/interview">Interview</NavLink>
          <NavLink href="/emotion">Wellness</NavLink>
        </div>

        <button
          onClick={onLogout}
          className="btn btn-primary"
        >
          Logout
        </button>
      </div>
    </nav>
  );
};

const NavLink = ({ href, children }) => (
  <a href={href} className="hover:text-primary-400 transition-colors">
    {children}
  </a>
);
