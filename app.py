"""
Flask Web Application for Flipkart Scraper
Complete web interface with search and filter functionality
"""

from flask import Flask, render_template, request, jsonify, send_file
import os
import pandas as pd
import glob
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def index():
    """Home page with search form"""
    return render_template('index.html')

@app.route('/results')
def results():
    """Show all scraped data files"""
    try:
        csv_files = []
        if os.path.exists('data'):
            for filename in os.listdir('data'):
                if filename.endswith('.csv'):
                    filepath = os.path.join('data', filename)
                    file_info = {
                        'filename': filename,
                        'size': os.path.getsize(filepath),
                        'modified': datetime.fromtimestamp(os.path.getmtime(filepath)).strftime('%Y-%m-%d %H:%M'),
                        'rows': 0
                    }
                    
                    # Count rows safely
                    try:
                        df = pd.read_csv(filepath)
                        file_info['rows'] = len(df)
                    except:
                        file_info['rows'] = 'Error'
                    
                    csv_files.append(file_info)
        
        # Sort by modification time (newest first)
        csv_files.sort(key=lambda x: x['modified'], reverse=True)
        
        return render_template('results.html', files=csv_files)
    
    except Exception as e:
        return render_template('error.html', error=str(e))

@app.route('/view/<filename>')
def view_data(filename):
    """View and search data from a specific CSV file"""
    try:
        # Ensure .csv extension
        if not filename.endswith('.csv'):
            filename += '.csv'
        
        filepath = os.path.join('data', filename)
        
        if not os.path.exists(filepath):
            return render_template('error.html', error='File not found')
        
        # Load data
        df = pd.read_csv(filepath)
        
        # Convert to list of dictionaries for template
        products = df.to_dict('records')
        
        # Basic stats
        stats = {
            'total_products': len(df),
            'filename': filename,
            'columns': list(df.columns)
        }
        
        return render_template('view_data.html', products=products, stats=stats)
    
    except Exception as e:
        return render_template('error.html', error=f'Error loading file: {str(e)}')

@app.route('/download/<filename>')
def download_file(filename):
    """Download CSV file"""
    try:
        if not filename.endswith('.csv'):
            filename += '.csv'
        
        filepath = os.path.join('data', filename)
        
        if os.path.exists(filepath):
            return send_file(filepath, as_attachment=True)
        else:
            return render_template('error.html', error='File not found')
    
    except Exception as e:
        return render_template('error.html', error=str(e))

@app.route('/search')
def search():
    """Search products across all files"""
    query = request.args.get('q', '').strip().lower()
    brand = request.args.get('brand', '').strip().lower()
    min_price = request.args.get('min_price', type=float)
    max_price = request.args.get('max_price', type=float)
    min_rating = request.args.get('min_rating', type=float)

    filters = {
        'brand': brand,
        'min_price': min_price,
        'max_price': max_price,
        'min_rating': min_rating
    }
    
    if not query:
        return render_template('search_results.html', filters=filters)
    
    all_products = []
    
    try:
        # Search through all CSV files
        csv_files = glob.glob('data/*.csv')
        
        if not csv_files:
            return render_template('search_results.html',
                                products=[],
                                query=query,
                                total=0,
                                filters=filters,
                                message="No data files found. Please run the scraper first.")

        for csv_file in csv_files:
            try:                        
                df = pd.read_csv(csv_file)
                
                # Add source file info
                df['source_file'] = os.path.basename(csv_file)
                
                # Convert to records for easier processing
                products = df.to_dict('records')
                
                # Filter products
                for product in products:
                    title = str(product.get('title', '')).lower()
                    product_brand = str(product.get('title', '')).split()[0].lower() if product.get('title') else ''
                    
                    # Text search
                    if query not in title:
                        continue
                    
                    # Brand filter
                    if brand and brand not in product_brand:
                        continue
                    
                    # Price filter
                    try:
                        price_str = str(product.get('price', ''))
                        price = float(price_str.replace('₹', '').replace(',', '')) if '₹' in price_str else 0
                        
                        if min_price and price < min_price:
                            continue
                        if max_price and price > max_price:
                            continue
                            
                        product['numeric_price'] = price
                    except:
                        product['numeric_price'] = 0
                    
                    # Rating filter
                    try:
                        rating_str = str(product.get('rating', ''))
                        rating = float(rating_str.split()[0]) if rating_str and rating_str != 'No rating' else 0
                        
                        if min_rating and rating < min_rating:
                            continue
                            
                        product['numeric_rating'] = rating
                    except:
                        product['numeric_rating'] = 0
                    
                    all_products.append(product)
                    
            except Exception as e:
                print(f"Error processing {csv_file}: {e}")
                continue
        
        # Sort by relevance (you can implement more sophisticated scoring)
        all_products.sort(key=lambda x: x.get('numeric_rating', 0), reverse=True)
        
        return render_template('search_results.html', 
                             products=all_products[:50],  # Limit to 50 results
                             query=query, 
                             total=len(all_products),
                             filters=filters)
    
    except Exception as e:
        return render_template('error.html', error=f'Search error: {str(e)}')

@app.route('/api/search')
def api_search():
    """API endpoint for AJAX search"""
    query = request.args.get('q', '').strip().lower()
    
    if len(query) < 2:
        return jsonify({'products': [], 'total': 0})
    
    try:
        results = []
        csv_files = glob.glob('data/*.csv')
        
        for csv_file in csv_files[:3]:  # Limit to 3 most recent files
            try:
                df = pd.read_csv(csv_file)
                products = df.to_dict('records')
                
                for product in products:
                    title = str(product.get('title', '')).lower()
                    if query in title:
                        results.append({
                            'title': product.get('title', '')[:100],
                            'price': product.get('price', ''),
                            'rating': product.get('rating', ''),
                            'source': os.path.basename(csv_file)
                        })
                        
                        if len(results) >= 10:  # Limit results
                            break
                            
                if len(results) >= 10:
                    break
                    
            except:
                continue
        
        return jsonify({'products': results, 'total': len(results)})
        
    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/stats')
def stats():
    """Show statistics across all data"""
    try:
        all_data = []
        csv_files = glob.glob('data/*.csv')
        
        for csv_file in csv_files:
            try:
                df = pd.read_csv(csv_file)
                all_data.append(df)
            except:
                continue
        
        if not all_data:
            return render_template('error.html', error='No data files found')
        
        # Combine all data
        combined_df = pd.concat(all_data, ignore_index=True)
        
        # Calculate statistics
        stats_data = {
            'total_products': len(combined_df),
            'total_files': len(csv_files),
            'latest_scrape': max([datetime.fromtimestamp(os.path.getmtime(f)).strftime('%Y-%m-%d %H:%M') 
                                for f in csv_files]) if csv_files else 'None'
        }
        
        # Brand analysis
        brands = {}
        for title in combined_df.get('title', []):
            if pd.notna(title):
                brand = str(title).split()[0] if str(title) else 'Unknown'
                brands[brand] = brands.get(brand, 0) + 1
        
        # Price analysis
        prices = []
        for price in combined_df.get('price', []):
            try:
                if pd.notna(price) and '₹' in str(price):
                    numeric_price = float(str(price).replace('₹', '').replace(',', ''))
                    prices.append(numeric_price)
            except:
                continue
        
        # Rating analysis
        ratings = []
        for rating in combined_df.get('rating', []):
            try:
                if pd.notna(rating) and rating != 'No rating':
                    numeric_rating = float(str(rating).split()[0])
                    ratings.append(numeric_rating)
            except:
                continue
        
        stats_data.update({
            'top_brands': dict(sorted(brands.items(), key=lambda x: x[1], reverse=True)[:10]),
            'avg_price': sum(prices) / len(prices) if prices else 0,
            'price_range': [min(prices), max(prices)] if prices else [0, 0],
            'avg_rating': sum(ratings) / len(ratings) if ratings else 0,
            'products_with_ratings': len(ratings)
        })
        
        return render_template('stats.html', stats=stats_data)
        
    except Exception as e:
        return render_template('error.html', error=f'Statistics error: {str(e)}')

@app.errorhandler(404)
def not_found(error):
    return render_template('error.html', error='Page not found'), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('error.html', error='Internal server error'), 500

if __name__ == '__main__':
    print("Starting Flask application...")

    # Ensure required directories exist
    os.makedirs('data', exist_ok=True)
    os.makedirs('templates', exist_ok=True)
    
    print("Directories created/verified")
    print("Starting server on http://localhost:5000")
    

    app.run(debug=True, port=5000)
