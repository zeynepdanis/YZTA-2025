import React, { useState } from 'react';
import { RefreshCcw, AlertCircle, Syringe, ClipboardList, Stethoscope, Bot, X, Search, PillBottleIcon, PillIcon } from 'lucide-react';
import logo from './assets/logo.png';

const ResultModal = ({ result, onClose, drugName }) => {
  return (
    <div className="modal-overlay">
      <div className="modal-content">
        <button className="modal-close-button" onClick={onClose}>
          <X size={24} />
        </button>
        <div className="result-card">
          <h2 className="result-title">
            <Syringe className="result-title-icon" />
            Tahmin Sonucu
          </h2>
          <p className="result-description">
            <span style={{ fontWeight: 'bold' }}>"{drugName}"</span> ilacı için olası yan etkiler:
          </p>
          
          <div className="result-item">
            <h3 className="result-item-title">
              <Stethoscope className="result-item-icon" />
              Predicted Side Effect:
            </h3>
            <p className="result-item-content">
              {result.predicted_side_effect}
            </p>
          </div>

          <div className="result-item">
            <h3 className="result-item-title">
              <ClipboardList className="result-item-icon" />
              All Side Effects:
            </h3>
            <ul className="list-group">
              {result.all_side_effects.map((effect, index) => (
                <li key={index}>{effect}</li>
              ))}
            </ul>
          </div>

          <div className="result-item">
            <h3 className="result-item-title">
              <PillIcon className="result-item-icon" />
              Similar Drugs:
            </h3>
            <ul className="list-group">
              {result.similar_drugs.map((drug, index) => (
                <li key={index}>{drug}</li>
              ))}
            </ul>
          </div>
        </div>
      </div>
    </div>
  );
};

const App = () => {
  // State variables
  const [drugName, setDrugName] = useState('');
  const [age, setAge] = useState('');
  const [gender, setGender] = useState('');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);
  const [showAssistantMessage, setShowAssistantMessage] = useState(false);

  // Backend API URL
  const API_URL = 'http://localhost:5000/predict_side_effect';

  /**
   * Handles click on the AI Assistant button.
   */
  const handleAIAssistantClick = () => {
    setShowAssistantMessage(true);
  };

  /**
   * Handles form submission, sends a request to the backend API.
   * @param {Event} e - The form submit event
   */
  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setResult(null);
    setError(null);

    try {
      const payload = {
        drugName,
        age: parseInt(age),
        gender,
      };

      const response = await fetch(API_URL, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(payload),
      });

      if (!response.ok) {
        throw new Error(`API request failed: ${response.statusText}`);
      }

      const data = await response.json();
      setResult(data);
    } catch (err) {
      console.error("API error:", err);
      setError('Tahmin alınamadı. Lütfen ağ bağlantınızı veya arka uç sunucusunu kontrol edin.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <>
      <style>
        {`
        html, body {
            height: 100%;
            margin: 0;
            padding: 0;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
            color: #1e293b;
        }
        
        #root {
            height: 100%;
            display: flex;
            align-items: center;
            justify-content: center;
        }

        .app-container {
            min-height: 100vh;
            width: 100vw;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 1.5rem;
            box-sizing: border-box;
            background-color: #a6d5d4ff;
        }
        
        .main-card {
          background-color: #fffffff4;
          border: 1px solid #e2e8f0;
          border-radius: 1.5rem;
          box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 8px 10px -6px rgba(0, 0, 0, 0.1);
          padding: 2.5rem;
          max-width: 48rem;
          width: 100%;
          display: flex;
          flex-direction: column;
          align-items: center;
          margin: auto;
        }
        
        .header {
          display: flex;
          align-items: center;
          margin-bottom: 2rem;
          border-bottom: 1px solid #e2e8f0;
          padding-bottom: 1.5rem;
          width: 100%;
          justify-content: space-between;
        }
        
        .header-logo-container {
            display: flex;
            align-items: center;
        }

        .header-logo {
            height: 200px;
            width: auto;
            margin-right: 1rem;
        }
        
        .header-title-container {
            display: flex;
            flex-direction: column;
        }
        
        .header-title {
          font-size: 2rem;
          font-weight: 800;
          color: #295c6b;
        }

        .header-subtitle {
            font-size: 1rem;
            color: #4b5563;
            margin-top: -0.25rem;
        }

        @media (max-width: 767px) {
          .header-title {
            font-size: 1.25rem;
          }
          .header-subtitle {
              font-size: 0.75rem;
          }
        }
        
        .form-container {
          width: 100%;
        }
        
        .search-section {
            display: flex;
            align-items: center;
            gap: 0.5rem;
            margin-bottom: 1.5rem;
        }

        .search-input-group {
            position: relative;
            flex: 1;
        }

        .search-icon {
            position: absolute;
            left: 1rem;
            top: 50%;
            transform: translateY(-50%);
            color: #9ca3af;
        }

        .search-bar {
            width: 100%;
            padding: 0.75rem 1rem 0.75rem 3rem;
            border: 1px solid #d1d5db;
            background-color: #fff;
            border-radius: 0.75rem;
            transition: all 0.2s ease-in-out;
            box-sizing: border-box;
            color: black;
        }

        .search-bar:focus {
          outline: 2px solid #295c6b;
          border-color: transparent;
        }

        .assistant-button {
          flex-shrink: 0;
          width: auto;
          height: auto;
          border-radius: 0.75rem;
          color: #295c6b;
          display: flex;
          align-items: center;
          justify-content: center;
          cursor: pointer;
          transition: background-color 0.2s ease-in-out;
          border: none;
          background-color: #fff;
        }
        
        .assistant-button:hover {
           border: 2px solid #295c6b;
        }

        .form-row {
          display: flex;
          flex-direction: column;
          gap: 1.25rem;
          margin-bottom: 1rem;
        }
        
        @media (min-width: 768px) {
          .form-row {
            flex-direction: row;
          }
        }
        
        .form-group {
          flex: 1;
        }
        
        .label {
          display: block;
          color: #374151;
          font-weight: 600;
          margin-bottom: 0.5rem;
        }
        
        .input-field{
          width: 100%;
          padding: 0.75rem 1rem;
          border: 1px solid #d1d5db;
          border-radius: 0.75rem;
          transition: all 0.2s ease-in-out;
          background-color: #fff;
         box-sizing: border-box;
         color: black;
        }
        .select-field {
          width: 100%;
          height: auto;
          padding: 0.75rem 1rem;
          border: 1px solid #e5e7eb;
          border-radius: 0.75rem;
          background-color: #295c6b;
          box-sizing: border-box;
          font-size: 1rem;
          outline: none;
          transition: 
            border-color 0.2s ease, 
            box-shadow 0.2s ease, 
            background-color 0.2s;
          box-shadow: 0 1px 2px 0 rgba(16, 24, 40, 0.03);
          color: white;
        }

        .select-field:hover {
          border-color: #3c869dff;
       
        }

        .select-field:focus {
          border-color: #295c6b;
          box-shadow: 0 2px 8px 0 rgba(41, 92, 107, 0.15);
     
        }

        .input-field:focus {
          outline: 2px solid #295c6b;
          border-color: transparent;
        }

        .assistant-help-section {
          display: flex;
          align-items: center;
          justify-content: flex-end;
          gap: 0.5rem;
          margin-top: 1rem;
          width: 100%;
        }

        .assistant-help-text {
            color: #4b5563;
            font-size: 0.875rem;
        }

        .submit-button {
          width: 100%;
          margin-top: 1.5rem;
          padding: 0.75rem 1.5rem;
          background-color: #295c6b;
          color: #fff;
          font-weight: 700;
          border-radius: 0.75rem;
          box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -4px rgba(0, 0, 0, 0.1);
          transition: all 0.2s ease-in-out;
          display: flex;
          align-items: center;
          justify-content: center;
          border: none;
          cursor: pointer;
        }
        
        .submit-button:hover {
          background-color: #1a3d46;
        }
        
        .submit-button:disabled {
          opacity: 0.5;
          cursor: not-allowed;
        }
        
        .loading-icon {
          animation: spin 1s linear infinite;
          margin-right: 0.5rem;
        }
        
        @keyframes spin {
          from { transform: rotate(0deg); }
          to { transform: rotate(360deg); }
        }

        .results-section {
          display: none; /* Sonuç bölümünü gizle */
        }
        
        .modal-overlay {
          position: fixed;
          top: 0;
          left: 0;
          width: 100%;
          height: 100%;
          background-color: rgba(0, 0, 0, 0.7);
          display: flex;
          justify-content: center;
          align-items: center;
          z-index: 1000;
        }

        .modal-content {
          background-color: #fffffff4;
          padding: 2.5rem;
          border-radius: 1.5rem;
          max-width: 48rem;
          width: 90%;
          position: relative;
          box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25);
          overflow-y: auto;
          max-height: 90vh;
        }

        .modal-close-button {
          position: absolute;
          top: 1.5rem;
          right: 1.5rem;
          background: none;
          border: none;
          cursor: pointer;
          color: #4b5563;
        }

        .result-card {
            background: none;
            border: none;
            box-shadow: none;
            padding: 0;
        }

        .result-title {
          font-size: 1.75rem;
          font-weight: 800;
          color: #047857;
          margin-bottom: 1.5rem;
        }

        .result-description {
            font-size: 1rem;
            color: #4b5563;
            margin-bottom: 1.5rem;
        }
        
        .result-item {
          margin-bottom: 2rem;
        }

        .result-item-title {
          font-weight: 700;
          font-size: 1.25rem;
          color: #047857;
          display: flex;
          align-items: center;
          margin-bottom: 0.5rem;
        }
        
        .result-item-icon {
          width: 1.5rem;
          height: 1.5rem;
          margin-right: 0.75rem;
        }
        
        .result-item-content {
          margin-top: 0.5rem;
          font-size: 1.5rem;
          font-weight: 800;
          color: #064e3b;
        }
        
        .list-group {
          list-style-type: disc;
          list-style-position: inside;
          margin-top: 0.75rem;
          color: #4b5563;
          padding-left: 1rem;
        }

        .list-group li {
            margin-bottom: 0.5rem;
        }

        .error-card {
          background-color: #fee2e2;
          border-left: 4px solid #ef4444;
          color: #b91c1c;
          padding: 1.5rem;
          border-radius: 0.75rem;
          box-shadow: inset 0 2px 4px 0 rgba(0, 0, 0, 0.06);
          display: flex;
          align-items: center;
          margin-top: 2.5rem;
        }
        
        .error-icon {
          width: 1.5rem;
          height: 1.5rem;
          margin-right: 0.75rem;
          flex-shrink: 0;
        }
        
        .error-text {
          font-weight: 600;
        }

        .message-modal {
          position: fixed;
          top: 50%;
          left: 50%;
          transform: translate(-50%, -50%);
          background-color: #fefcbf;
          border: 1px solid #fcd34d;
          color: #92400e;
          padding: 1.5rem;
          border-radius: 0.75rem;
          box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -4px rgba(0, 0, 0, 0.1);
          z-index: 1000;
          display: flex;
          align-items: center;
        }

        .message-content {
          flex: 1;
        }
        
        .message-close-button {
          background: none;
          border: none;
          color: #92400e;
          cursor: pointer;
          margin-left: 1rem;
        }
        
        `}
      </style>

      <div className="app-container">
        <div className="main-card">
          {/* Header */}
          <header className="header">
            <div className="header-logo-container">
              <img src={logo} alt="SideWise Logo" className="header-logo"/>
              <div className="header-title-container">
                <h1 className="header-title">SideWise</h1>
                <p className="header-subtitle">Your AI-Powered Medication Guide</p>
                <p className="header-subtitle">Find information on drug ingredients and side effects</p>
              </div>
            </div>
          </header>

          {/* Form */}
          <form onSubmit={handleSubmit} className="form-container">
            <div className="search-section">
                <div className="search-input-group">
                    <Search className="search-icon" size={20} />
                    <input
                        type="text"
                        id="drugName"
                        value={drugName}
                        onChange={(e) => setDrugName(e.target.value)}
                        className="search-bar"
                        placeholder="Search for a drug"
                        required
                    />
                </div>
            </div>
            
            <div className="form-row">
              <div className="form-group">
                <label htmlFor="gender" className="label">
                  Gender
                </label>
                <select
                  id="gender"
                  value={gender}
                  onChange={(e) => setGender(e.target.value)}
                  className="select-field"
                  required
                >
                  <option value="">Select...</option>
                  <option value="Female">Female</option>
                  <option value="Male">Male</option>
                  <option value="Other">Other</option>
                </select>
              </div>
              <div className="form-group">
                <label htmlFor="age" className="label">
                  Age
                </label>
                <input
                  type="number"
                  id="age"
                  value={age}
                  onChange={(e) => setAge(e.target.value)}
                  className="input-field"
                  placeholder="e.g. 20"
                  min="0"
                  required
                />
              </div>
            </div>
            
            <div className="assistant-help-section">
                <span className="assistant-help-text">Need Help?</span>
                <button type="button" onClick={handleAIAssistantClick} className="assistant-button">
                    <Bot size={30} />
                </button>
            </div>

            <button
              type="submit"
              disabled={loading}
              className="submit-button"
            >
              {loading ? (
                <>
                  <RefreshCcw className="loading-icon" />
                  Loading...
                </>
              ) : (
                'Predict Side Effect'
              )}
            </button>
          </form>

          {/* Error Section */}
          {error && (
            <div className="error-card">
              <AlertCircle className="error-icon" />
              <p className="error-text">{error}</p>
            </div>
          )}
        </div>
      </div>
      
      {/* Result Modal */}
      {result && (
        <ResultModal
          result={result}
          onClose={() => setResult(null)}
          drugName={drugName}
        />
      )}

      {/* AI Assistant Message Modal */}
      {showAssistantMessage && (
        <div className="message-modal">
          <p className="message-content">AI Assistant is currently under development.</p>
          <button onClick={() => setShowAssistantMessage(false)} className="message-close-button">
            <X size={20} />
          </button>
        </div>
      )}
    </>
  );
};

export default App;
