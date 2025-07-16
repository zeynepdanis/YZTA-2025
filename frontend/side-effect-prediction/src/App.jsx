import React, { useState } from 'react';
import './App.css'; // App.css dosyasını zaten kullanıyorsunuz.

function App() {
  const [drugName, setDrugName] = useState('');
  const [age, setAge] = useState('');
  const [gender, setGender] = useState('');
  const [predictedSideEffect, setPredictedSideEffect] = useState(null);
  const [allSideEffects, setAllSideEffects] = useState([]);
  const [similarDrugs, setSimilarDrugs] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    setPredictedSideEffect(null);
    setAllSideEffects([]);
    setSimilarDrugs([]);

    try {
      // Backend API endpoint'i (şimdilik varsayımsal bir URL, kendi Flask backend URL'niz olacak)
      const response = await fetch('http://localhost:5000/predict_side_effect', { // Backend'inizin çalıştığı port ve endpoint'i buraya yazın
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ drugName, age: parseInt(age), gender }),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || 'API isteği başarısız oldu.');
      }

      const data = await response.json();
      setPredictedSideEffect(data.predicted_side_effect);
      setAllSideEffects(data.all_side_effects || []); // API'den tüm yan etkiler geliyorsa
      setSimilarDrugs(data.similar_drugs || []);     // API'den benzer ilaçlar geliyorsa

    } catch (err) {
      console.error("API hatası:", err);
      setError('Veri getirilirken bir hata oluştu: ' + err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container">
      <h1>İlaç Yan Etki Tahmin ve Alternatif Öneri Sistemi</h1>

      <form onSubmit={handleSubmit} className="prediction-form">
        <div className="form-group">
          <label htmlFor="drugName">İlaç Adı:</label>
          <input
            type="text"
            id="drugName"
            value={drugName}
            onChange={(e) => setDrugName(e.target.value)}
            required
          />
        </div>

        <div className="form-group">
          <label htmlFor="age">Yaş:</label>
          <input
            type="number"
            id="age"
            value={age}
            onChange={(e) => setAge(e.target.value)}
            required
            min="1"
            max="120"
          />
        </div>

        <div className="form-group">
          <label htmlFor="gender">Cinsiyet:</label>
          <select
            id="gender"
            value={gender}
            onChange={(e) => setGender(e.target.value)}
            required
          >
            <option value="">Seçiniz...</option>
            <option value="male">Erkek</option>
            <option value="female">Kadın</option>
            <option value="other">Diğer</option>
          </select>
        </div>

        <button type="submit" disabled={loading}>
          {loading ? 'Yükleniyor...' : 'Yan Etkiyi Tahmin Et'}
        </button>
      </form>

      {error && <p className="error-message">{error}</p>}

      {predictedSideEffect && (
        <div className="results-section">
          <h2>Tahmin Sonuçları</h2>
          <div className="result-card">
            <h3>Tahmin Edilen Yan Etki:</h3>
            <p className="predicted-effect">{predictedSideEffect}</p>
          </div>

          {allSideEffects.length > 0 && (
            <div className="result-card">
              <h3>İlaca Ait Bilinen Tüm Yan Etkiler:</h3>
              <ul className="side-effects-list">
                {allSideEffects.map((effect, index) => (
                  <li key={index}>{effect}</li>
                ))}
              </ul>
            </div>
          )}

          {similarDrugs.length > 0 && (
            <div className="result-card">
              <h3>Benzer Yan Etki Profili Olan Alternatif İlaçlar:</h3>
              <ul className="similar-drugs-list">
                {similarDrugs.map((drug, index) => (
                  <li key={index}>{drug}</li>
                ))}
              </ul>
            </div>
          )}
        </div>
      )}
    </div>
  );
}

export default App;