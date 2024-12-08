import pandas as pd
from stable_baselines3 import PPO
from stock_trading_env import StockTradingEnv
from preprocess_data import preprocess_data

def train_and_backtest(file_path):
    preprocess_data(file_path)
    df = pd.read_csv('preprocessed_data.csv')
    env = StockTradingEnv(df)

    # Train the RL agent
    model = PPO("MlpPolicy", env, verbose=1)
    model.learn(total_timesteps=10000)

    # Backtesting
    env = StockTradingEnv(df)
    obs = env.reset()
    results = []

    while True:
        action, _states = model.predict(obs)
        obs, reward, done, info = env.step(action)
        current_price = df.loc[env.current_step - 1, 'close']
        results.append([
            env.cash, 
            env.stock_held, 
            reward, 
            env.cash + env.stock_held * current_price
        ])
        if done:
            break

    # Save results
    result_df = pd.DataFrame(results, columns=['Cash', 'Stock Held', 'Reward', 'Net Worth'])
    output_df = pd.concat([df.reset_index(drop=True), result_df], axis=1)
    output_df.to_csv('output_with_trading_results.csv', index=False)
    print("Training and backtesting complete.")
