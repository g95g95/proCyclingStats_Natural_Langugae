import { useState, useCallback } from 'react';
import { chatApi } from '../services/api';
import { ChatMessage, ChatResponse, VisualizationData } from '../types';

interface UseChatReturn {
  messages: ChatMessage[];
  isLoading: boolean;
  error: string | null;
  lastVisualization: VisualizationData | null;
  lastData: Record<string, unknown> | null;
  sendMessage: (content: string) => Promise<void>;
  clearMessages: () => void;
}

export function useChat(): UseChatReturn {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [lastVisualization, setLastVisualization] = useState<VisualizationData | null>(null);
  const [lastData, setLastData] = useState<Record<string, unknown> | null>(null);

  const sendMessage = useCallback(async (content: string) => {
    if (!content.trim()) return;

    const userMessage: ChatMessage = { role: 'user', content };
    setMessages(prev => [...prev, userMessage]);
    setIsLoading(true);
    setError(null);

    try {
      const response: ChatResponse = await chatApi.sendMessage(content, messages);

      const assistantMessage: ChatMessage = {
        role: 'assistant',
        content: response.message,
      };

      setMessages(prev => [...prev, assistantMessage]);

      if (response.visualization) {
        setLastVisualization(response.visualization);
      }

      if (response.data) {
        setLastData(response.data);
      }
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Failed to send message';
      setError(errorMessage);

      // Add error message to chat
      setMessages(prev => [
        ...prev,
        {
          role: 'assistant',
          content: `Mi dispiace, si è verificato un errore: ${errorMessage}. Per favore riprova.`,
        },
      ]);
    } finally {
      setIsLoading(false);
    }
  }, [messages]);

  const clearMessages = useCallback(() => {
    setMessages([]);
    setLastVisualization(null);
    setLastData(null);
    setError(null);
  }, []);

  return {
    messages,
    isLoading,
    error,
    lastVisualization,
    lastData,
    sendMessage,
    clearMessages,
  };
}
