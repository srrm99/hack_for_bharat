"use client";

import { useState, useEffect } from "react";
import SignalSimulator, { Signals } from "@/components/SignalSimulator";
import HomeFeed from "@/components/HomeFeed";
import ChatOverlay from "@/components/ChatOverlay";

export default function Home() {
  const [signals, setSignals] = useState<Signals>({
    device_class: "mid_range",
    network_type: "4g",
    location: "UP",
    time_of_day: "evening",
    apps: ["khatabook", "whatsapp_business", "paytm"],
    language: "hi"
  });

  const [inferenceData, setInferenceData] = useState<any>(null);
  const [isChatOpen, setIsChatOpen] = useState(false);
  const [chatQuery, setChatQuery] = useState("");
  const [chatContext, setChatContext] = useState<string | undefined>(undefined);

  // Fetch inference when signals change
  useEffect(() => {
    const fetchInference = async () => {
      try {
        // Transform signals to match backend expected format
        const payload = {
          signals: {
            device_class: signals.device_class,
            network_type: signals.network_type,
            state: signals.location,
            time_of_day: signals.time_of_day,
            business_apps: signals.apps.filter(a => ['khatabook', 'whatsapp_business'].includes(a)),
            payment_apps_installed: signals.apps.filter(a => ['paytm'].includes(a)),
            system_language: signals.language,
            // Add defaults for required fields
            whatsapp_business_usage: signals.apps.includes('whatsapp_business') ? "yes" : "no",
            otp_message_frequency: "high" // Simulator default
          }
        };

        const res = await fetch('http://127.0.0.1:8000/v1/infer', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(payload)
        });
        
        const data = await res.json();
        if (data.success) {
          setInferenceData(data.data);
        }
      } catch (err) {
        console.error("Inference API failed:", err);
      }
    };

    // Debounce API calls
    const timer = setTimeout(fetchInference, 500);
    return () => clearTimeout(timer);
  }, [signals]);

  const handleAskFollowUp = (query: string, context?: string) => {
    setChatQuery(query);
    setChatContext(context);
    setIsChatOpen(true);
  };

  return (
    <main className="min-h-screen bg-gray-100 flex justify-center">
      {/* Mobile Container */}
      <div className="w-full max-w-md bg-white shadow-2xl min-h-screen relative overflow-hidden">
        
        {inferenceData ? (
          <HomeFeed 
            userState={inferenceData.user_need_state}
            recommendations={inferenceData}
            onAskFollowUp={handleAskFollowUp}
          />
        ) : (
          <div className="flex items-center justify-center h-screen">
            <div className="animate-pulse flex flex-col items-center">
              <div className="w-12 h-12 bg-gray-200 rounded-full mb-4"></div>
              <div className="h-4 w-32 bg-gray-200 rounded"></div>
            </div>
          </div>
        )}

        <ChatOverlay 
          isOpen={isChatOpen} 
          onClose={() => setIsChatOpen(false)}
          initialQuery={chatQuery}
          context={chatContext}
        />

      </div>

      {/* Simulator Panel (Desktop Only) */}
      <div className="hidden md:block">
        <SignalSimulator onSignalsChange={setSignals} />
      </div>
    </main>
  );
}
