#!/usr/bin/env python3
"""
Simple Data Processor for Flipkart scraped data
Creates visualizations and analysis
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import re
from datetime import datetime
import numpy as np

def load_latest_data():
    """Load the most recent CSV file"""
    try:
        # Get all CSV files in data folder
        csv_files = [f for f in os.listdir('data') if f.endswith('.csv')]
        
        if not csv_files:
            print("No CSV files found in data folder")
            return None
        
        # Get the latest file
        latest_file = max(csv_files, key=lambda f: os.path.getmtime(os.path.join('data', f)))
        print(f"Loading data from: {latest_file}")
        
        # Load the data
        df = pd.read_csv(os.path.join('data', latest_file))
        print(f"Loaded {len(df)} products")
        
        return df
        
    except Exception as e:
        print(f"Error loading data: {e}")
        return None

def clean_price(price_str):
    """Extract numeric price from price string"""
    try:
        # Remove currency symbols and commas
        price_clean = re.sub(r'[₹,\s]', '', str(price_str))
        # Extract first number found
        price_match = re.search(r'(\d+)', price_clean)
        if price_match:
            return float(price_match.group(1))
        return 0
    except:
        return 0

def clean_rating(rating_str):
    """Extract numeric rating from rating string"""
    try:
        # Extract decimal number
        rating_match = re.search(r'(\d+\.?\d*)', str(rating_str))
        if rating_match:
            rating = float(rating_match.group(1))
            if 0 <= rating <= 5:
                return rating
        return 0
    except:
        return 0

def extract_brand(title):
    """Extract brand name from product title"""
    try:
        # Common mobile brands
        brands = ['Apple', 'Samsung', 'OnePlus', 'Xiaomi', 'Redmi', 'OPPO', 'Vivo', 
                 'Realme', 'Nothing', 'POCO', 'Motorola', 'Nokia', 'Honor', 'iQOO']
        
        title_upper = str(title).upper()
        for brand in brands:
            if brand.upper() in title_upper:
                return brand
        
        # If no known brand, return first word
        first_word = str(title).split()[0] if title else 'Unknown'
        return first_word.strip('()')
        
    except:
        return 'Unknown'

def clean_data(df):
    """Clean and process the scraped data"""
    if df is None or len(df) == 0:
        return df
    
    print("Cleaning data...")
    
    # Create a copy
    cleaned_df = df.copy()
    
    # Clean price data
    if 'price' in cleaned_df.columns:
        cleaned_df['clean_price'] = cleaned_df['price'].apply(clean_price)
        # Remove rows with invalid prices
        cleaned_df = cleaned_df[cleaned_df['clean_price'] > 0]
    
    # Clean rating data
    if 'rating' in cleaned_df.columns:
        cleaned_df['numeric_rating'] = cleaned_df['rating'].apply(clean_rating)
    
    # Extract brand from title
    if 'title' in cleaned_df.columns:
        cleaned_df['brand'] = cleaned_df['title'].apply(extract_brand)
    
    print(f"Cleaned data: {len(cleaned_df)} valid products")
    return cleaned_df

def create_visualizations(df):
    """Create visualizations of the data"""
    if df is None or len(df) == 0:
        print("No data available for visualization")
        return
    
    print("Creating visualizations...")
    
    # Create output directory
    os.makedirs('static/images', exist_ok=True)
    
    # Set up the plotting area (2x3 grid)
    fig, axes = plt.subplots(2, 3, figsize=(18, 12))
    fig.suptitle('Flipkart Product Analysis Dashboard', fontsize=16, fontweight='bold')
    
    # 1. Price Distribution
    if 'clean_price' in df.columns and df['clean_price'].sum() > 0:
        axes[0, 0].hist(df['clean_price'], bins=15, alpha=0.7, color='skyblue', edgecolor='black')
        axes[0, 0].set_title('Price Distribution')
        axes[0, 0].set_xlabel('Price (₹)')
        axes[0, 0].set_ylabel('Number of Products')
        # Format price labels
        axes[0, 0].xaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'₹{x:,.0f}'))
    
    # 2. Rating Distribution
    if 'numeric_rating' in df.columns and df['numeric_rating'].sum() > 0:
        valid_ratings = df[df['numeric_rating'] > 0]['numeric_rating']
        axes[0, 1].hist(valid_ratings, bins=10, alpha=0.7, color='lightgreen', edgecolor='black')
        axes[0, 1].set_title('Rating Distribution')
        axes[0, 1].set_xlabel('Rating (out of 5)')
        axes[0, 1].set_ylabel('Number of Products')
        axes[0, 1].set_xlim(0, 5)
    
    # 3. Brand Distribution (Top 10)
    if 'brand' in df.columns:
        brand_counts = df['brand'].value_counts().head(10)
        if len(brand_counts) > 0:
            wedges, texts, autotexts = axes[0, 2].pie(brand_counts.values, 
                                                     labels=brand_counts.index, 
                                                     autopct='%1.1f%%',
                                                     startangle=90)
            axes[0, 2].set_title('Top 10 Brands by Product Count')
    
    # 4. Price vs Rating Scatter Plot
    if 'clean_price' in df.columns and 'numeric_rating' in df.columns:
        valid_data = df[(df['clean_price'] > 0) & (df['numeric_rating'] > 0)]
        if len(valid_data) > 0:
            axes[1, 0].scatter(valid_data['numeric_rating'], valid_data['clean_price'], 
                              alpha=0.6, color='coral', s=50)
            axes[1, 0].set_title('Price vs Rating')
            axes[1, 0].set_xlabel('Rating')
            axes[1, 0].set_ylabel('Price (₹)')
            axes[1, 0].yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'₹{x:,.0f}'))
            axes[1, 0].set_xlim(0, 5)
    
    # 5. Average Price by Brand
    if 'brand' in df.columns and 'clean_price' in df.columns:
        brand_avg_price = df.groupby('brand')['clean_price'].mean().sort_values(ascending=True).tail(10)
        if len(brand_avg_price) > 0:
            brand_avg_price.plot(kind='barh', ax=axes[1, 1], color='lightcoral')
            axes[1, 1].set_title('Average Price by Brand (Top 10)')
            axes[1, 1].set_xlabel('Average Price (₹)')
            axes[1, 1].xaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'₹{x:,.0f}'))
    
    # 6. Price Range Analysis
    if 'clean_price' in df.columns:
        price_ranges = ['Under ₹10k', '₹10k-₹20k', '₹20k-₹30k', '₹30k+']
        range_counts = [
            len(df[df['clean_price'] < 10000]),
            len(df[(df['clean_price'] >= 10000) & (df['clean_price'] < 20000)]),
            len(df[(df['clean_price'] >= 20000) & (df['clean_price'] < 30000)]),
            len(df[df['clean_price'] >= 30000])
        ]
        
        axes[1, 2].bar(price_ranges, range_counts, color='gold', alpha=0.7)
        axes[1, 2].set_title('Products by Price Range')
        axes[1, 2].set_xlabel('Price Range')
        axes[1, 2].set_ylabel('Number of Products')
        axes[1, 2].tick_params(axis='x', rotation=45)
    
    plt.tight_layout()
    
    # Save the visualization
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"static/images/flipkart_analysis_{timestamp}.png"
    plt.savefig(filename, dpi=300, bbox_inches='tight')
    print(f"Visualization saved as: {filename}")
    
    plt.show()

def generate_summary_report(df):
    """Generate a summary report"""
    if df is None or len(df) == 0:
        return "No data available for analysis"
    
    report = []
    report.append("=" * 60)
    report.append("FLIPKART PRODUCT ANALYSIS REPORT")
    report.append("=" * 60)
    report.append(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report.append(f"Total products analyzed: {len(df)}")
    report.append("")
    
    # Price analysis
    if 'clean_price' in df.columns:
        valid_prices = df[df['clean_price'] > 0]['clean_price']
        if len(valid_prices) > 0:
            report.append("PRICE ANALYSIS:")
            report.append(f"  Average price: ₹{valid_prices.mean():,.2f}")
            report.append(f"  Median price: ₹{valid_prices.median():,.2f}")
            report.append(f"  Price range: ₹{valid_prices.min():,.2f} - ₹{valid_prices.max():,.2f}")
            report.append("")
    
    # Rating analysis
    if 'numeric_rating' in df.columns:
        valid_ratings = df[df['numeric_rating'] > 0]['numeric_rating']
        if len(valid_ratings) > 0:
            report.append("RATING ANALYSIS:")
            report.append(f"  Average rating: {valid_ratings.mean():.2f}/5.0")
            report.append(f"  Median rating: {valid_ratings.median():.2f}/5.0")
            report.append(f"  Products with 4+ rating: {len(valid_ratings[valid_ratings >= 4])}")
            report.append("")
    
    # Brand analysis
    if 'brand' in df.columns:
        brand_counts = df['brand'].value_counts()
        report.append("BRAND ANALYSIS:")
        report.append(f"  Total unique brands: {len(brand_counts)}")
        report.append("  Top 5 brands:")
        for i, (brand, count) in enumerate(brand_counts.head().items()):
            report.append(f"    {i+1}. {brand}: {count} products")
        report.append("")
    
    report.append("=" * 60)
    return "\n".join(report)

def main():
    """Main function to run data processing"""
    print("Flipkart Data Processor")
    print("=" * 40)
    
    # Load the latest data
    df = load_latest_data()
    
    if df is not None:
        # Clean the data
        cleaned_df = clean_data(df)
        
        if len(cleaned_df) > 0:
            # Generate visualizations
            create_visualizations(cleaned_df)
            
            # Generate summary report
            report = generate_summary_report(cleaned_df)
            print("\n" + report)
            
            # Save report to file
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            report_file = f"data/analysis_report_{timestamp}.txt"
            with open(report_file, 'w') as f:
                f.write(report)
            print(f"\nDetailed report saved as: {report_file}")
        else:
            print("No valid data after cleaning")
    else:
        print("No data found. Please run the scraper first.")

if __name__ == "__main__":
    main()