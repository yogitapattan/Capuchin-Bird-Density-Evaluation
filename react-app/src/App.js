import React, { useState } from 'react';
import './App.css';
import { evaluateCapuchinDensity } from './api-service';

const App = () => {
  const [audioFile, setAudioFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [results, setResults] = useState(null);

  const handleFileChange = (event) => {
    const file = event.target.files[0];
    setAudioFile(file);
    setResults(null);
  };

  const handleSubmit = () => {
    setLoading(true);
    
    evaluateCapuchinDensity(audioFile).then((response) => {
      setResults(response.data);
    }).catch((error) => {
      console.error('Error:', error);
    })

    setLoading(false);
  };

  return (
    <div className="app">
      <div className="card">
        <header>
          <h1>Capuchin Bird Density Assessment</h1>
          <p>
            A deep learning model that accurately classifies Capuchin bird sounds and evaluates bird density in different forest locations, enabling applications in monitoring bird populations, assessing biodiversity, and supporting environmental impact assessments, with potential implications for ecological conservation and environmental planning.{' '} 
            <a href='https://github.com/yogitapattan/Capuchin-Bird-Density-Evaluation' target='_blank'>Here's the Github Repo!</a>
          </p>
          <p><b>Instructions: </b>Please follow the below steps to test the model using sample forest recordings.</p>
          <ul className="instructions">
            <li>Select and download a forest recording from <a href='https://drive.google.com/drive/folders/1y5awpxDMqMxXgKuPHb-xKFQmVpZ37oL6?usp=sharing' target='_blank'>here</a>.</li>
            <li>Click on Choose file button and Upload the recording.</li>
            <li>The Capuchin bird audio count and density is displayed.</li>
          </ul>
        </header>
        <section>
          <h2>Upload an Audio File</h2>
          <input type="file" accept="audio/*" onChange={handleFileChange} />
          <button onClick={handleSubmit} disabled={!audioFile || loading}>
            {loading ? 'Loading...' : 'Submit'}
          </button>
          {results && (
            <div className="results">
              <h3>Results:</h3>
              <p>Capuchin Audio Count: <b>{results.capuchin_count}</b></p>
              <p>Evaluated Density: <b>{results.density}</b></p>
            </div>
          )}
        </section>
        <footer>
          <p>© Yogita Pattan</p>
        </footer>
      </div>
    </div>
  );
};

export default App;
