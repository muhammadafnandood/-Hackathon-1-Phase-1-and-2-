import React from 'react';
import AIChatbot from '../components/AIChatbot';

// Root wrapper component that includes the AI Chatbot
export default function Root({children}) {
  return (
    <>
      {children}
      <AIChatbot />
    </>
  );
}
