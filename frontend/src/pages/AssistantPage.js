import React, { useState, useRef, useEffect } from "react";
import { useLanguage } from "@/contexts/LanguageContext";
import { MessageSquare, Send, Bot, User, Loader2 } from "lucide-react";
import { Card, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { ScrollArea } from "@/components/ui/scroll-area";
import axios from "axios";

const API = `${process.env.REACT_APP_BACKEND_URL}/api`;

export default function AssistantPage() {
  const { t } = useLanguage();
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [sessionId] = useState(() => `session_${Date.now()}`);
  const scrollRef = useRef(null);

  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
    }
  }, [messages]);

  const sendMessage = async () => {
    if (!input.trim() || loading) return;
    const userMsg = input.trim();
    setInput("");
    setMessages(prev => [...prev, { role: "user", content: userMsg }]);
    setLoading(true);

    try {
      const res = await axios.post(`${API}/chat`, { message: userMsg, session_id: sessionId });
      setMessages(prev => [...prev, { role: "assistant", content: res.data.response }]);
    } catch (e) {
      setMessages(prev => [...prev, { role: "assistant", content: "Error: Unable to reach AI service. Please try again." }]);
    } finally {
      setLoading(false);
    }
  };

  const handleKeyDown = (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  const renderContent = (content) => {
    // Simple markdown-like rendering
    const lines = content.split("\n");
    return lines.map((line, i) => {
      if (line.startsWith("### ")) return <h3 key={i} className="font-['Space_Grotesk'] text-base font-semibold text-white mt-3 mb-1">{line.slice(4)}</h3>;
      if (line.startsWith("## ")) return <h2 key={i} className="font-['Space_Grotesk'] text-lg font-semibold text-white mt-3 mb-1">{line.slice(3)}</h2>;
      if (line.startsWith("# ")) return <h1 key={i} className="font-['Space_Grotesk'] text-xl font-bold text-white mt-3 mb-1">{line.slice(2)}</h1>;
      if (line.startsWith("- ")) return <li key={i} className="text-sm text-slate-300 ml-4 list-disc">{line.slice(2)}</li>;
      if (line.startsWith("**") && line.endsWith("**")) return <p key={i} className="text-sm font-semibold text-white">{line.slice(2, -2)}</p>;
      if (line.trim() === "") return <br key={i} />;
      return <p key={i} className="text-sm text-slate-300 leading-relaxed">{line}</p>;
    });
  };

  return (
    <div className="flex flex-col h-[calc(100vh-3rem)]" data-testid="assistant-page">
      <div className="mb-4">
        <h1 className="font-['Space_Grotesk'] text-2xl font-bold tracking-tight text-white">{t("assistant_title")}</h1>
        <p className="text-sm text-slate-500 mt-1">{t("assistant_subtitle")}</p>
      </div>

      {/* Chat Area */}
      <Card className="flex-1 bg-slate-900/40 backdrop-blur-md border-slate-800 rounded-sm flex flex-col overflow-hidden" data-testid="chat-card">
        <div ref={scrollRef} className="flex-1 overflow-y-auto p-4 space-y-4">
          {messages.length === 0 && (
            <div className="flex flex-col items-center justify-center h-full text-center py-16" data-testid="chat-empty-state">
              <div className="w-14 h-14 rounded-sm bg-blue-500/10 border border-blue-500/30 flex items-center justify-center mb-4">
                <MessageSquare className="w-7 h-7 text-blue-400" />
              </div>
              <h3 className="font-['Space_Grotesk'] text-lg font-semibold text-white mb-2">GOVERN.AI Assistant</h3>
              <p className="text-sm text-slate-500 max-w-md">
                {t("assistant_subtitle")}
              </p>
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-2 mt-6 max-w-lg">
                {[
                  "What are the key requirements of the EU AI Act for high-risk systems?",
                  "How should I classify my AI chatbot under EU AI Act risk categories?",
                  "Quali sono gli obblighi GDPR per i sistemi AI che trattano dati personali?",
                  "Come implementare un audit trail conforme alla ISO 42001?"
                ].map((q, i) => (
                  <button
                    key={i}
                    onClick={() => { setInput(q); }}
                    className="text-left text-xs text-slate-400 bg-slate-800/50 border border-slate-700 hover:border-blue-500/30 hover:text-slate-300 rounded-sm p-3 transition-colors duration-200"
                    data-testid={`suggestion-${i}`}
                  >
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
                  <Bot className="w-4 h-4 text-blue-400" />
                </div>
              )}
              <div className={`max-w-[75%] rounded-sm p-4 ${
                msg.role === "user"
                  ? "bg-blue-600/20 border border-blue-500/30"
                  : "bg-slate-800/50 border border-slate-700"
              }`}>
                {msg.role === "user" ? (
                  <p className="text-sm text-slate-200">{msg.content}</p>
                ) : (
                  <div>{renderContent(msg.content)}</div>
                )}
              </div>
              {msg.role === "user" && (
                <div className="w-8 h-8 rounded-sm bg-slate-700 flex items-center justify-center shrink-0">
                  <User className="w-4 h-4 text-slate-300" />
                </div>
              )}
            </div>
          ))}

          {loading && (
            <div className="flex gap-3" data-testid="chat-loading">
              <div className="w-8 h-8 rounded-sm bg-blue-500/10 border border-blue-500/30 flex items-center justify-center shrink-0">
                <Bot className="w-4 h-4 text-blue-400" />
              </div>
              <div className="bg-slate-800/50 border border-slate-700 rounded-sm p-4 flex items-center gap-2">
                <Loader2 className="w-4 h-4 text-blue-400 animate-spin" />
                <span className="text-xs text-slate-500 font-mono">{t("loading")}</span>
              </div>
            </div>
          )}
        </div>

        {/* Input */}
        <div className="p-4 border-t border-slate-800" data-testid="chat-input-area">
          <div className="flex gap-2">
            <Input
              className="bg-slate-950 border-slate-800 text-slate-200 rounded-sm flex-1 focus:border-blue-500 focus:ring-1 focus:ring-blue-500"
              placeholder={t("assistant_placeholder")}
              value={input}
              onChange={e => setInput(e.target.value)}
              onKeyDown={handleKeyDown}
              disabled={loading}
              data-testid="chat-input"
            />
            <Button
              onClick={sendMessage}
              disabled={!input.trim() || loading}
              className="bg-blue-600 hover:bg-blue-500 text-white rounded-sm px-4"
              data-testid="chat-send-btn"
            >
              <Send className="w-4 h-4" />
            </Button>
          </div>
        </div>
      </Card>
    </div>
  );
}
