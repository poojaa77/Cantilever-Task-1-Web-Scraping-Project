# Flipkart Web Scraper - Internship Project

A web scraping application that extracts product data from Flipkart and provides an interactive Flask web interface for searching, filtering, and analyzing scraped data.

## 🚀 Project Overview

This project demonstrates end-to-end web scraping implementation including data extraction, storage, visualization, and user interface development. Built as part of an internship program to showcase skills in Python web development, data analysis, and user interface design.

### Key Achievements
- **Interactive web interface** with real-time search and filtering
- **Data visualization dashboard** with charts and statistics  
- **Professional UI design** using Bootstrap 5
- **Complete project documentation** with setup guides

## 📋 Features

### Web Scraping
- Extracts product titles, prices, ratings, and images from Flipkart
- Handles pagination for multi-page scraping
- Implements anti-bot detection handling
- Robust error handling and logging
- Respects website rate limits with built-in delays

### Data Management
- Saves data in CSV format (Excel compatible)
- Timestamped file organization
- Data cleaning and validation
- Support for multiple product categories

### Web Interface
- **Home Page**: Search form with filter options
- **Data Viewer**: Interactive table with real-time filtering
- **Search Results**: Display filtered products with metadata
- **Statistics Dashboard**: Charts showing price trends and brand analysis
- **File Management**: View and download all scraped data files

### Search & Filter Capabilities
- **Text Search**: Search across product titles
- **Brand Filtering**: Auto-populated dropdown from scraped data
- **Price Range Filtering**: Predefined ranges (Under ₹10k, ₹10k-20k, etc.)
- **Rating Filtering**: Filter by minimum star ratings (4+, 3+)
- **Real-time Results**: Instant filtering with JavaScript
- **Sorting Options**: Sort by price or rating

### Data Visualization
- Price distribution histograms
- Rating distribution charts
- Brand analysis pie charts
- Price vs Rating scatter plots
- Average price by brand comparisons
- Statistical summary reports

## 🛠 Technology Stack

### Backend
- **Python 3.7+**: Core programming language
- **Flask**: Web framework for user interface
- **Selenium WebDriver**: Web scraping automation
- **Pandas**: Data processing and manipulation
- **Matplotlib & Seaborn**: Data visualization

### Frontend
- **HTML5/CSS3**: Structure and styling
- **Bootstrap 5**: Responsive UI framework
- **JavaScript**: Interactive filtering and search
- **Font Awesome**: Icons and visual elements

### Data Storage
- **CSV Files**: Structured data storage
- **File-based system**: No database server required

### Development Tools
- **Chrome WebDriver**: Browser automation
- **webdriver-manager**: Automatic driver management
- **VS Code**: Primary development environment

## 📁 Project Structure

```
Cantilever-Task-1-Web-Scraping-Project/
├── scraper.py              # Core scraping logic
├── app.py                  # Flask web application
├── data_processor.py       # Data analysis and visualization
├── more_smartphones.py     # Extended scraping script
├── requirements.txt        # Python dependencies
├── README.md              # Project documentation
├── .gitignore             # Git ignore rules
│
├── templates/             # HTML templates
│   ├── base.html          # Base template with navigation
│   ├── index.html         # Home page with search form
│   ├── view_data.html     # Interactive data viewer
│   ├── search_results.html # Search results display
│   ├── stats.html         # Statistics dashboard
│   └── error.html         # Error handling page
│
└── data/                  # Scraped data files
    ├── flipkart_smartphone_*.csv
    └── sample_data.csv
```

## 🚦 Installation & Setup

### Prerequisites
- Python 3.7 or higher
- Google Chrome browser
- Stable internet connection

### Installation Steps

1. **Clone the repository**
   ```bash
   git clone https://github.com/poojaa77/Cantilever-Task-1-Web-Scraping-Project.git
   cd Cantilever-Task-1-Web-Scraping-Project
   ```

2. **Install required packages**
   ```bash
   pip install -r requirements.txt
   ```

3. **Verify installation**
   ```bash
   python -c "import selenium, flask, pandas; print('All packages installed successfully!')"
   ```

## 🎯 Usage Instructions

### Running the Web Scraper

**Basic scraping (1-2 pages):**
```bash
python scraper.py
```

**Extended scraping for more products:**
```bash
python more_smartphones.py
```

### Starting the Web Interface

1. **Launch the Flask application:**
   ```bash
   python app.py
   ```

2. **Open your browser and navigate to:**
   ```
   http://localhost:5000
   ```

3. **Available pages:**
   - `/` - Home page with search functionality
   - `/results` - View all scraped data files
   - `/view/<filename>` - Interactive data viewer with filters
   - `/search` - Advanced search across all data
   - `/stats` - Statistics and analytics dashboard

### Generating Data Visualizations

```bash
python data_processor.py
```

This creates comprehensive charts and analysis reports saved in the `static/images/` directory.

## 📊 Sample Data

The scraper extracts the following information for each product:

| Field | Description | Example |
|-------|-------------|---------|
| title | Complete product name | "Samsung Galaxy M34 5G (Midnight Blue, 128 GB)" |
| price | Current selling price | "₹18,999" |
| rating | Customer rating | "4.2" |
| image_url | Product image link | "https://rukminim2.flixcart.com/..." |
| scraped_at | Timestamp | "2024-01-20 14:30:22" |

### Data Quality Metrics
- **Success Rate**: 95%+ successful data extraction
- **Data Completeness**: All required fields captured
- **File Size**: ~50-100KB per 100 products
- **Processing Speed**: ~24 products per page, 2-3 minutes per page

## 🔍 Web Interface Features

### Interactive Search
- **Real-time filtering** as you type
- **Multiple filter combinations** (text + brand + price + rating)
- **Instant result counting** showing filtered vs total products
- **Clear filters** button to reset all selections

### Data Visualization Dashboard
- **Price Distribution**: Histogram showing price ranges
- **Brand Analysis**: Pie chart of brand representation
- **Rating Trends**: Distribution of customer ratings
- **Price vs Rating**: Correlation analysis
- **Summary Statistics**: Average prices, ratings, and counts

### Responsive Design
- **Mobile-friendly** interface using Bootstrap 5
- **Modern UI** with gradient backgrounds and smooth animations
- **Professional styling** with consistent color scheme
- **Intuitive navigation** with clear page structure

## ⚙️ Configuration Options

### Scraper Settings
```python
# In scraper.py
scraper = FlipkartScraper(
    headless=True,          # Run browser in background
    storage_type="csv"      # Data storage format
)

# Scraping parameters
search_term = "smartphone"  # Product category
max_pages = 5              # Number of pages to scrape
```

### Web Application Settings
```python
# In app.py
app.run(
    debug=True,            # Development mode
    host='0.0.0.0',       # Accept connections from any IP
    port=5000             # Port number
)
```

## 🔧 Troubleshooting

### Common Issues and Solutions

**ChromeDriver not found:**
- The project uses `webdriver-manager` for automatic ChromeDriver installation
- Ensure Google Chrome is installed and up to date

**No products scraped:**
- Check internet connection
- Try different search terms
- Run with `headless=False` to observe browser behavior

**Flask app not starting:**
- Verify port 5000 is not in use: `netstat -an | grep 5000`
- Check if all dependencies are installed: `pip install -r requirements.txt`

**Import errors:**
- Create virtual environment: `python -m venv venv`
- Activate it: `source venv/bin/activate` (Linux/Mac) or `venv\Scripts\activate` (Windows)
- Reinstall packages: `pip install -r requirements.txt`

## 📈 Performance Metrics

### Scraping Performance
- **Speed**: ~24 products per page
- **Time**: 2-3 minutes per page including delays
- **Success Rate**: 95%+ data extraction accuracy
- **Memory Usage**: ~50MB during operation

### Web Application Performance
- **Search Speed**: <100ms for datasets under 1000 products
- **Filter Response**: Real-time with JavaScript
- **Page Load**: <2 seconds for all pages
- **File Handling**: Supports CSV files up to 10MB

## 🎓 Learning Outcomes

This project demonstrates proficiency in:

### Technical Skills
- **Web Scraping**: Selenium automation, anti-bot handling
- **Web Development**: Flask framework, REST principles
- **Data Processing**: Pandas manipulation, cleaning, validation
- **Frontend Development**: HTML/CSS/JavaScript, responsive design
- **Data Visualization**: Matplotlib/Seaborn chart creation

### Professional Skills
- **Project Organization**: Clean code structure, documentation
- **Version Control**: Git repository management
- **Problem Solving**: Error handling, debugging
- **User Experience**: Intuitive interface design
- **Documentation**: Comprehensive README, code comments

## 🔮 Future Enhancements

### Immediate Improvements
- Database integration (SQLite/PostgreSQL)
- User authentication and sessions
- Data export options (PDF, Excel)
- API endpoints for programmatic access

### Advanced Features
- Machine learning price predictions
- Automated scheduling for regular scraping
- Email notifications for price changes
- Advanced analytics with trending analysis

### Deployment Options
- Docker containerization
- Cloud deployment (Heroku, AWS, GCP)
- CI/CD pipeline setup
- Production monitoring and logging

## ⚖️ Legal and Ethical Considerations

- **Robots.txt Compliance**: Respects website scraping guidelines
- **Rate Limiting**: Implements delays to avoid server overload
- **Educational Purpose**: Project intended for learning and portfolio demonstration
- **Data Privacy**: No personal information collected or stored
- **Terms of Service**: Users should review Flipkart's terms before scraping



This project successfully demonstrates end-to-end web scraping implementation with a professional user interface, meeting all internship requirements and showcasing practical software development skills.
