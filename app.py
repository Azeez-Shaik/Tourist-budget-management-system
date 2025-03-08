import mysql.connector
from flask import Flask, request, render_template
import requests

app = Flask(__name__)

# Replace with your MySQL configuration
db_config = {
    'user': 'root',
    'password': '20050430',
    'host': 'localhost',
    'database': 'tourism_db'
}

# Replace with your Google Maps API key
GOOGLE_MAPS_API_KEY = 'AIzaSyC3hCbbPBjqUav_TJEjfry1q2-i67CIN2k'

def create_database_and_tables():
    conn = mysql.connector.connect(user=db_config['user'], password=db_config['password'], host=db_config['host'])
    cursor = conn.cursor()

    cursor.execute("CREATE DATABASE IF NOT EXISTS tourism_db")
    cursor.execute("USE tourism_db")

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS bus_costs (
        id INT AUTO_INCREMENT PRIMARY KEY,
        from_place VARCHAR(255),
        to_place VARCHAR(255),
        category VARCHAR(255),
        cost DECIMAL(10, 2),
        timing VARCHAR(50)
    )
    """)
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS train_costs (
        id INT AUTO_INCREMENT PRIMARY KEY,
        from_place VARCHAR(255),
        to_place VARCHAR(255),
        category VARCHAR(255),
        cost DECIMAL(10, 2),
        timing VARCHAR(50)
    )
    """)
    cursor.close()
    conn.close()

def get_directions(from_place, to_place):
    url = f'https://maps.googleapis.com/maps/api/directions/json?origin={from_place}&destination={to_place}&key={GOOGLE_MAPS_API_KEY}'
    response = requests.get(url)
    directions = response.json()
    if directions['status'] == 'OK':
        distance = directions['routes'][0]['legs'][0]['distance']['text']
        return distance
    return None

def get_costs(transport_type, from_place, to_place, sort_by_budget=None, budget=None):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    query = f"SELECT category, cost, timing FROM {transport_type}_costs WHERE from_place = %s AND to_place = %s"
    if sort_by_budget and budget:
        query += " ORDER BY cost ASC"
    else:
        query += " ORDER BY timing ASC"

    cursor.execute(query, (from_place, to_place))
    results = cursor.fetchall()
    conn.close()
    return results

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    from_place = request.form['from'].strip()
    to_place = request.form['to'].strip()
    total_members = request.form.get('total_members', None)
    budget = request.form.get('budget', None)

    if not from_place or not to_place:
        return "Invalid 'from' or 'to' location. Please provide valid place names."

    distance = get_directions(from_place, to_place)

    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    cursor.execute("SELECT cost FROM bus_costs WHERE from_place = %s AND to_place = %s ORDER BY cost ASC LIMIT 1", (from_place, to_place))
    bus_cost_per_person = cursor.fetchone()[0]

    cursor.execute("SELECT cost FROM train_costs WHERE from_place = %s AND to_place = %s ORDER BY cost ASC LIMIT 1", (from_place, to_place))
    train_cost_per_person = cursor.fetchone()[0]

    bus_total_cost = bus_cost_per_person * int(total_members) if total_members else None
    train_total_cost = train_cost_per_person * int(total_members) if total_members else None

    conn.close()

    if total_members and budget:
        if float(budget) < min(bus_total_cost, train_total_cost):
            budget_message = "You will need additional funds to proceed with this tour."
            costs = None
        else:
            budget_message = None
            costs = None
    else:
        budget_message = None
        costs = None

    return render_template('index.html', from_place=from_place, to_place=to_place, directions=distance, kilometers=distance,
                           bus_cost_per_person=bus_cost_per_person, train_cost_per_person=train_cost_per_person, 
                           bus_total_cost=bus_total_cost, train_total_cost=train_total_cost, budget_message=budget_message)

@app.route('/bus')
def bus():
    from_place = request.args.get('from')
    to_place = request.args.get('to')
    budget = request.args.get('budget', None)
    costs = get_costs('bus', from_place, to_place, sort_by_budget=True if budget else False, budget=budget)
    return render_template('index.html', costs=costs, transport_type='bus')

@app.route('/train')
def train():
    from_place = request.args.get('from')
    to_place = request.args.get('to')
    budget = request.args.get('budget', None)
    costs = get_costs('train', from_place, to_place, sort_by_budget=True if budget else False, budget=budget)
    return render_template('index.html', costs=costs, transport_type='train')

if __name__ == '__main__':
    create_database_and_tables()
    app.run(debug=True)
