"use client";
import { useState, useRef, useEffect } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { Send, Mic, MicOff, Loader2, Activity, Bot, User, ArrowRight } from "lucide-react";
import { useRouter } from "next/navigation";
import DisclaimerBanner from "@/components/DisclaimerBanner";
import { triageApi } from "@/services/api";

interface ChatMsg {
  role: "user" | "assistant";
  content: string;
  timestamp?: string;
}

export default function ChatPage() {
  const router = useRouter();
  const [messages, setMessages] = useState<ChatMsg[]>([]);
  const [input, setInput] = useState("");
  const [sessionId, setSessionId] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const [isComplete, setIsComplete] = useState(false);
  const [resultData, setResultData] = useState<{ session_id: string; severity_score: number; urgency_level: string } | null>(null);
  const [isListening, setIsListening] = useState(false);
  const chatEndRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLInputElement>(null);

  // Scroll to bottom on new messages
  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  // Initialize conversation
  useEffect(() => {
    startChat();
  }, []);

  const startChat = async () => {
    try {
      setLoading(true);
      const res = await triageApi.chat({ message: "", session_id: undefined, language: "en" });
      setSessionId(res.session_id);
      setMessages(res.chat_history.map((m: ChatMsg) => ({ role: m.role, content: m.content })));
    } catch {
      setMessages([{
        role: "assistant",
        content: "Hello! I'm your TriageX assistant. I'll help assess your symptoms.\n\nPlease describe your symptoms in detail. For example: 'I have a headache, sore throat, and mild fever.'"
      }]);
      setSessionId("local-" + Date.now());
    } finally {
      setLoading(false);
    }
  };

  const sendMessage = async () => {
    if (!input.trim() || loading || isComplete) return;

    const userMsg = input.trim();
    setInput("");
    setMessages((prev) => [...prev, { role: "user", content: userMsg }]);
    setLoading(true);

    try {
      const res = await triageApi.chat({
        message: userMsg,
        session_id: sessionId || undefined,
        language: "en",
      });

      setSessionId(res.session_id);
      setMessages(res.chat_history.map((m: ChatMsg) => ({ role: m.role, content: m.content })));

      if (res.is_complete) {
        setIsComplete(true);
        setResultData(res.collected_data);
      }
    } catch {
      setMessages((prev) => [
        ...prev,
        { role: "assistant", content: "I apologize, but I encountered an issue. Please try again." },
      ]);
    } finally {
      setLoading(false);
      inputRef.current?.focus();
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  // Voice input
  const toggleVoice = () => {
    if (!("webkitSpeechRecognition" in window || "SpeechRecognition" in window)) {
      alert("Voice input not supported in this browser.");
      return;
    }

    if (isListening) {
      setIsListening(false);
      return;
    }

    const SpeechRecognition = (window as any).SpeechRecognition || (window as any).webkitSpeechRecognition;
    const recognition = new SpeechRecognition();
    recognition.continuous = false;
    recognition.interimResults = false;
    recognition.lang = "en-US";

    recognition.onresult = (event: any) => {
      const transcript = event.results[0][0].transcript;
      setInput((prev) => prev + " " + transcript);
      setIsListening(false);
    };
    recognition.onerror = () => setIsListening(false);
    recognition.onend = () => setIsListening(false);

    setIsListening(true);
    recognition.start();
  };

  return (
    <div className="min-h-screen pt-20 pb-4 px-4">
      <div className="max-w-3xl mx-auto h-[calc(100vh-6rem)] flex flex-col">
        {/* Header */}
        <motion.div
          initial={{ opacity: 0, y: -10 }}
          animate={{ opacity: 1, y: 0 }}
          className="flex items-center gap-3 mb-4"
        >
          <div className="w-10 h-10 rounded-xl gradient-bg flex items-center justify-center">
            <Activity className="w-5 h-5 text-white" />
          </div>
          <div>
            <h1 className="text-lg font-bold text-slate-800 dark:text-white">Symptom Assessment</h1>
            <p className="text-xs text-slate-500">Chat with TriageX AI assistant</p>
          </div>
        </motion.div>

        <DisclaimerBanner />

        {/* Chat Messages */}
        <div className="flex-1 overflow-y-auto mt-4 space-y-4 pr-2">
          <AnimatePresence>
            {messages.map((msg, i) => (
              <motion.div
                key={i}
                initial={{ opacity: 0, y: 15, scale: 0.98 }}
                animate={{ opacity: 1, y: 0, scale: 1 }}
                transition={{ duration: 0.3 }}
                className={`flex items-end gap-2 ${msg.role === "user" ? "justify-end" : "justify-start"}`}
              >
                {msg.role === "assistant" && (
                  <div className="w-8 h-8 rounded-lg gradient-bg flex items-center justify-center shrink-0 mb-1">
                    <Bot className="w-4 h-4 text-white" />
                  </div>
                )}
                <div className={`chat-bubble ${msg.role}`}>
                  {msg.content}
                </div>
                {msg.role === "user" && (
                  <div className="w-8 h-8 rounded-lg bg-slate-200 dark:bg-slate-700 flex items-center justify-center shrink-0 mb-1">
                    <User className="w-4 h-4 text-slate-600 dark:text-slate-300" />
                  </div>
                )}
              </motion.div>
            ))}
          </AnimatePresence>

          {loading && (
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              className="flex items-end gap-2"
            >
              <div className="w-8 h-8 rounded-lg gradient-bg flex items-center justify-center">
                <Bot className="w-4 h-4 text-white" />
              </div>
              <div className="chat-bubble assistant flex items-center gap-2">
                <Loader2 className="w-4 h-4 animate-spin text-blue-500" />
                <span className="text-slate-400 text-sm">Thinking...</span>
              </div>
            </motion.div>
          )}

          <div ref={chatEndRef} />
        </div>

        {/* Results CTA */}
        {isComplete && resultData && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="mt-4"
          >
            <button
              onClick={() => router.push(`/results?session=${resultData.session_id}`)}
              className="w-full btn-primary flex items-center justify-center gap-3 py-4 text-base"
            >
              <span>View Full Results & Body Map</span>
              <ArrowRight className="w-5 h-5" />
            </button>
          </motion.div>
        )}

        {/* Input Bar */}
        {!isComplete && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="mt-4 glass-card p-2 flex items-center gap-2"
          >
            <button
              onClick={toggleVoice}
              className={`p-3 rounded-xl transition-colors ${
                isListening
                  ? "bg-red-100 text-red-500 dark:bg-red-500/10"
                  : "text-slate-400 hover:bg-slate-100 dark:hover:bg-slate-800"
              }`}
              title="Voice input"
            >
              {isListening ? <MicOff className="w-5 h-5" /> : <Mic className="w-5 h-5" />}
            </button>

            <input
              ref={inputRef}
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={handleKeyDown}
              placeholder="Describe your symptoms..."
              disabled={loading}
              className="flex-1 bg-transparent border-none outline-none text-sm text-slate-800 dark:text-white placeholder:text-slate-400 px-2"
            />

            <button
              onClick={sendMessage}
              disabled={!input.trim() || loading}
              className="p-3 rounded-xl gradient-bg text-white disabled:opacity-40 transition-opacity"
            >
              <Send className="w-5 h-5" />
            </button>
          </motion.div>
        )}
      </div>
    </div>
  );
}
