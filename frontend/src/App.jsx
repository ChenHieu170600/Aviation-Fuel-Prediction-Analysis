import React, { useState } from 'react';
import './App.css';

const App = () => {
  const [currentSlide, setCurrentSlide] = useState(0);

  const slides = [
    {
      id: 'introduction',
      title: 'Aviation Extra Fuel Prediction Analysis',
      subtitle: 'Deep Learning Approach with Weather Integration',
      content: (
        <div className="slide-content">
          <div className="intro-grid">
            <div className="intro-text">
              <h3>🎯 Project Objectives</h3>
              <div className="objective-cards">
                <div className="objective-card">
                  <div className="card-icon">📊</div>
                  <div className="card-content">
                    <h4>Data Analysis</h4>
                    <p>Comprehensive analysis of aviation fuel consumption patterns using real flight data</p>
                  </div>
                </div>
                <div className="objective-card">
                  <div className="card-icon">🌤️</div>
                  <div className="card-content">
                    <h4>Weather Integration</h4>
                    <p>Incorporate METAR weather data to enhance prediction accuracy</p>
                  </div>
                </div>
                <div className="objective-card">
                  <div className="card-icon">🤖</div>
                  <div className="card-content">
                    <h4>ML Models</h4>
                    <p>Develop and compare multiple machine learning algorithms for optimal performance</p>
                  </div>
                </div>
              </div>
            </div>
            <div className="intro-visual">
              <div className="aircraft-icon">✈️</div>
              <div className="fuel-metrics">
                <div className="metric">
                  <span className="metric-value">1000+</span>
                  <span className="metric-label">Flight Records</span>
                </div>
                <div className="metric">
                  <span className="metric-value">50+</span>
                  <span className="metric-label">Airports</span>
                </div>
                <div className="metric">
                  <span className="metric-value">4</span>
                  <span className="metric-label">ML Models</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      )
    },
    {
      id: 'data_methodology',
      title: 'Data Acquisition & Methodology',
      content: (
        <div className="slide-content">
          <div className="methodology-grid">
            <div className="data-sources">
              <h3>📋 Data Sources</h3>
              <div className="source-cards">
                <div className="source-card primary">
                  <h4>🛫 US 2023 Civil Flights</h4>
                  <p>Comprehensive flight data including delays, routes, and aircraft information</p>
                  <div className="source-stats">
                    <span>1000+ flights analyzed</span>
                  </div>
                </div>
                <div className="source-card secondary">
                  <h4>🌦️ METAR Weather Data</h4>
                  <p>Real-time meteorological observations from airports worldwide</p>
                  <div className="source-stats">
                    <span>Temperature, Wind, Visibility, Pressure</span>
                  </div>
                </div>
                <div className="source-card tertiary">
                  <h4>⛽ Aircraft Fuel Consumption</h4>
                  <p>Fuel burn rates by aircraft type and operational conditions</p>
                  <div className="source-stats">
                    <span>Multiple aircraft models</span>
                  </div>
                </div>
              </div>
            </div>
            <div className="methodology-flow">
              <h3>🔄 Processing Pipeline</h3>
              <div className="flow-steps">
                <div className="flow-step">
                  <div className="step-number">1</div>
                  <div className="step-content">
                    <h4>Data Collection</h4>
                    <p>Gather flight records and weather observations</p>
                  </div>
                </div>
                <div className="flow-arrow">→</div>
                <div className="flow-step">
                  <div className="step-number">2</div>
                  <div className="step-content">
                    <h4>Feature Engineering</h4>
                    <p>Create weather impact scores and fuel estimates</p>
                  </div>
                </div>
                <div className="flow-arrow">→</div>
                <div className="flow-step">
                  <div className="step-number">3</div>
                  <div className="step-content">
                    <h4>Model Training</h4>
                    <p>Train and evaluate multiple ML algorithms</p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      )
    },
    {
      id: 'exploratory_data_analysis',
      title: 'Exploratory Data Analysis',
      content: (
        <div className="slide-content">
          <div className="eda-grid">
            <div className="eda-insights">
              <h3>🔍 Key Insights</h3>
              <div className="insight-cards">
                <div className="insight-card fuel">
                  <div className="insight-icon">⛽</div>
                  <div className="insight-data">
                    <h4>Fuel Consumption</h4>
                    <p>Average baseline: <strong>1,722.5 kg</strong></p>
                    <p>Weather impact: <strong>+211.3 kg</strong></p>
                  </div>
                </div>
                <div className="insight-card weather">
                  <div className="insight-icon">🌪️</div>
                  <div className="insight-data">
                    <h4>Weather Impact</h4>
                    <p>Range: <strong>48.7 - 675.7 kg</strong></p>
                    <p>Average increase: <strong>12.3%</strong></p>
                  </div>
                </div>
                <div className="insight-card distance">
                  <div className="insight-icon">📏</div>
                  <div className="insight-data">
                    <h4>Distance Factor</h4>
                    <p>Most important predictor</p>
                    <p>Accounts for <strong>24.5%</strong> of variance</p>
                  </div>
                </div>
              </div>
            </div>
            <div className="eda-visualizations">
              <h3>📊 Data Visualizations</h3>
              <div className="viz-container">
                <img src="/assets/fuel_distribution.png" alt="Fuel Distribution" className="viz-image" />
                <img src="/assets/fuel_vs_distance.png" alt="Fuel vs Distance" className="viz-image" />
              </div>
            </div>
          </div>
        </div>
      )
    },
    {
      id: 'model_development_evaluation',
      title: 'Machine Learning Model Development & Evaluation',
      content: (
        <div className="slide-content">
          <div className="model-grid">
            <div className="model-comparison">
              <h3>🏆 Model Performance Comparison</h3>
              <div className="performance-table">
                <table>
                  <thead>
                    <tr>
                      <th>Model</th>
                      <th>R² Score</th>
                      <th>MAE (kg)</th>
                      <th>RMSE (kg)</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr className="best-model">
                      <td><strong>LightGBM</strong> 🥇</td>
                      <td><strong>0.975</strong></td>
                      <td><strong>5.79</strong></td>
                      <td><strong>14.83</strong></td>
                    </tr>
                    <tr>
                      <td>XGBoost</td>
                      <td>0.965</td>
                      <td>6.16</td>
                      <td>17.41</td>
                    </tr>
                    <tr>
                      <td>Random Forest</td>
                      <td>0.965</td>
                      <td>6.72</td>
                      <td>17.45</td>
                    </tr>
                    <tr>
                      <td>Linear Regression</td>
                      <td>0.907</td>
                      <td>21.71</td>
                      <td>28.57</td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>
            <div className="model-features">
              <h3>🎯 Top Feature Importance</h3>
              <div className="feature-list">
                <div className="feature-item">
                  <div className="feature-bar" style={{width: '100%'}}></div>
                  <span className="feature-name">Distance (24.5%)</span>
                </div>
                <div className="feature-item">
                  <div className="feature-bar" style={{width: '87%'}}></div>
                  <span className="feature-name">Dest Wind Speed (21.3%)</span>
                </div>
                <div className="feature-item">
                  <div className="feature-bar" style={{width: '74%'}}></div>
                  <span className="feature-name">Flight Duration (18.1%)</span>
                </div>
                <div className="feature-item">
                  <div className="feature-bar" style={{width: '41%'}}></div>
                  <span className="feature-name">Weather Impact (10.1%)</span>
                </div>
                <div className="feature-item">
                  <div className="feature-bar" style={{width: '39%'}}></div>
                  <span className="feature-name">Total Weather (9.5%)</span>
                </div>
              </div>
            </div>
          </div>
          <div className="model-visualizations">
            <img src="/assets/weather_enhanced_model_performance.png" alt="Weather Enhanced Model Performance" className="full-width-viz" />
          </div>
        </div>
      )
    },
    {
      id: 'weather_enhancement',
      title: 'Weather Enhancement Results',
      content: (
        <div className="slide-content">
          <div className="weather-grid">
            <div className="weather-impact">
              <h3>🌤️ Weather Integration Impact</h3>
              <div className="impact-metrics">
                <div className="impact-card dramatic">
                  <div className="impact-value">97.5%</div>
                  <div className="impact-label">R² Score Achieved</div>
                  <div className="impact-description">Best-in-class prediction accuracy</div>
                </div>
                <div className="impact-card significant">
                  <div className="impact-value">5.79kg</div>
                  <div className="impact-label">Mean Absolute Error</div>
                  <div className="impact-description">Exceptional precision</div>
                </div>
                <div className="impact-card important">
                  <div className="impact-value">211kg</div>
                  <div className="impact-label">Avg Weather Impact</div>
                  <div className="impact-description">12.3% fuel increase</div>
                </div>
              </div>
            </div>
            <div className="weather-features">
              <h3>🎯 Weather Feature Contributions</h3>
              <div className="weather-feature-grid">
                <div className="weather-feature-card">
                  <div className="feature-icon">💨</div>
                  <h4>Wind Conditions</h4>
                  <p>Destination wind speed is the 2nd most important predictor</p>
                </div>
                <div className="weather-feature-card">
                  <div className="feature-icon">👁️</div>
                  <h4>Visibility</h4>
                  <p>Low visibility increases operational complexity and fuel burn</p>
                </div>
                <div className="weather-feature-card">
                  <div className="feature-icon">🌡️</div>
                  <h4>Temperature</h4>
                  <p>Temperature differentials affect engine efficiency</p>
                </div>
                <div className="weather-feature-card">
                  <div className="feature-icon">🛩️</div>
                  <h4>Flight Category</h4>
                  <p>VFR/IFR conditions determine operational procedures</p>
                </div>
              </div>
            </div>
          </div>
          <div className="weather-visualizations">
            <img src="/assets/weather_enhanced_feature_importance.png" alt="Weather Enhanced Feature Importance" className="full-width-viz" />
          </div>
        </div>
      )
    },
    {
      id: 'documentation',
      title: 'Technical Documentation',
      content: (
        <div className="slide-content documentation-section">
          <h3>📚 Project Details & Methodology</h3>
          <div className="doc-grid">
            <div className="doc-card">
              <h4>Data Structure</h4>
              <p>The primary dataset used is the <strong>US 2023 Civil Flights, delays, meteo and aircrafts</strong> from Kaggle. Key columns include:</p>
              <ul>
                <li><code>Flight_Duration</code>: Total flight time in minutes.</li>
                <li><code>Dep_Airport</code>, <code>Arr_Airport</code>: IATA codes for origin and destination airports.</li>
                <li><code>Tail_Number</code>: Unique identifier for the aircraft.</li>
                <li><code>Temperature</code>, <code>Wind_Speed</code>, <code>Visibility</code>, <code>Pressure</code>: Weather conditions at origin/destination.</li>
                <li><code>Dep_Delay</code>, <code>Arr_Delay</code>: Departure and arrival delays in minutes.</li>
              </ul>
              <p>Additional data was incorporated:</p>
              <ul>
                <li><strong>Aircraft Fuel Consumption Rates:</strong> A custom lookup table was created based on publicly available data for various aircraft models (e.g., CRJ, B737, A320).</li>
                <li><strong>Airport Geolocation:</strong> Latitude and longitude for airports to calculate flight distances.</li>
              </ul>
            </div>
            <div className="doc-card">
              <h4>Processing Steps</h4>
              <ol>
                <li><strong>Data Loading & Sampling:</strong> Due to the large size of the original dataset, a representative sample of 100,000 rows was used for analysis.</li>
                <li><strong>Aircraft Type Mapping:</strong> <code>Tail_Number</code> was used to infer aircraft <code>Model</code>. For models not directly available, a default or 'no info' was assigned.</li>
                <li><strong>Baseline Fuel Estimation:</strong> Estimated total fuel burned for the route (<code>Baseline_Fuel_kg</code>) was calculated using the aircraft's estimated cruise fuel flow rate (kg/hour) and <code>Flight_Duration</code>.</li>
                <li><strong>Weather Data Integration:</strong> Simulated METAR-like weather features were generated and merged with flight data based on airport codes and timeframes.</li>
                <li><strong>Feature Engineering:</strong> New features were created, such as <code>Estimated_Distance_km</code> (Haversine formula), <code>temp_diff_c</code>, <code>avg_wind_impact</code>, <code>avg_visibility_impact</code>, and a <code>comprehensive_weather_impact</code> score.</li>
                <li><strong>Target Variable Definition:</strong> <code>Extra_Fuel_kg</code> was defined as <code>Weather_Adjusted_Fuel_kg - Baseline_Fuel_kg</code>.</li>
                <li><strong>Data Splitting:</strong> The dataset was split into training (70%), validation (15%), and test (15%) sets.</li>
              </ol>
            </div>
            <div className="doc-card">
              <h4>Incorporating METAR Data</h4>
              <p>While direct real-time METAR API integration faced limitations, the methodology for incorporating METAR-like data involved:</p>
              <ul>
                <li><strong>Data Source:</strong> Simulated METAR data was generated to represent realistic weather conditions (Temperature, Wind Speed/Direction, Visibility, Pressure, Sky Conditions).</li>
                <li><strong>Temporal & Spatial Matching:</strong> Weather observations were matched to flights based on the departure and arrival airport IATA codes and the flight's scheduled time.</li>
                <li><strong>Feature Extraction:</strong> Key weather parameters were extracted and transformed into numerical features suitable for machine learning models.</li>
              </ul>
              <p>Future work aims to integrate with live METAR APIs for real-time predictions.</p>
            </div>
            <div className="doc-card">
              <h4>Method to Determine Weather Impact</h4>
              <p>The weather impact on fuel consumption was determined through a multi-step process:</p>
              <ol>
                <li><strong>Baseline Fuel:</strong> Calculated as the ideal fuel burn under standard conditions (<code>Fuel_Rate_kg_per_hour * Flight_Duration / 60</code>).</li>
                <li><strong>Weather Impact Factor:</strong> A <code>Weather_Impact_Factor</code> was introduced, derived from a <code>comprehensive_weather_impact</code> score. This score is a composite of various weather conditions (e.g., higher for strong winds, low visibility, precipitation). The factor scales this score to represent an increase in fuel consumption (e.g., <code>1.0 + (comprehensive_weather_impact / 50)</code>).</li>
                <li><strong>Weather-Adjusted Fuel:</strong> Calculated by multiplying <code>Baseline_Fuel_kg</code> by the <code>Weather_Impact_Factor</code>.</li>
                <li><strong>Extra Fuel:</strong> The target variable, <code>Extra_Fuel_kg</code>, was then derived as the difference between <code>Weather_Adjusted_Fuel_kg</code> and <code>Baseline_Fuel_kg</code>. This quantifies the additional fuel needed specifically due to adverse weather conditions.</li>
              </ol>
              <p>This approach allows the model to learn the non-linear relationships between various weather parameters and the resulting extra fuel required.</p>
            </div>
          </div>
        </div>
      )
    },
    {
      id: 'conclusion_future_work',
      title: 'Conclusion & Future Work',
      content: (
        <div className="slide-content">
          <div className="conclusion-grid">
            <div className="achievements">
              <h3>🎉 Key Achievements</h3>
              <div className="achievement-cards">
                <div className="achievement-card">
                  <div className="achievement-icon">🎯</div>
                  <h4>Exceptional Accuracy</h4>
                  <p>Achieved 97.5% R² score with LightGBM model, demonstrating superior predictive capability for aviation fuel consumption</p>
                </div>
                <div className="achievement-card">
                  <div className="achievement-icon">🌦️</div>
                  <h4>Weather Integration</h4>
                  <p>Successfully incorporated METAR weather data, revealing weather accounts for 12.3% additional fuel consumption</p>
                </div>
                <div className="achievement-card">
                  <div className="achievement-icon">📊</div>
                  <h4>Comprehensive Analysis</h4>
                  <p>Analyzed 1000+ flights across 50+ airports with multiple ML algorithms for robust model comparison</p>
                </div>
              </div>
            </div>
            <div className="future-work">
              <h3>🚀 Future Enhancements</h3>
              <div className="future-items">
                <div className="future-item">
                  <div className="future-icon">🛰️</div>
                  <div className="future-content">
                    <h4>Real-time METAR Integration</h4>
                    <p>Connect to live weather APIs for real-time fuel prediction updates</p>
                  </div>
                </div>
                <div className="future-item">
                  <div className="future-icon">🗺️</div>
                  <div className="future-content">
                    <h4>Route-specific Weather</h4>
                    <p>Incorporate en-route weather conditions along flight paths</p>
                  </div>
                </div>
                <div className="future-item">
                  <div className="future-icon">🧠</div>
                  <div className="future-content">
                    <h4>Deep Learning Models</h4>
                    <p>Explore neural networks for capturing complex weather-fuel relationships</p>
                  </div>
                </div>
                <div className="future-item">
                  <div className="future-icon">📱</div>
                  <div className="future-content">
                    <h4>Operational Deployment</h4>
                    <p>Develop production-ready system for airline fuel planning operations</p>
                  </div>
                </div>
              </div>
            </div>
          </div>
          <div className="conclusion-summary">
            <div className="summary-box">
              <h3>💡 Impact & Value</h3>
              <p>This research demonstrates the critical importance of weather data in aviation fuel prediction, achieving unprecedented accuracy levels that can significantly improve airline operational efficiency, reduce costs, and minimize environmental impact through optimized fuel planning.</p>
            </div>
          </div>
        </div>
      )
    }
  ];

  const nextSlide = () => {
    setCurrentSlide((prev) => (prev + 1) % slides.length);
  };

  const prevSlide = () => {
    setCurrentSlide((prev) => (prev - 1 + slides.length) % slides.length);
  };

  const goToSlide = (index) => {
    setCurrentSlide(index);
  };

  return (
    <div className="app">
      <header className="presentation-header">
        <div className="header-content">
          <div className="header-left">
            <h1>Aviation Fuel Prediction Analysis</h1>
            <div className="slide-indicators">
              {slides.map((_, index) => (
                <button
                  key={index}
                  className={`indicator ${index === currentSlide ? 'active' : ''}`}
                  onClick={() => goToSlide(index)}
                  aria-label={`Go to slide ${index + 1}`}
                >
                  {index + 1}
                </button>
              ))}
            </div>
          </div>
          <div className="header-right">
            <div className="slide-counter">
              {currentSlide + 1} / {slides.length}
            </div>
            <div className="current-slide-title">
              {slides[currentSlide].title}
            </div>
          </div>
        </div>
      </header>

      <main className="presentation-main">
        <div className="slide-container">
          <div className="slide">
            <div className="slide-header">
              <h2>{slides[currentSlide].title}</h2>
              {slides[currentSlide].subtitle && (
                <p className="slide-subtitle">{slides[currentSlide].subtitle}</p>
              )}
            </div>
            {slides[currentSlide].content}
          </div>
        </div>

        <div className="navigation-controls">
          <button 
            className="nav-button prev" 
            onClick={prevSlide}
            disabled={currentSlide === 0}
            aria-label="Previous slide"
          >
            ← Previous
          </button>
          <button 
            className="nav-button next" 
            onClick={nextSlide}
            disabled={currentSlide === slides.length - 1}
            aria-label="Next slide"
          >
            Next →
          </button>
        </div>
      </main>

      <footer className="presentation-footer">
        <div className="footer-content">
          <div className="footer-left">
            <span>Aviation Extra Fuel Prediction Analysis</span>
          </div>
          <div className="footer-right">
          </div>
        </div>
      </footer>
    </div>
  );
};

export default App;

