import pandas as pd
import glob
import os

def combine_all_csv_files():
    """Combine all CSV files into one master file"""
    
    # Find all CSV files in data folder
    csv_files = glob.glob('data/*.csv')
    
    if not csv_files:
        print("No CSV files found in data folder")
        return
    
    print(f"Found {len(csv_files)} CSV files to combine:")
    
    all_dataframes = []
    
    for csv_file in csv_files:
        try:
            df = pd.read_csv(csv_file)
            # Add source file column
            df['source_file'] = os.path.basename(csv_file)
            all_dataframes.append(df)
            print(f"  - {os.path.basename(csv_file)}: {len(df)} products")
        except Exception as e:
            print(f"  - Error reading {csv_file}: {e}")
    
    if all_dataframes:
        # Combine all dataframes
        combined_df = pd.concat(all_dataframes, ignore_index=True)
        
        # Remove duplicates based on title
        combined_df = combined_df.drop_duplicates(subset=['title'], keep='first')
        
        # Save combined file
        output_file = 'data/combined_all_products.csv'
        combined_df.to_csv(output_file, index=False)
        
        print(f"\nCombined file created: {output_file}")
        print(f"Total unique products: {len(combined_df)}")
        print(f"Columns: {list(combined_df.columns)}")
        
        return output_file
    
    return None

if __name__ == "_main_":
    combine_all_csv_files()