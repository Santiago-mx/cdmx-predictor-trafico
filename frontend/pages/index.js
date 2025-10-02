import { useState, useEffect } from 'react';
import { useState, useEffect } from 'react';
import axios from 'axios';

export default function Home() {
  const [prediction, setPrediction] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function fetchPrediction() {
      try {
        // Obtener la fecha de hoy en formato YYYY-MM-DD
        const today = new Date().toISOString().split('T')[0];
        const base = process.env.NEXT_PUBLIC_API_BASE || 'http://localhost:8000';
        const response = await axios.get(`${base}/v1/predict`, {
          params: { date: today, city: 'cdmx' },
        });
        setPrediction(response.data);
      } catch (err) {
        console.error(err);
      } finally {
        setLoading(false);
      }
    }
    fetchPrediction();
  }, []);

  if (loading) {
    return <p>Cargando...</p>;
  }

  if (!prediction) {
    return <p>No se pudo obtener la predicción.</p>;
  }

  return (
    <div style={{ maxWidth: '600px', margin: '0 auto', padding: '1rem' }}>
      <h1 style={{ fontSize: '2rem', fontWeight: 'bold' }}>Predicción de tráfico para CDMX</h1>
      <h2 style={{ fontSize: '1.5rem' }}>Nivel: {prediction.level}</h2>
      <p>Fecha: {prediction.date}</p>
      <p>Ciudad: {prediction.city}</p>
      <p>Horas pico: {prediction.peak_hours.join(', ')}</p>
      <h3 style={{ marginTop: '1rem', fontWeight: 'bold' }}>Razones:</h3>
      <ul>
        {prediction.reasons.map((reason, idx) => (
          <li key={idx}>{reason}</li>
        ))}
      </ul>
      <h3 style={{ marginTop: '1rem', fontWeight: 'bold' }}>Fuentes:</h3>
      <ul>
        {prediction.evidence.map((item, idx) => (
          <li key={idx}>
            {item.title}
            {item.url && (
              <>
                {' '}
                <a href={item.url} target="_blank" rel="noopener noreferrer">
                  enlace
                </a>
              </>
            )}
          </li>
        ))}
      </ul>
    </div>
  );
}
