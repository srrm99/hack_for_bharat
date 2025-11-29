"use client";

import React, { useState, useRef } from 'react';
import { motion, useMotionValue, useTransform, PanInfo } from 'framer-motion';
import { MessageCircle, X, Heart, Share2 } from 'lucide-react';

interface CardProps {
  item: any;
  onSwipe: (direction: 'left' | 'right') => void;
  onChat: () => void;
  index: number;
}

export default function SwipeableCard({ item, onSwipe, onChat, index }: CardProps) {
  const x = useMotionValue(0);
  const rotate = useTransform(x, [-200, 200], [-15, 15]);
  const opacity = useTransform(x, [-200, -100, 0, 100, 200], [0, 1, 1, 1, 0]);
  
  // Background color indicators
  const bgRight = useTransform(x, [0, 200], ["rgba(0,0,0,0)", "rgba(16, 185, 129, 0.2)"]);
  const bgLeft = useTransform(x, [-200, 0], ["rgba(239, 68, 68, 0.2)", "rgba(0,0,0,0)"]);

  const handleDragEnd = (event: MouseEvent | TouchEvent | PointerEvent, info: PanInfo) => {
    if (info.offset.x > 100) {
      onSwipe('right');
    } else if (info.offset.x < -100) {
      onSwipe('left');
    }
  };

  return (
    <motion.div
      style={{ 
        x, 
        rotate, 
        opacity,
        zIndex: 100 - index,
        position: 'absolute',
        top: 0,
        left: 0,
        width: '100%',
        height: '100%',
      }}
      drag="x"
      dragConstraints={{ left: 0, right: 0 }}
      onDragEnd={handleDragEnd}
      className="w-full h-full p-4"
    >
      <motion.div 
        className="relative w-full h-full bg-white rounded-3xl shadow-xl overflow-hidden border border-gray-100 flex flex-col"
      >
        {/* Swipe Indicators */}
        <motion.div style={{ opacity: useTransform(x, [0, 100], [0, 1]) }} className="absolute top-8 left-8 z-20 border-4 border-green-500 text-green-500 rounded-lg px-4 py-2 font-bold text-2xl transform -rotate-12">
          INTERESTED
        </motion.div>
        <motion.div style={{ opacity: useTransform(x, [-100, 0], [1, 0]) }} className="absolute top-8 right-8 z-20 border-4 border-red-500 text-red-500 rounded-lg px-4 py-2 font-bold text-2xl transform rotate-12">
          SKIP
        </motion.div>

        {/* Image Section */}
        <div className="relative h-1/2 bg-gray-200">
          {item.image ? (
            <img src={item.image} alt={item.title} className="w-full h-full object-cover" />
          ) : (
            <div className="w-full h-full bg-gradient-to-br from-gray-800 to-gray-900 flex items-center justify-center p-6">
               <h3 className="text-white font-bold text-xl text-center">{item.title}</h3>
            </div>
          )}
          <div className="absolute inset-0 bg-gradient-to-t from-black/80 via-transparent to-transparent" />
          
          <div className="absolute bottom-4 left-4 right-4 text-white">
            <div className="flex items-center gap-2 text-xs opacity-80 mb-2">
              <span className="bg-white/20 px-2 py-0.5 rounded backdrop-blur-sm">{item.source || "News"}</span>
              <span>•</span>
              <span>{item.time || "Today"}</span>
            </div>
            <h2 className="font-bold text-xl leading-tight shadow-black drop-shadow-md">
              {item.image ? item.title : ""}
            </h2>
          </div>
        </div>

        {/* Content Section */}
        <div className="flex-1 p-6 flex flex-col justify-between bg-white relative">
          <motion.div style={{ background: bgRight }} className="absolute inset-0 pointer-events-none" />
          <motion.div style={{ background: bgLeft }} className="absolute inset-0 pointer-events-none" />

          <div>
            <p className="text-gray-600 leading-relaxed text-base">
              {item.summary || item.content || "Swipe right to learn more about this topic or chat with our AI assistant for specific details."}
            </p>
            
            <div className="mt-4 flex flex-wrap gap-2">
              {item.tags?.map((tag: string) => (
                <span key={tag} className="text-xs bg-gray-100 text-gray-600 px-2 py-1 rounded-full">#{tag}</span>
              ))}
            </div>
          </div>

          {/* Actions */}
          <div className="flex items-center justify-between mt-4 pt-4 border-t border-gray-100 z-10">
            <button onClick={() => onSwipe('left')} className="p-3 rounded-full bg-gray-100 text-gray-500 hover:bg-red-50 hover:text-red-500 transition-colors">
              <X size={24} />
            </button>
            
            <button 
              onClick={onChat}
              className="flex items-center gap-2 px-6 py-3 bg-black text-white rounded-full font-medium shadow-lg hover:bg-gray-800 transition-transform active:scale-95"
            >
              <MessageCircle size={20} />
              <span>Chat</span>
            </button>

            <button onClick={() => onSwipe('right')} className="p-3 rounded-full bg-gray-100 text-gray-500 hover:bg-green-50 hover:text-green-500 transition-colors">
              <Heart size={24} />
            </button>
          </div>
        </div>
      </motion.div>
    </motion.div>
  );
}

