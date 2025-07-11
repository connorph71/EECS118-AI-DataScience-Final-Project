# ✈️ Flight Database & Analytics Terminal 🧠
This project is a flight database explorer that integrates SQL queries and machine learning–powered visual analytics. Users can query real-world-like flight data and visualize insights such as seat reservations, flight prices over time, and seat utilization across aircraft types.

---

## 📋 Features

### 🔍 Relational Queries:
- Find flights within a given price range and day of week
- View your flight's departure and arrival times
- Search all flights between two airports
- Count flights by airline
- List all airports in a selected U.S. state

### 📊 Non-Relational (Data Analysis + Visualization):
- Pie chart of seat reservations by airline
- Bar chart of seat utilization across airplane types
- Airline seat availability visualization
- Scatter plot of flight prices over time
- Detect overpriced flights using Isolation Forest anomaly detection

---

## 🔌 **Technologies Used & Program Requirements**
- Python 3.6 or higher versions
- MySQL & MySQL Server
- Python packages:
  ```bash
  pip install pymysql pandas matplotlib scikit-learn
  ```

---

## 🛠️ Setup Instructions

### 1. Set Up the MySQL Database

Start your MySQL server, then:

1. **Create and Populate the Database**  
   Import the following files into your MySQL server **in order**:
   ```sql
   source create_table.sql;
   source import_table.sql;
   ```
   These files will:
   - `create_table.sql` creates the `flights` database schema
   - `import_table.sql` populates the schema with sample flight, fare, reservation, and airplane data
   > ⚠️ Make sure both SQL files are in the same working directory as your terminal or selected correctly in your GUI.

### 2. Update Python Connection Parameters

In the script's function `TermP()`, modify the MySQL server credentials if needed:
```python
db = pymysql.connect(
    host='localhost',
    user='YOUR_USERNAME',
    passwd='YOUR_PASSWORD',
    db='flights'
)
```

---

## ▶️ How to Run

```bash
python term_project_script.py
```

You’ll be greeted with a menu in the terminal. Type the number or letter corresponding to your query and follow the prompts. Example inputs and outputs can be found in `term_project_report.pdf`

---

## 💡 Notes

- Flight data is fictional and intended for demo/academic use.
- Anomaly detection is done using `IsolationForest` from `sklearn.ensemble`, identifying price outliers that may represent overpriced flights.
- All user input is handled through the terminal menu.

---

## 🧠 Skills Demonstrated

- SQL JOINs, aggregation, and filtering
- Python MySQL connector usage (`pymysql`)
- Data wrangling using `pandas`
- Data visualization using `matplotlib`
- Anomaly detection using `scikit-learn`
