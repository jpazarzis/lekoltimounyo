from flask import Flask
import MySQLdb
import json

select_sql = '''select schools_id, school_name from schools where school_name like '{}%' LIMIT 30'''

select_school_sql = '''select grouping, departement , community , city, neighborhood, grant_suggested_by, school_name,
    director_name, address, telephone, year1_effective, year2_effective, year3_effective,
    year4_effective, year5_effective, year6_effective, unknown_effective, total_effective 
    from schools where schools_id = {}
    '''
    



app = Flask(__name__)


HOSTNAME = 'localhost'
USER = 'root'
PASSWORD = '1111'
DATABASE = 'haiti'
db = MySQLdb.connect(host=HOSTNAME, user=USER, passwd=PASSWORD, db=DATABASE)


@app.route('/school/<school_id>')
def get_school_data(school_id):
    cur = db.cursor()
    sql = select_school_sql.format(school_id)
    cur.execute(sql)
    col_names = [i[0] for i in cur.description]
    school_details = {}
    for row in cur.fetchall():
        for i, cell in enumerate(row):
            school_details[col_names[i]] = cell
    return 'school_data_callback( {0} )'.format(json.dumps(school_details))




@app.route('/matches/<school_name>')
def get_matching_schools(school_name):
    cur = db.cursor()
    sql = select_sql.format(school_name)
    cur.execute(sql)
    schools = []
    for row in cur.fetchall():
        schools.append({'id': row[0], 'name': row[1]})
    return 'mycallback( {0} )'.format(json.dumps(schools))


if __name__ == '__main__':
    app.run(debug=True, port=5002)
