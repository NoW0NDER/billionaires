from flask import Flask, render_template, request, jsonify
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
    query_type = request.args.get('query_type')

    conn = create_connection()
    cursor = conn.cursor(dictionary=True)

    if query_type == 'total_wealth_by_country':
        sql_query = 'SELECT country, SUM(finalWorth) as total_wealth FROM Billionaire GROUP BY country HAVING total_wealth > %s'
        params = [filter_value]
    elif query_type == 'count_wealthy_over_age':
        sql_query = 'SELECT COUNT(*) as count FROM Billionaire WHERE age > %s'
        params = [filter_value]
    elif query_type == 'count_wealthy_under_age':
        sql_query = 'SELECT COUNT(*) as count FROM Billionaire WHERE age < %s'
        params = [filter_value]
    elif query_type == 'avg_age_by_country':
        sql_query = 'SELECT country, AVG(age) as avg_age FROM Billionaire GROUP BY country'
        params = []
    elif query_type == 'max_wealth_by_country':
        sql_query = 'SELECT country, MAX(finalWorth) as max_wealth FROM Billionaire GROUP BY country'
        params = []
    elif query_type == 'min_wealth_by_country':
        sql_query = 'SELECT country, MIN(finalWorth) as min_wealth FROM Billionaire GROUP BY country'
        params = []
    else:
        sql_query = f'SELECT * FROM {table} WHERE 1=1'
        params = []

        if query:
            sql_query += ' AND personName LIKE %s' if table == 'billionaire' else ' AND industryName LIKE %s' if table == 'industry' else ' AND country LIKE %s'
            params.append('%' + query + '%')

        if filter_column and filter_value:
            sql_query += f' AND {filter_column} {filter_operator} %s'
            params.append(filter_value)

        if sort_column and sort_order in ['ASC', 'DESC']:
            sql_query += f' ORDER BY {sort_column} {sort_order}'
    print(sql_query, params)
    cursor.execute(sql_query, params)
    results = cursor.fetchall()

    # Fetch related data
    if not query_type:
        for result in results:
            if table == 'billionaire':
                person_name = result['personName']
                print(f'SELECT * FROM Industry WHERE industryId IN (SELECT industryId FROM BillionaireIndustry WHERE personName = {person_name})')
                cursor.execute('SELECT * FROM Industry WHERE industryId IN (SELECT industryId FROM BillionaireIndustry WHERE personName = %s)', (person_name,))
                result['industries'] = cursor.fetchall()
                print('SELECT * FROM Country WHERE country = %s'%{result['country']}, )
                cursor.execute('SELECT * FROM Country WHERE country = %s', (result['country'],))
                result['country_info'] = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template('search_results.html', results=results, query=query, table=table, query_type=query_type)

if __name__ == '__main__':
    app.run(debug=True)
