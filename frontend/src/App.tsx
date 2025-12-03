import React from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { Home } from './pages/Home';
import { RankingsPage } from './pages/RankingsPage';

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/rankings" element={<RankingsPage />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
