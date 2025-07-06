from flask import Flask, render_template, request, jsonify
from scraper import find_professors
import json
import schedule
import threading
import time

app = Flask(__name__)

# ---------- Data Loading ---------- #
def load_professors():
    with open('data.json', 'r') as f:
        return json.load(f)

# Initially load once into cache
cached_data = load_professors()

# ---------- Scheduled Auto-Update ---------- #
def save_to_file(data, filename='data.json'):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2)

def update_professor_data():
    print("[AutoUpdate] Scraping and refreshing data.json...")
    try:
        data = find_professors()
        save_to_file(data)
        global cached_data
        cached_data = data
        print(f"[AutoUpdate] {len(data)} professors updated.")
    except Exception as e:
        print(f"[AutoUpdate] Failed: {e}")

def run_scheduler():
    schedule.every(12).hours.do(update_professor_data)  # adjust frequency as needed
    while True:
        schedule.run_pending()
        time.sleep(60)

# Start the scheduler in a background thread
scheduler_thread = threading.Thread(target=run_scheduler)
scheduler_thread.daemon = True
scheduler_thread.start()

# ---------- Flask Routes ---------- #
@app.route('/')
def index():
    return render_template('index.html', professors=cached_data)

@app.route('/search')
def search():
    name_query = request.args.get('name', '').lower()
    dept_query = request.args.get('department', '').lower()
    min_rating = float(request.args.get('min_rating', 0))

    filtered = []
    for prof in cached_data:
        try:
            if (name_query in prof['name'].lower() and
                dept_query in prof['department'].lower() and
                float(prof['rating']) >= min_rating):
                filtered.append(prof)
        except Exception:
            continue

    return jsonify(filtered)

# Optional: Manual Trigger Endpoint
@app.route('/update', methods=['POST'])
def manual_update():
    update_professor_data()
    return jsonify({"status": "manual update triggered"})

if __name__ == '__main__':
    app.run(debug=True)
