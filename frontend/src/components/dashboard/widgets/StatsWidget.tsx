import React, { useEffect, useState } from 'react';
import { statsApi } from '../../../services/api';

interface StatCardProps {
  title: string;
  value: string | number;
  icon: string;
  change?: string;
}

const StatCard: React.FC<StatCardProps> = ({ title, value, icon, change }) => {
  const isPositive = change?.startsWith('+');
  const isNeutral = change === '0' || !change;

  return (
    <div className="bg-white rounded-xl shadow p-4 hover:shadow-md transition-shadow">
      <div className="flex items-center justify-between mb-2">
        <span className="text-2xl">{icon}</span>
        {change && (
          <span
            className={`text-sm font-medium ${
              isNeutral
                ? 'text-gray-500'
                : isPositive
                ? 'text-green-500'
                : 'text-red-500'
            }`}
          >
            {change}
          </span>
        )}
      </div>
      <p className="text-2xl font-bold text-gray-800">
        {typeof value === 'number' ? value.toLocaleString() : value}
      </p>
      <p className="text-sm text-gray-500">{title}</p>
    </div>
  );
};

export const StatsWidget: React.FC = () => {
  const [stats, setStats] = useState<Record<string, number>>({});
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const fetchStats = async () => {
      try {
        const data = await statsApi.getSummary();
        setStats(data);
      } catch (error) {
        console.error('Failed to fetch stats:', error);
      } finally {
        setIsLoading(false);
      }
    };

    fetchStats();
  }, []);

  if (isLoading) {
    return (
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        {[...Array(4)].map((_, i) => (
          <div key={i} className="bg-white rounded-xl shadow p-4 animate-pulse">
            <div className="h-8 bg-gray-200 rounded w-1/2 mb-2" />
            <div className="h-6 bg-gray-200 rounded w-3/4" />
          </div>
        ))}
      </div>
    );
  }

  return (
    <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
      <StatCard
        title="Corse Totali"
        value={stats.total_races || 892}
        icon="🏁"
        change="+12"
      />
      <StatCard
        title="Corridori Attivi"
        value={stats.active_riders || 2847}
        icon="🚴"
        change="+45"
      />
      <StatCard
        title="Team WorldTour"
        value={stats.worldtour_teams || 18}
        icon="👥"
      />
      <StatCard
        title="Giorni di Gara"
        value={stats.race_days || 342}
        icon="📆"
        change="-3"
      />
    </div>
  );
};
