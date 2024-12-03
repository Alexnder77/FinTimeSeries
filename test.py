import pandas as pd

try:
    # Read the CSV
    df = pd.read_csv('OMXS30.csv')
    
    # Clean numeric columns with proper error handling
    def convert_volume(vol_str):
        try:
            if isinstance(vol_str, str):
                if 'M' in vol_str:
                    return float(vol_str.replace('M', '')) * 1e6
                elif 'B' in vol_str:
                    return float(vol_str.replace('B', '')) * 1e9
                else:
                    return float(vol_str)
            return vol_str
        except Exception as e:
            print(f"Error converting volume: {vol_str}, {e}")
            return None

    # Clean data
    df['Price'] = df['Price'].str.replace(',', '').astype(float)
    df['Open'] = df['Open'].str.replace(',', '').astype(float)
    df['High'] = df['High'].str.replace(',', '').astype(float)
    df['Low'] = df['Low'].str.replace(',', '').astype(float)
    df['Vol.'] = df['Vol.'].apply(convert_volume)
    df['Change %'] = df['Change %'].str.rstrip('%').astype(float) / 100

    # Convert Date to datetime
    df['Date'] = pd.to_datetime(df['Date'])
    
    # Set index for resampling
    df.set_index('Date', inplace=True)
    
    # Resample to quarterly
    quarterly_data = df['Price'].resample('QE').last()
    
    # Save to Excel
    df.to_excel('OMXS30.xlsx', sheet_name='OMXS30')
    
except Exception as e:
    print(f"Error processing data: {e}")