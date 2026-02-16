import pandas as pd
import numpy as np

def calculate_ird_signal(path_a, path_b, c1, c2):
    # 1. Load the CSV paths into DataFrames
    df1 = pd.read_csv(path_a)
    df2 = pd.read_csv(path_b)
    
    # Standardize column names
    df1.columns = ['date', 'yield_a']
    df2.columns = ['date', 'yield_b']

    # 2. Convert 'date' to actual datetime objects for proper sorting/filling
    df1['date'] = pd.to_datetime(df1['date'])
    df2['date'] = pd.to_datetime(df2['date'])

    # 3. Outer Merge: Keep all dates from both datasets
    # This creates NaNs where one country has data but the other doesn't
    merged = pd.merge(df1, df2, on='date', how='outer').sort_values('date')
    print(merged)
    # 4. FORWARD FILL: Carry the last known yield forward to fill the NaNs
    # This makes the Monthly data "Daily" by assuming the yield stays the same 
    # until the next official update.
    merged[['yield_a', 'yield_b']] = merged[['yield_a', 'yield_b']].ffill()

    # Drop any remaining NaNs at the very beginning of the history
    merged = merged.dropna().sort_values('date', ascending=False)
    
    if len(merged) < 10:
        print(f"⚠️ Warning: Not enough aligned data found for {c1} and {c2}.")
        return

    # 5. Calculate the Spread (Yield A - Yield B) in Basis Points
    merged['spread'] = (merged['yield_a'] - merged['yield_b']) * 100
    
    current_spread = merged['spread'].iloc[0]
    
    # 6. High-Sensitivity 7-Day Z-Score
    # We look at the top 7 rows (the most recent 7 days of the filled data)
    short_window = merged['spread'].head(7)
    mean = short_window.mean()
    std = short_window.std()

    # Prevent division by zero if yields are totally flat
    if std == 0 or np.isnan(std):
        z_score = 0.0
    else:
        z_score = (current_spread - mean) / std
    
    # --- OUTPUT RESULTS ---
    print(f"\n" + "="*45)
    print(f"🌍 {c1} vs {c2} YIELD ANALYSIS")
    print(f"Date: {merged['date'].iloc[0].strftime('%Y-%m-%d')}")
    print(f"-"*45)
    print(f"{c1} Yield: {merged['yield_a'].iloc[0]:.3f}%")
    print(f"{c2} Yield: {merged['yield_b'].iloc[0]:.3f}%")
    print(f"Current Spread: {current_spread:.1f} bps")
    print(f"7-Day Z-Score: {z_score:+.2f}")
    
    # Volatility Check
    if abs(z_score) > 2.0:
        print("\n🚨 SIGNAL: EXTREME DIVERGENCE")
        print(f"The spread is {z_score:.1f} standard deviations from its 1-week mean.")
    elif abs(z_score) > 1.0:
        print("\n⚡ SIGNAL: MOMENTUM BUILDING")
    
    print("="*45)