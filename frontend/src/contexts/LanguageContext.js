import React, { createContext, useContext, useState, useCallback } from "react";
import en from "../locales/en.json";
import it from "../locales/it.json";

const translations = { en, it };

const LanguageContext = createContext();

export const LanguageProvider = ({ children }) => {
  const [lang, setLang] = useState("en");

  const t = useCallback((key) => {
    return translations[lang]?.[key] || translations.en[key] || key;
  }, [lang]);

  const toggleLang = useCallback(() => {
    setLang(prev => prev === "en" ? "it" : "en");
  }, []);

  return (
    <LanguageContext.Provider value={{ lang, setLang, toggleLang, t }}>
      {children}
    </LanguageContext.Provider>
  );
};

export const useLanguage = () => useContext(LanguageContext);
