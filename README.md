# 📚 Streamlit Books Catalog

An interactive Streamlit web application for exploring and analyzing book data. Browse thousands of books with dynamic filtering, visualize market trends, and discover insights through interactive charts and analytics.

**Live Demo:** [Deploy on Streamlit Cloud](#-deploy-on-streamlit-cloud)

## ✨ Features

### 📊 Data Visualization
- **Price Distribution Histogram** - Analyze price ranges across the catalog
- **Rating Breakdown Chart** - See the distribution of book ratings
- **Books Per Category Analysis** - Identify popular categories
- **Average Price by Category** - Compare pricing across categories
- **Price vs Rating Scatter Plot** - Explore the relationship between price and customer ratings
- **Stock Availability Donut Chart** - Track inventory status

### 🔍 Advanced Filtering
- Filter by **category** (multi-select)
- Set **price range** with slider control
- Filter by **minimum rating** (1-5 stars)
- **Stock availability** toggle
- **Keyword search** in titles and descriptions

### 📋 Book Management
- **Sortable book table** with customizable ordering
- **Book detail cards** with comprehensive information
- Real-time **search and filter** functionality
- Display of **5 summary metrics** (books shown, avg price, avg rating, categories, in stock)

### 🎨 User Interface
- Clean, modern design with professional styling
- Responsive layout that works on all devices
- Smooth animations and hover effects
- Light color scheme for comfortable viewing

## 🛠️ Tech Stack

| Component | Technology |
|-----------|-------------|
| **Framework** | [Streamlit](https://streamlit.io/) |
| **Data Processing** | [Pandas](https://pandas.pydata.org/) |
| **Visualization** | [Plotly](https://plotly.com/) |
| **Language** | Python 3.13+ |

## 📦 Installation

### Prerequisites
- Python 3.10 or higher
- Git
- pip package manager

### Step 1: Clone the Repository
```bash
git clone https://github.com/DeepighaJ/streamlit-books-catalog.git
cd streamlit-books-catalog
```

### Step 2: Create Virtual Environment
```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# macOS/Linux
python3 -m venv .venv
source .venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Prepare the Data
```bash
python scrape_all_books.py
```
This will create/update `all_books.csv` with book data from [books.toscrape.com](https://books.toscrape.com/).

### Step 5: Run the Application
```bash
streamlit run src/app.py
```

The app will open in your default browser at: **http://localhost:8501**

## 📁 Project Structure

```
streamlit-books-catalog/
├── src/
│   ├── app.py                    # Main application entry point
│   ├── config.py                 # Configuration & constants
│   ├── styles.py                 # CSS styling
│   ├── data/
│   │   └── loader.py             # Data loading & preprocessing
│   └── components/
│       ├── __init__.py
│       ├── sidebar.py            # Filter sidebar component
│       ├── metrics.py            # Summary metrics component
│       ├── charts.py             # Chart visualization components
│       ├── table.py              # Book table component
│       └── detail.py             # Book detail card component
├── all_books.csv                 # Book dataset (~11,000 books)
├── scrape_all_books.py           # BeautifulSoup data scraper
├── requirements.txt              # Python dependencies
├── .gitignore                    # Git ignore rules
└── README.md                     # This file
```

## 🚀 Deploy on Streamlit Cloud

### Option 1: Automatic Deployment (Recommended)

1. **Push code to GitHub** (already done ✅)
2. Visit [Streamlit Cloud](https://streamlit.io/cloud)
3. Click **"New app"**
4. Connect your GitHub account
5. Select repository: `streamlit-books-catalog`
6. Set main file: `src/app.py`
7. Click **Deploy**

Your app will be live at: `https://<your-username>-streamlit-books-catalog.streamlit.app`

### Option 2: Manual Steps
```bash
# Ensure all changes are pushed to GitHub
git add .
git commit -m "Deploy ready"
git push origin main
```

### Deployment Settings
- **Python version**: 3.10+
- **Main file**: `src/app.py`
- **Requirements file**: `requirements.txt`

## 💡 Usage Guide

### Filtering Books
1. Use the **sidebar** on the left to apply filters
2. Select multiple categories or adjust price/rating ranges
3. Use the search box to find books by title or description
4. Toggle "In stock only" to see available books

### Viewing Analytics
- Hover over charts to see detailed information
- Click on chart elements to interact with them
- The table updates automatically based on filters

### Exploring Book Details
1. Go to the **"Book detail"** section
2. Type in the search box to filter books
3. Select a book from the dropdown
4. View comprehensive book information including:
   - Title, category, and price
   - Rating (in stars)
   - Stock availability and quantity
   - UPC code
   - Direct link to book
   - Full description

## 📊 Data Source

The application uses book data scraped from **[books.toscrape.com](https://books.toscrape.com/)**, a practice website for web scraping enthusiasts.

### Dataset Details
- **Total Books**: ~11,000+
- **Categories**: 50+ book categories
- **Data Points**: Title, price, rating, availability, stock, category, UPC, description, URL
- **Update Frequency**: Run `python scrape_all_books.py` to refresh

### Refresh Data
To update the book catalog with the latest data:
```bash
python scrape_all_books.py
```

## 🔧 Development

### Project Architecture

The project follows a modular, component-based architecture:

- **Separation of Concerns**: Each feature is isolated in its own module
- **Reusability**: Components can be easily reused or extended
- **Maintainability**: Easy to locate and modify specific features
- **Scalability**: Simple to add new components or visualizations

### Adding New Features

1. Create a new file in `src/components/`
2. Import in `src/app.py`
3. Call the render function in the main flow

Example:
```python
# src/components/my_feature.py
def render_my_feature(filtered: pd.DataFrame):
    st.markdown("### My Feature")
    # Your code here
```

## 📈 Performance Tips

- The app caches data loading with `@st.cache_data` decorator
- Charts are optimized with Plotly for smooth interactions
- Filtering is performed in-memory for fast response times

## 🐛 Troubleshooting

### Issue: "all_books.csv not found"
**Solution**: Run `python scrape_all_books.py` to generate the dataset

### Issue: Port 8501 already in use
**Solution**: Run on a different port:
```bash
streamlit run src/app.py --server.port 8502
```

### Issue: Slow performance on large filters
**Solution**: Streamlit cloud instances are lightweight. For better performance, consider Streamlit's [Streamlit Community Cloud Pro](https://streamlit.io/cloud)

## 📝 Requirements

```
pandas>=2.0.3
plotly>=5.18.0
streamlit>=1.36.0
```

For latest versions, see `requirements.txt`

## 🤝 Contributing

Contributions are welcome! Please feel free to:

- 🐛 Report bugs by opening an issue
- 💡 Suggest features or improvements
- 🔧 Submit pull requests for enhancements
- 📝 Improve documentation

### Development Workflow
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the **MIT License** - see the LICENSE file for details.

You are free to:
- Use this project for personal or commercial purposes
- Modify and distribute the code
- Use it as a learning resource

## 🎓 Learning Resources

This project demonstrates:
- **Streamlit**: Building interactive web apps with Python
- **Pandas**: Data manipulation and analysis
- **Plotly**: Creating interactive visualizations
- **Web Scraping**: Using BeautifulSoup for data collection
- **Git/GitHub**: Version control and collaboration
- **Modular Design**: Component-based architecture

## 📞 Support

If you encounter any issues:

1. Check the [Troubleshooting](#-troubleshooting) section
2. Review the [Streamlit Documentation](https://docs.streamlit.io/)
3. Search existing [GitHub Issues](https://github.com/DeepighaJ/streamlit-books-catalog/issues)
4. Create a new issue with detailed description

## 🎯 Roadmap

Potential future enhancements:
- [ ] User reviews and ratings
- [ ] Wishlist/favorites functionality
- [ ] Export filtered results to CSV/PDF
- [ ] Price tracking and alerts
- [ ] Book recommendations engine
- [ ] Multi-language support
- [ ] Dark mode theme toggle

## 🙏 Acknowledgments

- [Streamlit](https://streamlit.io/) for the amazing framework
- [books.toscrape.com](https://books.toscrape.com/) for the practice dataset
- [Plotly](https://plotly.com/) for interactive visualizations
- All contributors and users of this project

---

**Made with ❤️ using Streamlit**

⭐ If you find this project helpful, please consider giving it a star on GitHub!

[🔝 Back to top](#-streamlit-books-catalog)
