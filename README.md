📊 CSV Data Analyzer

A comprehensive Streamlit application for analyzing CSV files with data merging, visualization, and export capabilities.

🎯 Features

Core Functionality
	•	CSV Upload: Upload and process multiple CSV files
	•	Full Data Display: View complete datasets without truncation
	•	Statistical Analysis: Automatic descriptive statistics for numeric columns
	•	Data Cleaning: Remove duplicates and handle missing values
	•	Data Visualization: 4 chart types with image export capabilities
	•	Data Merging: All SQL-style joins (INNER, LEFT, RIGHT, FULL OUTER, CONCAT)
	•	Export Results: Download processed data in CSV format

Data Visualization Options
	1.	Histogram – Distribution analysis for numeric variables
	2.	Line Chart – Trend analysis between variables
	3.	Bar Chart – Categorical data comparison
	4.	Scatter Plot – Relationship analysis between numeric variables

Merge Operations Supported
	•	INNER JOIN – Only matching rows from both tables
	•	LEFT JOIN – All rows from left table + matching from right
	•	RIGHT JOIN – All rows from right table + matching from left
	•	FULL OUTER JOIN – All rows from both tables
	•	CONCATENATE – Simple vertical stacking of tables

⸻

📦 Installation

Prerequisites
	•	Python 3.8+
	•	pip

### Step-by-Step Setup

1. **Clone the repository**
git clone https://github.com/Ualikhan21/analyze_student_db.git
cd csv-data-analyzer


2. **Create virtual environment (recommended)**
```bash
python -m venv venv

# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

## 🚀 Quick Start

1. **Run the application**
```bash
streamlit run app.py
```

2. **Open your browser**
   Navigate to `http://localhost:8501`

3. **Start analyzing**
   - Upload your CSV file
   - Explore data with visualizations
   - Merge with other datasets if needed
   - Export your results

## 📁 Project Structure

```
csv-data-analyzer/
├── app.py                 # Main application file
├── requirements.txt       # Python dependencies
├── README.md             # This file
├── examples/             # Sample CSV files for testing
│   ├── students.csv      # Sample student data
│   └── grades.csv        # Sample grade data
└── screenshots/          # Application screenshots
```

## 🔧 Requirements

The `requirements.txt` file contains:

```
streamlit>=1.28.0
pandas>=2.0.0
numpy>=1.24.0
matplotlib>=3.7.0
seaborn>=0.12.0
```

## 📊 Usage Guide

### Step 1: Data Upload
- Click "Browse files" to upload your main CSV
- Optional: Upload a second CSV for merging operations

### Step 2: Data Exploration
- View complete dataset in interactive table
- Check statistical summary for numeric columns
- Review data cleaning results

### Step 3: Visualization
- Select chart type from dropdown
- Choose columns for X and Y axes
- View generated charts as images

### Step 4: Data Merging (Optional)
- Upload second CSV file
- Select common column for merging
- Choose join type (INNER, LEFT, RIGHT, FULL OUTER)
- View merged results

### Step 5: Export
- Download cleaned data as CSV
- Download merged results as separate files

## 🧪 Testing with Sample Data

The repository includes sample files for testing:

```bash
# Example student data (students.csv)
student_id,name,age,grade,attendance
1,John Doe,20,A,95
2,Jane Smith,21,B,88
3,Bob Johnson,19,A,92
```

```bash
# Example grade data (grades.csv)
student_id,math_score,science_score,english_score
1,85,90,88
2,78,85,80
3,92,88,90
```

## 🛠️ Technical Details

### Data Processing Pipeline
1. **Loading**: Read CSV with proper encoding
2. **Cleaning**: Strip whitespace, remove duplicates, fill missing values
3. **Analysis**: Generate statistics, identify data types
4. **Visualization**: Create charts using Matplotlib/Seaborn
5. **Merging**: Perform SQL-like joins using pandas
6. **Export**: Save results in UTF-8 CSV format

### Key Functions
- `pd.read_csv()`: Load CSV files
- `df.drop_duplicates()`: Remove duplicate rows
- `df.fillna()`: Handle missing values
- `pd.merge()`: Perform table joins
- `plt.subplots()`: Create visualization figures
- `st.dataframe()`: Display interactive tables

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Development Setup
```bash
# Install development dependencies
pip install -r requirements-dev.txt

# Run tests
pytest tests/

# Format code
black app.py
```

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with [Streamlit](https://streamlit.io/)
- Data manipulation with [pandas](https://pandas.pydata.org/)
- Visualization with [Matplotlib](https://matplotlib.org/) and [Seaborn](https://seaborn.pydata.org/)
- Icons from [Twemoji](https://twemoji.twitter.com/)

## 📧 Contact

For questions or feedback:
- GitHub Issues: [Create an issue](https://github.com/Ualikhan21/analyze_student_db.git/issues)

---

⭐ **If you find this project useful, please give it a star!**
```

## Key Sections Included:

1. **Features**: Comprehensive list of all capabilities
2. **Installation**: Step-by-step setup instructions
3. **Quick Start**: Get running in minutes
4. **Usage Guide**: Detailed workflow explanation
5. **Testing**: Sample data for demonstration
6. **Technical Details**: Implementation insights
7. **Contributing**: Guidelines for developers
8. **License**: MIT license information
9. **Contact**: How to get help or provide feedback

The README is professional, comprehensive, and follows GitHub best practices with clear sections, emoji headers, and detailed instructions.