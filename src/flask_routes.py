from flask import Flask, jsonify
import psycopg2
from fetch_api import get_data, get_list_breweries
from utils import cur_fetchone, cur_fetchall
from insert_data import insert_raw_data


app = Flask(__name__)


@app.route('/')
def index():
    query = 'SELECT version();'
    try:
        databases = cur_fetchone(query)
        return jsonify(databases), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/databases', methods=['GET'])
def show_databases():
    select_query = "SELECT datname FROM pg_database WHERE datistemplate = false;"
    try:
        databases = cur_fetchall(select_query)
        return jsonify(databases), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/tables', methods=['GET'])
def get_tables():
    select_query = """
        SELECT table_schema, table_name
        FROM information_schema.tables
        WHERE table_type = 'BASE TABLE' AND table_schema NOT IN ('pg_catalog', 'information_schema')
        ORDER BY table_schema, table_name;
    """
    try:
        tables = cur_fetchall(select_query)
        return jsonify(tables), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/insert', methods=['GET'])
def insert_data():
    with app.app_context():
        try:
            response_data = get_list_breweries()
            insert_raw_data(response_data)
            return jsonify({'message': 'Successfully inserted data!'}), 201
        except Exception as e:
            return jsonify({'error': str(e)}), 500


@app.route('/rw_list_breweries', methods=['GET'])
def get_raw_data():
    select_query = "SELECT * FROM rw_list_breweries;"
    try:
        data = cur_fetchall(select_query)
        return jsonify(data), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
