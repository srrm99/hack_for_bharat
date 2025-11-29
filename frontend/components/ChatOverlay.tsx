"use client";

import React, { useState } from 'react';
import { X, Send, Bot, User } from 'lucide-react';

interface Message {
  role: 'user' | 'assistant';
  content: string;
}

interface ChatOverlayProps {
  isOpen: boolean;
  onClose: () => void;
  initialQuery?: string;
  context?: string;
}

export default function ChatOverlay({ isOpen, onClose, initialQuery, context }: ChatOverlayProps) {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  // Initialize chat with query if provided
  React.useEffect(() => {
    if (isOpen && initialQuery) {
      setMessages([{ role: 'user', content: initialQuery }]);
      setIsLoading(true);
      
      // Call the real backend chat API
      fetch('http://127.0.0.1:8000/v1/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          messages: [{ role: 'user', content: initialQuery }],
          context: context || ""
        })
      })
      .then(res => res.json())
      .then(data => {
        setIsLoading(false);
        if (data.success) {
          setMessages(prev => [...prev, { role: 'assistant', content: data.response }]);
        } else {
          setMessages(prev => [...prev, { role: 'assistant', content: "Sorry, I couldn't connect to the chat server." }]);
        }
      })
      .catch(err => {
        setIsLoading(false);
        console.error(err);
        setMessages(prev => [...prev, { role: 'assistant', content: "Network error occurred." }]);
      });

    } else if (isOpen && !messages.length) {
        setMessages([]);
    }
  }, [isOpen, initialQuery]); // Removed 'context' from deps to avoid re-triggering on prop stable updates if query hasn't changed

  if (!isOpen) return null;

  const sendMessage = async () => {
    if (!input.trim()) return;
    
    const newMsg: Message = { role: 'user', content: input };
    const updatedMessages = [...messages, newMsg];
    setMessages(updatedMessages);
    setInput('');
    setIsLoading(true);

    try {
      const res = await fetch('http://127.0.0.1:8000/v1/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          messages: updatedMessages.map(m => ({ role: m.role, content: m.content })), // Send full history
          context: context || ""
        })
      });
      
      const data = await res.json();
      setIsLoading(false);
      
      if (data.success) {
        setMessages(prev => [...prev, { role: 'assistant', content: data.response }]);
      } else {
        setMessages(prev => [...prev, { role: 'assistant', content: "Error getting response." }]);
      }
    } catch (err) {
      setIsLoading(false);
      setMessages(prev => [...prev, { role: 'assistant', content: "Failed to send message." }]);
    }
  };

  return (
    <div className="fixed inset-0 bg-white z-50 flex flex-col md:max-w-md md:mx-auto animate-in slide-in-from-bottom duration-300">
      
      {/* Header */}
      <div className="px-4 py-3 border-b border-gray-100 flex justify-between items-center bg-white">
        <div className="flex items-center gap-2">
          <div className="w-8 h-8 bg-black rounded-full flex items-center justify-center">
            <Bot className="text-white w-5 h-5" />
          </div>
          <div>
            <h3 className="font-bold text-sm">BharatAI Assistant</h3>
            <span className="text-xs text-green-500 flex items-center gap-1">
              <span className="w-1.5 h-1.5 bg-green-500 rounded-full"></span>
              Online
            </span>
          </div>
        </div>
        <button onClick={onClose} className="p-2 hover:bg-gray-100 rounded-full">
          <X className="w-6 h-6 text-gray-500" />
        </button>
      </div>

      {/* Messages */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4 bg-gray-50">
        {messages.map((msg, i) => (
          <div key={i} className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}>
            <div className={`max-w-[80%] rounded-2xl px-4 py-3 ${
              msg.role === 'user' 
                ? 'bg-black text-white rounded-br-none' 
                : 'bg-white border border-gray-200 text-gray-800 rounded-bl-none shadow-sm'
            }`}>
              <p className="text-sm leading-relaxed whitespace-pre-wrap">{msg.content}</p>
            </div>
          </div>
        ))}
        {isLoading && (
          <div className="flex justify-start">
            <div className="bg-white border border-gray-200 rounded-2xl rounded-bl-none px-4 py-3 shadow-sm">
              <div className="flex gap-1">
                <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce"></div>
                <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce delay-100"></div>
                <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce delay-200"></div>
              </div>
            </div>
          </div>
        )}
      </div>

      {/* Input */}
      <div className="p-4 bg-white border-t border-gray-100">
        <div className="flex items-center gap-2 bg-gray-100 rounded-full px-4 py-2">
          <input 
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => e.key === 'Enter' && sendMessage()}
            placeholder="Type your message..."
            className="flex-1 bg-transparent border-none outline-none text-sm"
            autoFocus
          />
          <button 
            onClick={sendMessage}
            disabled={!input.trim()}
            className="p-2 bg-black text-white rounded-full disabled:opacity-50"
          >
            <Send className="w-4 h-4" />
          </button>
        </div>
      </div>

    </div>
  );
}
