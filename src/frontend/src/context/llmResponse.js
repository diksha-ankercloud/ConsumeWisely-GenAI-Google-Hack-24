import React, { createContext, useContext, useState } from 'react';

const LlmContext = createContext();

export const LlmProvider = ({ children }) => {
  const [llmResponse, setLlmResponse] = useState([]);
  return (
    <LlmContext.Provider value={{ llmResponse, setLlmResponse }}>
      {children}
    </LlmContext.Provider>
  );
};

export const usellmResponse = () => useContext(LlmContext);
