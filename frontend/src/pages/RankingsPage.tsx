import React from 'react';
import { Header } from '../components/common/Header';
import { RankingWidget } from '../components/dashboard/widgets/RankingWidget';

export const RankingsPage: React.FC = () => {
  return (
    <div className="min-h-screen bg-gray-100">
      <Header />

      <main className="max-w-7xl mx-auto px-4 py-6">
        <h1 className="text-2xl font-bold text-gray-800 mb-6">Classifiche UCI</h1>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <RankingWidget limit={50} title="🏆 Classifica Individuale" />

          <div className="bg-white rounded-xl shadow p-6">
            <h3 className="font-semibold text-gray-800 mb-4">Informazioni</h3>
            <p className="text-gray-600 text-sm mb-4">
              La classifica UCI viene aggiornata settimanalmente e tiene conto dei
              risultati ottenuti nelle corse del calendario internazionale.
            </p>
            <p className="text-gray-600 text-sm">
              I punti vengono assegnati in base al tipo di corsa e al piazzamento
              finale di ogni corridore.
            </p>
          </div>
        </div>
      </main>
    </div>
  );
};
