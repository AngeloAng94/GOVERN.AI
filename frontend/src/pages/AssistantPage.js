import React, { useState, useRef, useEffect } from "react";
import { useLanguage } from "@/contexts/LanguageContext";
import { Shield, Send, User, Loader2 } from "lucide-react";
import { Card, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import axios from "axios";

const API = `${process.env.REACT_APP_BACKEND_URL}/api`;
const MAX_CHARS = 2000;

export default function AssistantPage() {
  const { t, lang } = useLanguage();
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [sessionId] = useState(() => `session_${Date.now()}`);
  const scrollRef = useRef(null);

  useEffect(() => {
    if (scrollRef.current) scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
  }, [messages]);

  const sendMessage = async () => {
    if (!input.trim() || loading || input.trim().length < 5 || input.length > MAX_CHARS) return;
    const userMsg = input.trim();
    setInput("");
    setMessages(prev => [...prev, { role: "user", content: userMsg }]);
    setLoading(true);
    try {
      const res = await axios.post(`${API}/chat`, { message: userMsg, session_id: sessionId });
      setMessages(prev => [...prev, { role: "assistant", content: res.data.response }]);
    } catch (e) {
      const detail = e.response?.data?.detail || "Error: Unable to reach ARIA. Please try again.";
      setMessages(prev => [...prev, { role: "assistant", content: detail }]);
    } finally {
      setLoading(false);
    }
  };

  const handleKeyDown = (e) => {
    if (e.key === "Enter" && !e.shiftKey) { e.preventDefault(); sendMessage(); }
  };

  const mdComponents = {
    code: ({inline, children, ...props}) => (
      inline
        ? <code className="bg-slate-800 text-blue-400 px-1 py-0.5 rounded text-sm font-mono" {...props}>{children}</code>
        : <pre className="bg-slate-900 border border-slate-700 rounded-sm p-4 overflow-x-auto my-2"><code className="text-blue-400 text-sm font-mono" {...props}>{children}</code></pre>
    ),
    p: ({children}) => <p className="mb-2 last:mb-0 text-sm text-slate-300 leading-relaxed">{children}</p>,
    ul: ({children}) => <ul className="list-disc list-inside mb-2 space-y-1 text-sm text-slate-300">{children}</ul>,
    ol: ({children}) => <ol className="list-decimal list-inside mb-2 space-y-1 text-sm text-slate-300">{children}</ol>,
    strong: ({children}) => <strong className="font-semibold text-white">{children}</strong>,
    h1: ({children}) => <h1 className="font-['Space_Grotesk'] text-xl font-bold text-white mt-3 mb-1">{children}</h1>,
    h2: ({children}) => <h2 className="font-['Space_Grotesk'] text-lg font-semibold text-white mt-3 mb-1">{children}</h2>,
    h3: ({children}) => <h3 className="font-['Space_Grotesk'] text-base font-semibold text-white mt-3 mb-1">{children}</h3>,
    a: ({href, children}) => <a href={href} target="_blank" rel="noopener noreferrer" className="text-blue-400 hover:text-blue-300 underline">{children}</a>,
    table: ({children}) => <div className="overflow-x-auto my-2"><table className="min-w-full border border-slate-700 text-sm">{children}</table></div>,
    th: ({children}) => <th className="border border-slate-700 bg-slate-800 px-3 py-2 text-left font-medium text-slate-300">{children}</th>,
    td: ({children}) => <td className="border border-slate-700 px-3 py-2 text-slate-300">{children}</td>,
  };

  const charCount = input.length;
  const isOverLimit = charCount > 1800;
  const isTooShort = input.trim().length > 0 && input.trim().length < 5;

  return (
    <div className="flex flex-col h-[calc(100vh-3rem)]" data-testid="assistant-page">
      <div className="mb-4">
        <div className="flex items-center gap-2">
          <h1 className="font-['Space_Grotesk'] text-2xl font-bold tracking-tight text-white">ARIA</h1>
          <span className="text-xs font-mono text-blue-400 bg-blue-500/10 border border-blue-500/30 px-2 py-0.5 rounded-sm">AI Regulatory Intelligence Assistant</span>
        </div>
        <p className="text-sm text-slate-500 mt-1">
          {lang === "it" ? "Chiedi ad ARIA sulla compliance EU AI Act, GDPR, DORA, NIS2..." : "Ask ARIA about EU AI Act, GDPR, DORA, NIS2 compliance..."}
        </p>
      </div>

      <Card className="flex-1 bg-slate-900/40 backdrop-blur-md border-slate-800 rounded-sm flex flex-col overflow-hidden" data-testid="chat-card">
        <div ref={scrollRef} className="flex-1 overflow-y-auto p-4 space-y-4">
          {messages.length === 0 && (
            <div className="flex flex-col items-center justify-center h-full text-center py-16" data-testid="chat-empty-state">
              <div className="w-14 h-14 rounded-sm bg-blue-500/10 border border-blue-500/30 flex items-center justify-center mb-4">
                <Shield className="w-7 h-7 text-blue-400" />
              </div>
              <h3 className="font-['Space_Grotesk'] text-lg font-semibold text-white mb-1">ARIA</h3>
              <p className="text-xs font-mono text-slate-500 mb-4">AI Regulatory Intelligence Assistant</p>
              <p className="text-sm text-slate-500 max-w-md mb-6">
                {lang === "it"
                  ? "Esperta in EU AI Act, GDPR, DORA, NIS2, ISO 42001/27001 e governance agenti AI."
                  : "Expert in EU AI Act, GDPR, DORA, NIS2, ISO 42001/27001 and AI agent governance."}
              </p>
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-2 max-w-lg">
                {[
                  "What are the key requirements of the EU AI Act for high-risk systems?",
                  "How should I classify my AI chatbot under EU AI Act risk categories?",
                  "Quali sono gli obblighi GDPR per i sistemi AI che trattano dati personali?",
                  "Come implementare un audit trail conforme alla ISO 42001?"
                ].map((q, i) => (
                  <button key={i} onClick={() => setInput(q)}
                    className="text-left text-xs text-slate-400 bg-slate-800/50 border border-slate-700 hover:border-blue-500/30 hover:text-slate-300 rounded-sm p-3 transition-colors duration-200"
                    data-testid={`suggestion-${i}`}>
                    {q}
                  </button>
                ))}
              </div>
            </div>
          )}

          {messages.map((msg, i) => (
            <div key={i} className={`flex gap-3 ${msg.role === "user" ? "justify-end" : ""}`} data-testid={`chat-msg-${i}`}>
              {msg.role === "assistant" && (
                <div className="w-8 h-8 rounded-sm bg-blue-500/10 border border-blue-500/30 flex items-center justify-center shrink-0">
                  <Shield className="w-4 h-4 text-blue-400" />
                </div>
              )}
              <div className={`max-w-[75%] rounded-sm p-4 ${msg.role === "user" ? "bg-blue-600/20 border border-blue-500/30" : "bg-slate-800/50 border border-slate-700"}`}>
                {msg.role === "user" ? <p className="text-sm text-slate-200">{msg.content}</p> : <ReactMarkdown remarkPlugins={[remarkGfm]} components={mdComponents}>{msg.content}</ReactMarkdown>}
              </div>
              {msg.role === "user" && (
                <div className="w-8 h-8 rounded-sm bg-slate-700 flex items-center justify-center shrink-0"><User className="w-4 h-4 text-slate-300" /></div>
              )}
            </div>
          ))}

          {loading && (
            <div className="flex gap-3" data-testid="chat-loading">
              <div className="w-8 h-8 rounded-sm bg-blue-500/10 border border-blue-500/30 flex items-center justify-center shrink-0"><Shield className="w-4 h-4 text-blue-400" /></div>
              <div className="bg-slate-800/50 border border-slate-700 rounded-sm p-4 flex items-center gap-2">
                <Loader2 className="w-4 h-4 text-blue-400 animate-spin" />
                <span className="text-xs text-slate-500 font-mono">{t("loading")}</span>
              </div>
            </div>
          )}
        </div>

        {/* Input + char counter + footer */}
        <div className="border-t border-slate-800">
          <div className="p-4 pb-2" data-testid="chat-input-area">
            <div className="flex gap-2">
              <Input
                className="bg-slate-950 border-slate-800 text-slate-200 rounded-sm flex-1 focus:border-blue-500 focus:ring-1 focus:ring-blue-500"
                placeholder={lang === "it" ? "Chiedi ad ARIA sulla compliance EU AI Act, GDPR, DORA, NIS2..." : "Ask ARIA about EU AI Act, GDPR, DORA, NIS2 compliance..."}
                value={input} onChange={e => setInput(e.target.value.slice(0, MAX_CHARS))}
                onKeyDown={handleKeyDown} disabled={loading} maxLength={MAX_CHARS}
                data-testid="chat-input"
              />
              <Button onClick={sendMessage} disabled={!input.trim() || loading || isTooShort || charCount > MAX_CHARS}
                className="bg-blue-600 hover:bg-blue-500 text-white rounded-sm px-4" data-testid="chat-send-btn">
                <Send className="w-4 h-4" />
              </Button>
            </div>
            <div className="flex items-center justify-between mt-1.5 px-1">
              <span className="text-[10px] text-slate-700 font-mono">
                {isTooShort && <span className="text-amber-500">{lang === "it" ? "Min 5 caratteri" : "Min 5 characters"}</span>}
              </span>
              <span className={`text-[10px] font-mono ${isOverLimit ? "text-red-400" : "text-slate-700"}`} data-testid="char-counter">
                {charCount}/{MAX_CHARS}
              </span>
            </div>
          </div>
          <div className="px-4 pb-3">
            <p className="text-[10px] font-mono text-slate-700 text-center">Powered by GOVERN.AI</p>
          </div>
        </div>
      </Card>
    </div>
  );
}
