import React, { useRef, useEffect } from 'react';
import { useChat } from '../../hooks/useChat';
import { ChatMessage } from './ChatMessage';
import { ChatInput } from './ChatInput';
import { DynamicChart } from '../charts/DynamicChart';

export const ChatBox: React.FC = () => {
  const {
    messages,
    isLoading,
    lastVisualization,
    sendMessage,
    clearMessages,
  } = useChat();

  const messagesEndRef = useRef<HTMLDivElement>(null);

  // Auto-scroll to bottom
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const exampleQueries = [
    "Quante vittorie ha Pogacar nel 2024?",
    "Chi ha vinto il Tour de France 2024?",
    "Confronta Pogacar e Vingegaard",
    "Mostra la classifica UCI",
  ];

  return (
    <div className="flex flex-col h-full bg-white rounded-xl shadow-lg overflow-hidden">
      {/* Header */}
      <div className="flex items-center justify-between p-4 border-b bg-gradient-to-r from-blue-500 to-blue-600">
        <div className="flex items-center gap-2">
          <span className="text-2xl">🚴</span>
          <h2 className="text-lg font-semibold text-white">PCS Assistant</h2>
        </div>
        <button
          onClick={clearMessages}
          className="text-sm text-white/80 hover:text-white transition-colors"
        >
          Nuova chat
        </button>
      </div>

      {/* Messages */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4 bg-gray-50">
        {messages.length === 0 && (
          <div className="text-center text-gray-500 mt-8">
            <p className="text-lg mb-2">Ciao! Sono il tuo assistente ciclismo.</p>
            <p className="text-sm mb-6">Chiedimi qualsiasi cosa su ciclisti, corse, classifiche...</p>
            <div className="space-y-2">
              <p className="text-xs text-gray-400 mb-3">Prova a chiedere:</p>
              {exampleQueries.map((query, index) => (
                <button
                  key={index}
                  onClick={() => sendMessage(query)}
                  className="block mx-auto text-sm text-blue-500 hover:text-blue-700 hover:underline"
                >
                  "{query}"
                </button>
              ))}
            </div>
          </div>
        )}

        {messages.map((message, index) => (
          <ChatMessage key={index} message={message} />
        ))}

        {/* Show visualization after last assistant message */}
        {lastVisualization && messages.length > 0 && messages[messages.length - 1].role === 'assistant' && (
          <div className="mt-4 p-4 bg-white rounded-lg shadow">
            <DynamicChart
              type={lastVisualization.type}
              data={lastVisualization.data}
              title={lastVisualization.title}
            />
          </div>
        )}

        {isLoading && (
          <div className="flex items-center gap-2 text-gray-500">
            <div className="animate-spin h-4 w-4 border-2 border-blue-500 border-t-transparent rounded-full" />
            <span>Sto cercando...</span>
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>

      {/* Input */}
      <ChatInput onSend={sendMessage} disabled={isLoading} />
    </div>
  );
};
