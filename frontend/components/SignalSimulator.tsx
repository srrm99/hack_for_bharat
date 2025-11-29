"use client";

import React, { useState } from 'react';
import { Settings, Smartphone, Wifi, MapPin, Clock, Briefcase } from 'lucide-react';

export type Signals = {
  device_class: string;
  network_type: string;
  location: string;
  time_of_day: string;
  apps: string[];
  language: string;
};

interface SignalSimulatorProps {
  onSignalsChange: (signals: Signals) => void;
}

export default function SignalSimulator({ onSignalsChange }: SignalSimulatorProps) {
  const [isOpen, setIsOpen] = useState(false);
  const [signals, setSignals] = useState<Signals>({
    device_class: "mid_range",
    network_type: "4g",
    location: "UP",
    time_of_day: "evening",
    apps: ["khatabook", "whatsapp_business", "paytm"],
    language: "hi"
  });

  const updateSignal = (key: keyof Signals, value: any) => {
    const newSignals = { ...signals, [key]: value };
    setSignals(newSignals);
    onSignalsChange(newSignals);
  };

  const toggleApp = (app: string) => {
    const newApps = signals.apps.includes(app)
      ? signals.apps.filter(a => a !== app)
      : [...signals.apps, app];
    updateSignal('apps', newApps);
  };

  return (
    <div className={`fixed right-0 top-0 h-screen bg-white shadow-2xl transition-transform duration-300 z-50 w-80 border-l border-gray-200 ${isOpen ? 'translate-x-0' : 'translate-x-full'}`}>
      <button 
        onClick={() => setIsOpen(!isOpen)}
        className="absolute -left-12 top-4 bg-black text-white p-3 rounded-l-lg shadow-lg"
      >
        <Settings size={24} />
      </button>

      <div className="p-6 h-full overflow-y-auto">
        <h2 className="text-xl font-bold mb-6 flex items-center gap-2">
          <Smartphone size={20} />
          Signal Simulator
        </h2>

        <div className="space-y-6">
          {/* Time & Location */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2 flex items-center gap-2">
              <Clock size={16} /> Time of Day
            </label>
            <select 
              value={signals.time_of_day}
              onChange={(e) => updateSignal('time_of_day', e.target.value)}
              className="w-full p-2 border rounded-lg bg-gray-50"
            >
              <option value="morning">Morning (5AM - 12PM)</option>
              <option value="afternoon">Afternoon (12PM - 5PM)</option>
              <option value="evening">Evening (5PM - 9PM)</option>
              <option value="night">Night (9PM - 5AM)</option>
            </select>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2 flex items-center gap-2">
              <MapPin size={16} /> Location (State)
            </label>
            <select 
              value={signals.location}
              onChange={(e) => updateSignal('location', e.target.value)}
              className="w-full p-2 border rounded-lg bg-gray-50"
            >
              <option value="UP">Uttar Pradesh</option>
              <option value="MH">Maharashtra</option>
              <option value="TN">Tamil Nadu</option>
              <option value="KA">Karnataka</option>
              <option value="WB">West Bengal</option>
            </select>
          </div>

          {/* Device & Network */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2 flex items-center gap-2">
              <Wifi size={16} /> Network
            </label>
            <div className="grid grid-cols-3 gap-2">
              {['2g', '4g', 'wifi'].map((net) => (
                <button
                  key={net}
                  onClick={() => updateSignal('network_type', net)}
                  className={`p-2 rounded-lg text-sm capitalize ${signals.network_type === net ? 'bg-black text-white' : 'bg-gray-100'}`}
                >
                  {net}
                </button>
              ))}
            </div>
          </div>

          {/* Apps */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2 flex items-center gap-2">
              <Briefcase size={16} /> Installed Apps
            </label>
            <div className="space-y-2">
              {[
                { id: 'khatabook', label: 'Khatabook' },
                { id: 'whatsapp_business', label: 'WhatsApp Business' },
                { id: 'paytm', label: 'Paytm' },
                { id: 'instagram', label: 'Instagram' },
                { id: 'pubg', label: 'PUBG/BGMI' },
                { id: 'byjus', label: 'Byjus' }
              ].map((app) => (
                <div 
                  key={app.id}
                  onClick={() => toggleApp(app.id)}
                  className={`p-3 rounded-lg cursor-pointer flex items-center justify-between border ${signals.apps.includes(app.id) ? 'border-blue-500 bg-blue-50' : 'border-gray-200'}`}
                >
                  <span className="text-sm">{app.label}</span>
                  <div className={`w-4 h-4 rounded-full ${signals.apps.includes(app.id) ? 'bg-blue-500' : 'bg-gray-200'}`} />
                </div>
              ))}
            </div>
          </div>
          
          {/* Language */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">System Language</label>
            <select 
              value={signals.language}
              onChange={(e) => updateSignal('language', e.target.value)}
              className="w-full p-2 border rounded-lg bg-gray-50"
            >
              <option value="en">English</option>
              <option value="hi">Hindi</option>
              <option value="ta">Tamil</option>
              <option value="bn">Bengali</option>
            </select>
          </div>

        </div>
      </div>
    </div>
  );
}

