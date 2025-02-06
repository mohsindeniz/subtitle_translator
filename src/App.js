import React, { useState } from 'react';
import './App.css';
import { translateText } from './services/translationService';

function App() {
  const [subtitleText, setSubtitleText] = useState('');
  const [translatedText, setTranslatedText] = useState('');

  const handleFileUpload = (event) => {
    const file = event.target.files[0];
    const reader = new FileReader();
    
    reader.onload = (e) => {
      setSubtitleText(e.target.result);
    };
    
    reader.readAsText(file);
  };

  const handleTranslate = async () => {
    try {
      const result = await translateText(subtitleText);
      setTranslatedText(result);
    } catch (error) {
      console.error('Çeviri hatası:', error);
    }
  };

  return (
    <div className="App">
      <h1>Altyazı Çeviri Uygulaması</h1>
      
      <div className="upload-section">
        <input 
          type="file" 
          accept=".srt,.sub"
          onChange={handleFileUpload} 
        />
      </div>

      <div className="subtitle-container">
        <div className="original-text">
          <h3>Orijinal Metin</h3>
          <textarea 
            value={subtitleText}
            onChange={(e) => setSubtitleText(e.target.value)}
            rows={10}
          />
        </div>

        <div className="translated-text">
          <h3>Çevrilmiş Metin</h3>
          <textarea 
            value={translatedText}
            readOnly
            rows={10}
          />
        </div>
      </div>

      <button onClick={handleTranslate}>Çevir</button>
    </div>
  );
}

export default App; 