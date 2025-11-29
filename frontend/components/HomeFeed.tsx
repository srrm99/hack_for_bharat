"use client";

import React, { useState, useEffect } from 'react';
import { Search, Bell, Sparkles, Mic } from 'lucide-react';
import SwipeableCard from './SwipeableCard';
import { AnimatePresence } from 'framer-motion';

interface QuickAction {
  label: string;
  icon?: string;
}

interface HomeFeedProps {
  userState: string;
  recommendations: any;
  onAskFollowUp: (query: string, context?: string) => void;
}

export default function HomeFeed({ userState, recommendations, onAskFollowUp }: HomeFeedProps) {
  const content = recommendations?.content || {};
  const hero = content.hero_section || {};
  
  const [feed, setFeed] = useState<any[]>([]);
  const [history, setHistory] = useState<{id: string, action: 'liked' | 'disliked'}[]>([]);

  // Use real feed from backend if available, otherwise empty
  useEffect(() => {
    if (recommendations?.feed && recommendations.feed.length > 0) {
      setFeed(recommendations.feed);
    } else {
        // Fallback if no live feed (or error)
        setFeed([]); 
    }
  }, [recommendations]);

  const handleSwipe = (direction: 'left' | 'right', id: string) => {
    console.log(`User ${direction === 'right' ? 'liked' : 'disliked'} item ${id}`);
    setHistory(prev => [...prev, { id, action: direction === 'right' ? 'liked' : 'disliked' }]);
    
    // Remove card from stack
    setFeed(prev => prev.filter(item => item.id !== id));
  };

  const handleChat = (item: any) => {
    // Open chat with specific context
    const context = `Context: User is asking about "${item.title}". Summary: ${item.summary}. Source: ${item.source}.`;
    onAskFollowUp(`Tell me more about "${item.title}"`, context);
  };

  return (
    <div className="max-w-md mx-auto bg-gray-50 h-screen flex flex-col font-sans overflow-hidden">
      
      {/* Header */}
      <header className="bg-white/80 backdrop-blur-md z-10 px-4 py-3 flex justify-between items-center border-b border-gray-100 shrink-0">
        <div className="flex items-center gap-2">
          <div className="w-8 h-8 bg-black rounded-full flex items-center justify-center">
            <Sparkles className="text-white w-4 h-4" />
          </div>
          <span className="font-bold text-lg">BharatAI</span>
        </div>
        <div className="flex items-center gap-4">
          <Bell className="w-6 h-6 text-gray-600" />
          <div className="w-8 h-8 bg-gradient-to-r from-purple-500 to-pink-500 rounded-full" />
        </div>
      </header>

      {/* Chips */}
      <div className="px-4 py-3 flex gap-2 overflow-x-auto no-scrollbar shrink-0 bg-white border-b border-gray-100/50">
        {['For You', 'Business', 'News', 'Tech', 'Finance'].map((chip, i) => (
          <button 
            key={chip}
            className={`whitespace-nowrap px-4 py-1.5 rounded-full text-sm font-medium transition-colors ${
              i === 0 ? 'bg-black text-white' : 'bg-white text-gray-600 border border-gray-200'
            }`}
          >
            {chip}
          </button>
        ))}
      </div>

      {/* Context Bar (Mini Hero) */}
      <div className="px-4 py-2 bg-blue-50 border-b border-blue-100 shrink-0 flex justify-between items-center">
         <span className="text-xs font-medium text-blue-700">
           {userState || "Personalizing..."}
         </span>
         <span className="text-xs text-blue-500">
            {feed.length} Stories
         </span>
      </div>

      {/* Swipeable Cards Stack */}
      <div className="flex-1 relative p-4">
        <div className="relative w-full h-full">
          <AnimatePresence>
            {feed.map((item, index) => (
              <SwipeableCard 
                key={item.id}
                item={item}
                index={index}
                onSwipe={(dir) => handleSwipe(dir, item.id)}
                onChat={() => handleChat(item)}
              />
            ))}
          </AnimatePresence>
          
          {feed.length === 0 && (
            <div className="absolute inset-0 flex flex-col items-center justify-center text-gray-400">
               <div className="w-16 h-16 bg-gray-200 rounded-full mb-4 flex items-center justify-center">
                 <Sparkles size={24} />
               </div>
               <p className="text-center px-8">Generating personalized feed... <br/>(or API limit reached)</p>
            </div>
          )}
        </div>
      </div>

      {/* Bottom Search Bar */}
      <div className="bg-white border-t border-gray-200 px-4 py-3 pb-6 md:pb-3 z-20 shrink-0">
         <div className="max-w-md mx-auto relative">
            <div className="bg-gray-100 rounded-full flex items-center px-4 py-3 shadow-inner">
               <Search className="w-5 h-5 text-gray-500 mr-3" />
               <input 
                 type="text" 
                 placeholder="Ask follow-up..." 
                 className="bg-transparent border-none outline-none flex-1 text-gray-800 placeholder-gray-500"
                 onKeyDown={(e) => {
                    if (e.key === 'Enter') {
                      onAskFollowUp((e.target as HTMLInputElement).value);
                      (e.target as HTMLInputElement).value = '';
                    }
                 }}
               />
               <div className="w-px h-6 bg-gray-300 mx-3"></div>
               <button className="text-gray-600">
                  <Mic className="w-5 h-5" />
               </button>
            </div>
         </div>
      </div>

    </div>
  );
}
