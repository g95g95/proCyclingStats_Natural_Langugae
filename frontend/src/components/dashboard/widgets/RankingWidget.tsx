import React from 'react';
import { useRankings } from '../../../hooks/useRankings';
import { useWebSocket } from '../../../hooks/useWebSocket';
import { RankingEntry } from '../../../types';

interface RankingWidgetProps {
  limit?: number;
  title?: string;
}

// Flag emoji mapping
const getFlagEmoji = (nationality: string): string => {
  const flags: Record<string, string> = {
    SI: '🇸🇮', BE: '🇧🇪', DK: '🇩🇰', NL: '🇳🇱', GB: '🇬🇧',
    FR: '🇫🇷', IT: '🇮🇹', ES: '🇪🇸', CO: '🇨🇴', US: '🇺🇸',
    DE: '🇩🇪', AU: '🇦🇺', EC: '🇪🇨', PL: '🇵🇱', PT: '🇵🇹',
    SL: '🇸🇮', NO: '🇳🇴', CH: '🇨🇭', AT: '🇦🇹', IE: '🇮🇪',
    CA: '🇨🇦', NZ: '🇳🇿', ER: '🇪🇷', RU: '🇷🇺', KZ: '🇰🇿',
  };
  return flags[nationality?.toUpperCase()] || '🏳️';
};

export const RankingWidget: React.FC<RankingWidgetProps> = ({
  limit = 10,
  title = 'PCS Ranking',
}) => {
  const { rankings, isLoading, error, refresh } = useRankings(limit);
  const { isConnected } = useWebSocket({
    onMessage: (msg) => {
      if (msg.type === 'ranking_update') {
        refresh();
      }
    },
  });

  const getRankChange = (entry: RankingEntry) => {
    if (!entry.prev_rank) return { symbol: '–', class: 'text-gray-400', value: 0 };
    const change = entry.prev_rank - entry.rank;
    if (change > 0) return { symbol: '▲', class: 'text-green-500', value: change };
    if (change < 0) return { symbol: '▼', class: 'text-red-500', value: Math.abs(change) };
    return { symbol: '–', class: 'text-gray-400', value: 0 };
  };

  if (isLoading) {
    return (
      <div className="bg-white rounded-xl shadow p-4">
        <div className="animate-pulse">
          <div className="h-6 bg-gray-200 rounded w-1/2 mb-4" />
          {[...Array(limit)].map((_, i) => (
            <div key={i} className="h-12 bg-gray-100 rounded mb-2" />
          ))}
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="bg-white rounded-xl shadow p-4">
        <h3 className="font-semibold text-gray-800 mb-2">{title}</h3>
        <p className="text-red-500 text-sm">{error}</p>
        <button
          onClick={refresh}
          className="mt-2 text-sm text-blue-500 hover:underline"
        >
          Riprova
        </button>
      </div>
    );
  }

  return (
    <div className="bg-white rounded-xl shadow overflow-hidden">
      <div className="p-4 border-b flex items-center justify-between bg-gradient-to-r from-gray-50 to-white">
        <h3 className="font-semibold text-gray-800">{title}</h3>
        <div className="flex items-center gap-2">
          {isConnected && (
            <span className="w-2 h-2 bg-green-500 rounded-full animate-pulse" title="Live" />
          )}
          <button
            onClick={refresh}
            className="text-xs text-gray-500 hover:text-gray-700"
            title="Aggiorna"
          >
            ↻
          </button>
        </div>
      </div>

      <div className="divide-y max-h-[400px] overflow-y-auto">
        {rankings.slice(0, limit).map((entry) => {
          const change = getRankChange(entry);
          return (
            <div
              key={entry.rank}
              className="flex items-center p-3 hover:bg-gray-50 transition-colors"
            >
              <span className="w-8 text-lg font-bold text-gray-400">
                {entry.rank}
              </span>

              <span className={`w-10 text-sm ${change.class}`}>
                {change.symbol}
                {change.value > 0 && <span className="text-xs">{change.value}</span>}
              </span>

              <span className="text-xl mr-2">
                {getFlagEmoji(entry.nationality || '')}
              </span>

              <div className="flex-1 min-w-0">
                <p className="font-medium text-gray-800 truncate">
                  {entry.rider_name}
                </p>
                <p className="text-xs text-gray-500 truncate">
                  {entry.team_name}
                </p>
              </div>

              <span className="font-semibold text-blue-600 ml-2">
                {entry.points?.toLocaleString()}
              </span>
            </div>
          );
        })}
      </div>
    </div>
  );
};
