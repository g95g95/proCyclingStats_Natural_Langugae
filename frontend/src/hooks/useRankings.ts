import { useState, useEffect, useCallback } from 'react';
import { rankingsApi } from '../services/api';
import { RankingEntry } from '../types';

interface UseRankingsReturn {
  rankings: RankingEntry[];
  isLoading: boolean;
  error: string | null;
  refresh: () => Promise<void>;
}

export function useRankings(limit = 50): UseRankingsReturn {
  const [rankings, setRankings] = useState<RankingEntry[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchRankings = useCallback(async () => {
    setIsLoading(true);
    setError(null);

    try {
      const data = await rankingsApi.getIndividual(limit);
      setRankings(data.ranking || []);
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Failed to fetch rankings';
      setError(errorMessage);
    } finally {
      setIsLoading(false);
    }
  }, [limit]);

  useEffect(() => {
    fetchRankings();
  }, [fetchRankings]);

  return {
    rankings,
    isLoading,
    error,
    refresh: fetchRankings,
  };
}
