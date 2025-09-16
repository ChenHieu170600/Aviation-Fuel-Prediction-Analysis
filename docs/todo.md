# To-Do List

## Phase 1: Clarify requirements and gather information
- [x] Ask clarifying questions to understand the user's needs.

## Phase 2: Find and evaluate suitable public datasets
- [x] Search for public datasets containing flight data (origin, destination, fuel consumption) and comprehensive weather data (temperature, wind speed/direction, visibility, precipitation, humidity, pressure, turbulence, sky conditions).
- [x] Prioritize datasets that offer historical weather forecasts or can be linked with historical weather forecast data.
- [x] Evaluate datasets based on relevance, quality, size, and accessibility.
- [x] Select the most suitable dataset(s) for the project.
- [ ] Acknowledge the difficulty in finding a public dataset with actual per-flight fuel consumption and detailed weather data.

## Phase 3: Download and prepare the dataset
- [x] Download the selected dataset(s).
- [x] Clean and preprocess the data (handle missing values, outliers, data type conversions).
- [x] Feature engineering: Estimate fuel consumption using `tail_number`, aircraft model, and `openap` library. (Attempted, but OpenAP does not support CRJ aircraft types prevalent in the dataset.)
- [x] Feature engineering: Estimate fuel consumption using alternative methods for all aircraft types. (Attempted, but full dataset processing is resource-intensive and leads to 'Killed' errors.)
- [x] Process a representative sample of the dataset for fuel estimation and model building due to resource constraints.
- [x] Integrate estimated fuel consumption data into the main dataset.
- [x] Feature engineering: Estimate fuel consumption using `tail_number`, aircraft model, and `openap` library. (Attempted, but OpenAP does not support CRJ aircraft types prevalent in the dataset.)
- [x] Split the dataset into training, validation, and test sets.

## Phase 4: Exploratory data analysis
- [x] Perform descriptive statistics on the dataset.
- [x] Visualize key relationships between features and the target variable (extra fuel).
- [x] Identify potential correlations and patterns.

## Phase 5: Develop and train machine learning models
- [x] Implement baseline models using scikit-learn (e.g., Linear Regression, Random Forest).
- [x] Implement advanced models (e.g., XGBoost, LightGBM).
- [x] Train all models on the prepared training data.
- [x] Tune hyperparameters for optimal performance.

## Phase 6: Evaluate model performance and analyze results
- [x] Evaluate each model's performance using appropriate metrics (e.g., RMSE, MAE, R-squared).
- [x] Compare the performance of different models.
- [x] Analyze model strengths and weaknesses.
- [x] (Optional) Explore model interpretability if feasible.

## Phase 7: Create comprehensive report and deliver results
- [ ] Generate visualizations of model performance and key insights.
- [ ] Prepare a comprehensive report detailing the analysis, methodology, model development, and results.
- [ ] Create a web slide presentation summarizing the project.
- [ ] Deliver the dataset, code, visualizations, report, and presentation to the user.


