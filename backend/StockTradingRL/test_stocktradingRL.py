import pytest
import pandas as pd
import numpy as np
from stock_trading_env import StockTradingEnv
from preprocess_data import preprocess_data
from stable_baselines3 import PPO

@pytest.fixture
def sample_data():
    """Fixture to create a small sample dataset for testing."""
    data = {
        'Date': ['2023-01-01', '2023-01-02', '2023-01-03', '2023-01-04', '2023-01-05'],
        'Prev Close': [100, 102, 101, 103, 105],
        'open': [101, 102, 102, 104, 106],
        'high': [102, 104, 103, 106, 108],
        'low': [99, 101, 100, 102, 104],
        'Last': [101, 103, 102, 105, 107],
        'close': [102, 103, 101, 104, 106],
        'VWAP': [100.5, 102.3, 101.2, 103.4, 105.6],
        'Volume': [1000, 1200, 1100, 1300, 1500]
    }
    return pd.DataFrame(data)


def test_preprocess_data(sample_data, tmp_path):
    """Test if data preprocessing generates correct indicators."""
    file_path = tmp_path / "sample_data.csv"
    sample_data.to_csv(file_path, index=False)

    preprocess_data(file_path)

    processed_data = pd.read_csv('preprocessed_data.csv')
    assert 'MA20' in processed_data.columns, "'MA20' column missing after preprocessing."
    assert 'MA50' in processed_data.columns, "'MA50' column missing after preprocessing."
    assert 'RSI' in processed_data.columns, "'RSI' column missing after preprocessing."
    assert 'Momentum' in processed_data.columns, "'Momentum' column missing after preprocessing."
    assert not processed_data.isnull().values.any(), "Preprocessed data contains NaN values."


def test_environment_initialization(sample_data):
    """Test if the StockTradingEnv initializes correctly."""
    env = StockTradingEnv(sample_data)
    obs = env.reset()

    assert obs.shape[0] == sample_data.shape[1] - 3 + 4, "Observation shape mismatch."
    assert env.cash == 100000, "Initial cash is not set correctly."
    assert env.stock_held == 0, "Initial stock held is not set correctly."


def test_environment_step(sample_data):
    """Test if the environment step function updates state correctly."""
    env = StockTradingEnv(sample_data)
    obs = env.reset()

    initial_cash = env.cash
    action = [0.5]  # Allocate 50% of the net worth to stock
    obs, reward, done, info = env.step(action)

    assert env.cash <= initial_cash, "Cash did not reduce after a buy action."
    assert env.stock_held >= 0, "Stock held is invalid after a buy action."
    assert 'net_worth' in info, "'net_worth' key missing in the info dictionary."


def test_rl_model_training(sample_data):
    """Test if the PPO model can be trained without errors."""
    env = StockTradingEnv(sample_data)
    model = PPO("MlpPolicy", env, verbose=0)

    try:
        model.learn(total_timesteps=100)
    except Exception as e:
        pytest.fail(f"Model training failed with error: {e}")


def test_rl_model_action(sample_data):
    """Test if the trained model can generate valid actions."""
    env = StockTradingEnv(sample_data)
    model = PPO("MlpPolicy", env, verbose=0)
    model.learn(total_timesteps=100)

    obs = env.reset()
    action, _states = model.predict(obs)

    assert len(action) == 1, "Action dimension mismatch."
    assert 0 <= action[0] <= 1, "Action is out of the allowed range [0, 1]."
