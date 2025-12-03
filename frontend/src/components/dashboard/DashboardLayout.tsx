import React from 'react';
import { ChatBox } from '../chat/ChatBox';
import { RankingWidget } from './widgets/RankingWidget';
import { StatsWidget } from './widgets/StatsWidget';
import { Header } from '../common/Header';

export const DashboardLayout: React.FC = () => {
  return (
    <div className="min-h-screen bg-gray-100">
      <Header />

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 py-6">
        <div className="grid grid-cols-12 gap-6">
          {/* Chat Section - 5 columns on large screens */}
          <div className="col-span-12 lg:col-span-5">
            <div className="h-[calc(100vh-180px)] sticky top-24">
              <ChatBox />
            </div>
          </div>

          {/* Dashboard Widgets - 7 columns on large screens */}
          <div className="col-span-12 lg:col-span-7 space-y-6">
            {/* Stats Summary */}
            <StatsWidget />

            {/* Rankings */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <RankingWidget limit={10} title="🏆 Top 10 UCI Ranking" />

              {/* Quick Tips Card */}
              <div className="bg-white rounded-xl shadow p-4">
                <h3 className="font-semibold text-gray-800 mb-4">💡 Cosa puoi chiedere</h3>
                <ul className="space-y-3 text-sm text-gray-600">
                  <li className="flex items-start gap-2">
                    <span className="text-blue-500">•</span>
                    <span>"Quante vittorie ha Pogacar nel 2024?"</span>
                  </li>
                  <li className="flex items-start gap-2">
                    <span className="text-blue-500">•</span>
                    <span>"Chi ha vinto il Tour de France 2024?"</span>
                  </li>
                  <li className="flex items-start gap-2">
                    <span className="text-blue-500">•</span>
                    <span>"Confronta Vingegaard e Pogacar"</span>
                  </li>
                  <li className="flex items-start gap-2">
                    <span className="text-blue-500">•</span>
                    <span>"Risultati della Milano-Sanremo 2024"</span>
                  </li>
                  <li className="flex items-start gap-2">
                    <span className="text-blue-500">•</span>
                    <span>"Chi sono i corridori dell'UAE Team?"</span>
                  </li>
                  <li className="flex items-start gap-2">
                    <span className="text-blue-500">•</span>
                    <span>"Classifica UCI aggiornata"</span>
                  </li>
                </ul>
                <p className="mt-4 text-xs text-gray-400">
                  Powered by ProCyclingStats + Claude AI
                </p>
              </div>
            </div>

            {/* Info Banner */}
            <div className="bg-gradient-to-r from-blue-500 to-blue-600 rounded-xl shadow p-6 text-white">
              <h3 className="font-bold text-lg mb-2">🚴 PCS Assistant</h3>
              <p className="text-blue-100 text-sm">
                Chiedimi qualsiasi cosa sul ciclismo professionistico.
                Posso cercare informazioni su corridori, corse, classifiche e molto altro
                direttamente da ProCyclingStats.
              </p>
            </div>
          </div>
        </div>
      </main>

      {/* Footer */}
      <footer className="bg-white border-t mt-8">
        <div className="max-w-7xl mx-auto px-4 py-4 text-center text-sm text-gray-500">
          <p>PCS Assistant - Dati da ProCyclingStats.com</p>
        </div>
      </footer>
    </div>
  );
};
