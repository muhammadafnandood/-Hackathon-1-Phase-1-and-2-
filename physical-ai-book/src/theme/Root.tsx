import React from 'react';
import Chatbot from '../components/Chatbot';

// Root wrapper that provides the chatbot site-wide
export default function Root({ children }: { children: React.ReactNode }) {
  return (
    <>
      {children}
      <Chatbot />
    </>
  );
}
