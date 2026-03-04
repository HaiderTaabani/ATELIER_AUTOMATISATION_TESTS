from flask import Flask, render_template, jsonify, redirect, url_for
import storage
from tester.runner import run_tests
import json
import os

app = Flask(__name__)

# Ensure DB is initialized
storage.init_db()

@app.route("/")
def index():
    return redirect(url_for('dashboard'))

@app.route("/consignes")
def consignes():
    return render_template('consignes.html')

@app.route("/run")
def trigger_run():
    # Execute tests
    run_data = run_tests()
    # Save to SQLite
    storage.save_run(run_data)
    return jsonify(run_data)

@app.route("/dashboard")
def dashboard():
    last_run = storage.get_last_run()
    history = storage.list_runs(limit=10)
    
    last_run_data = None
    if last_run:
        # last_run["full_data"] is a JSON string
        last_run_data = json.loads(last_run["full_data"])
        
    return render_template('dashboard.html', 
                           last_run=last_run, 
                           last_run_data=last_run_data,
                           history=history)

@app.route("/health")
def health():
    return jsonify({
        "status": "healthy",
        "service": "api-tester",
        "database": os.path.exists(storage.DB_PATH)
    })

if __name__ == "__main__":
    # For local development
    app.run(host="0.0.0.0", port=5000, debug=True)
