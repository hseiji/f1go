# F1 Race Prediction 2025 - Machine Learning

Hi there, this a personal project created to predict the GPs winners based on some features we will find out throughout the 2025 season.
I will be using machine learning, FastF1 API data, and historical F1 race results to predict race outcomes.


## 🚀 Model
This repository utilizes **Gradient Boosting Machine Learning model** that predicts race results based on past performance, qualifying times, and other structured F1 data. The model leverages:
- FastF1 API for historical race data
- 2024 race results
- 2025 qualifying session results
- Feature engineering techniques to improve predictions

## 📊 Data Sources
- **FastF1 API**: Fetches lap times, race results, and telemetry data
- **2025 Qualifying Data**: Used for prediction
- **Historical F1 Results**: Processed from FastF1 for training the model

## 🏁 How It Works
1. **Data Collection**: The script pulls relevant F1 data using the FastF1 API.
2. **Preprocessing & Feature Engineering**: Converts lap times, normalizes driver names, and structures race data.
3. **Model Training**: A **Gradient Boosting Regressor** is trained using 2024 race results.
4. **Prediction**: The model predicts race times for 2025 and ranks drivers accordingly.
5. **Evaluation**: Model performance is measured using **Mean Absolute Error (MAE)**.

### Dependencies
- `fastf1`
- `numpy`
- `pandas`
- `scikit-learn`
- `matplotlib`

## 🔧 How to use
Run the prediction script:
```bash
python3 main.py
```
Expected output:
```
🏁 Predicted GP Winner 🏁
Predicted Lap Times and GP Winner:

  Abbreviation  Q3_seconds  Predicted_LapTime (s)
1          NOR      86.269              93.968200
2          ANT      86.271              93.968200
7          LEC      86.754              94.219445
0          VER      86.204              94.605306
```

## 📈 Model Performance
The Mean Absolute Error (MAE) is used to evaluate how well the model predicts race times. 
Lower MAE values indicate more accurate predictions.

## 📌 Future Improvements
- Incorporate other features as Teams and Drivers' current season standings
- Add race and sector pace
- Explore **deep learning** models for improved accuracy
