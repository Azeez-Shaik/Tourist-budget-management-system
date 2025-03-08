# Tourism Budget Management

## Overview
The **Tourism Budget Management** system helps users plan trips by calculating travel costs for **bus and train** routes between two locations. It integrates **Google Maps API** to display directions and fetches transportation costs from a **MySQL database**.

## Features
- **User Input Form**: Enter **From**, **To**, **Total Members**, and **Budget**.
- **Google Maps Integration**: Displays a route between locations.
- **Cost Calculation**: Retrieves **bus and train fares** from the database.
- **Budget Check**: Alerts users if the budget is insufficient.
- **Transport Details**: Provides sorted transport options based on cost.

## Technologies Used
- **Flask** (Python web framework)
- **MySQL** (Database)
- **Google Maps API** (Directions & Map Embed)
- **HTML, CSS** (Frontend UI)

## Installation & Setup
### Prerequisites
- Python 3.x
- MySQL Server
- Virtual Environment (optional but recommended)

### Step 1: Clone the Repository
```sh
git clone https://github.com/your-username/tourism-budget-management.git
cd tourism-budget-management
```

### Step 2: Install Dependencies
```sh
pip install -r requirements.txt
```

### Step 3: Configure Database
- Update `db_config` in `app.py` with your MySQL credentials.
- Run the app once to create the `tourism_db` database and required tables.

### Step 4: Set Up Google Maps API Key
- Replace `GOOGLE_MAPS_API_KEY` in `app.py` with your actual key.
- Alternatively, set it as an environment variable:
  ```sh
  export GOOGLE_MAPS_API_KEY='your-api-key-here'
  ```

### Step 5: Run the Application
```sh
python app.py
```
- Open **http://127.0.0.1:5000/** in your browser.

## Usage
1. Enter **From** and **To** locations.
2. Input **Total Members** and **Budget** (optional).
3. Click **Submit** to view travel costs and directions.
4. Select **Bus** or **Train** for a detailed cost breakdown.

## Database Schema
### `bus_costs`
| id | from_place | to_place | category | cost | timing |
|----|-----------|---------|----------|------|--------|

### `train_costs`
| id | from_place | to_place | category | cost | timing |
|----|-----------|---------|----------|------|--------|

## Contribution
Feel free to submit issues or pull requests to improve this project!

## License
This project is open-source and available under the MIT License.

