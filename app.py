from flask import Flask, render_template, request
import mysql.connector
from config import MyCONFIG

app = Flask(__name__)

config = MyCONFIG()
db_config = {
    'host': config.get_host(),
    'user': config.get_username(),
    'password': config.get_pwd(),
    'database': 'BILLIONAIRES'
}

def create_connection():
    return mysql.connector.connect(**db_config)

@app.route('/')
def index():
    conn = create_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT * FROM Billionaire LIMIT 10')
    billionaires = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('index.html', billionaires=billionaires)

@app.route('/search', methods=['GET', 'POST'])
def search():
    query = request.args.get('query')
    table = request.args.get('table')
    filter_column = request.args.get('filter_column')
    filter_value = request.args.get('filter_value')
    filter_operator = request.args.get('filter_operator', '=')
    sort_column = request.args.get('sort_column')
    sort_order = request.args.get('sort_order')

    conn = create_connection()
    cursor = conn.cursor(dictionary=True)
    
    sql_query = f'SELECT * FROM {table} WHERE 1=1'
    params = []

    if query:
        if table == 'billionaire':
            sql_query += ' AND personName LIKE %s'
        elif table == 'industry':
            sql_query += ' AND industryName LIKE %s'
        else:
            sql_query += ' AND country LIKE %s'
        params.append('%' + query + '%')

    if filter_column and filter_value:
        sql_query += f' AND {filter_column} {filter_operator} %s'
        params.append(filter_value)

    if sort_column and sort_order:
        sql_query += f' ORDER BY {sort_column} {sort_order}'

    cursor.execute(sql_query, params)
    results = cursor.fetchall()
    
    # Fetch related data
    for result in results:
        if table == 'billionaire':
            person_name = result['personName']
            cursor.execute('SELECT * FROM Industry WHERE industryId IN (SELECT industryId FROM BillionaireIndustry WHERE personName = %s)', (person_name,))
            result['industries'] = cursor.fetchall()
            cursor.execute('SELECT * FROM Country WHERE country = %s', (result['country'],))
            result['country_info'] = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template('search_results.html', results=results, query=query, table=table)

if __name__ == '__main__':
    app.run(debug=True)
