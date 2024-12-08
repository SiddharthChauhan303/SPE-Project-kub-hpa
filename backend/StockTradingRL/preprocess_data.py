import pandas as pd

def calculate_rsi(series, period=14):
    delta = series.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs = gain / loss
    return 100 - (100 / (1 + rs))

def preprocess_data(file_path):
    df = pd.read_csv(file_path)

    # Ensure required columns exist
    required_columns = ['Prev Close', 'open', 'high', 'low', 'Last', 'close', 'VWAP', 'Volume']
    for col in required_columns:
        if col not in df.columns:
            raise KeyError(f"Required column '{col}' not found in the dataset.")

    # Calculate technical indicators
    df['MA20'] = df['close'].rolling(window=20).mean()
    df['MA50'] = df['close'].rolling(window=50).mean()
    df['RSI'] = calculate_rsi(df['close'])
    df['Momentum'] = df['close'] - df['close'].shift(5)

    # Drop NaN values after indicator calculations
    df.dropna(inplace=True)

    # Reset index for proper alignment
    df.reset_index(drop=True, inplace=True)
    df.to_csv('preprocessed_data.csv', index=False)
    print("Data preprocessing complete.")
