from flask import Flask
from flask import g
from flask import request
import MySQLdb
import json
import ConfigParser
import logging
from flask import jsonify

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
fh = logging.FileHandler('sample_server.log')
fh.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.ERROR)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
ch.setFormatter(formatter)
logger.addHandler(fh)
logger.addHandler(ch)

select_sql = '''select school_id, school_name, grouping, departement , community, 
city, address, telephone, neighborhood, grant_suggested_by, director_name, 
year1_effective, year2_effective, year3_effective, year4_effective, year5_effective, 
year6_effective, unknown_effective, total_effective,
has_electricity , has_internet , has_restroom , classrooms_count , floors_count 
from schools where school_name like '{}%' '''

select_school_sql = '''select grouping, departement , community , city, neighborhood, grant_suggested_by, school_name,
    director_name, address, telephone, year1_effective, year2_effective, year3_effective,
    year4_effective, year5_effective, year6_effective, unknown_effective, total_effective,
    has_electricity , has_internet , has_restroom , classrooms_count , floors_count 
    from schools where school_id = {}
    '''

config = ConfigParser.RawConfigParser()
config.read('config.ini')

app = Flask(__name__)

HOSTNAME = config.get('dbsettings', 'HOSTNAME') 
USER = config.get('dbsettings', 'USER') 
PASSWORD = config.get('dbsettings', 'PASSWORD') 
DATABASE = config.get('dbsettings', 'DATABASE') 


@app.before_request
def db_connect():
    g.db_conn = MySQLdb.connect(host=HOSTNAME, user=USER, passwd=PASSWORD, db=DATABASE)

@app.teardown_request
def db_disconnect(exception=None):
    g.db_conn.close()


@app.route('/departments')
def get_departments():
    cur = g.db_conn.cursor()
    sql = "select distinct(departement) from schools where  departement != '' order by 1"
    logger.info("executing: {0}".format(sql))
    cur.execute(sql)
    departments = []
    for row in cur.fetchall():
        departments.append({'name': row[0]})

    return 'departments_data_callback( {0} )'.format(json.dumps(departments, ensure_ascii=False))


@app.route('/school/<school_id>')
def get_school_data(school_id):
    cur = g.db_conn.cursor()
    sql = select_school_sql.format(school_id)
    logger.info("executing: {0}".format(sql))
    cur.execute(sql)
    col_names = [i[0] for i in cur.description]
    school_details = {}
    for row in cur.fetchall():
        for i, cell in enumerate(row):
            school_details[col_names[i]] = cell
            
    logger.info("scholl data: {0}".format(json.dumps(school_details)))
    return 'school_data_callback( {0} )'.format(json.dumps(school_details))





#@app.route('/matches/<school_name>')

@app.route('/matches')
def get_matching_schools():
    cur = g.db_conn.cursor()
    school_name = request.args.get('school_name', None)

    if school_name is None:
        school_name = ''

    department = request.args.get('department', None)

    sql = select_sql.format(school_name)

    if department  is not  None:
        sql += " and departement = '{}'".format(department)

    sql +=' LIMIT 30'

    logger.info("executing: {0}".format(sql))
    cur.execute(sql)
    schools = []
    for row in cur.fetchall():
        schools.append({
            'id': row[0], 
            'name': row[1], 
            'grouping': row[2], 
            'department': row[3], 
            'community': row[4], 
            'city': row[5], 
            'address': row[6], 
            'telephone': row[7],
            'neighborhood': row[8],
            'grant_suggested_by': row[9], 
            'director_name': row[10], 
            'year1_effective': row[11], 
            'year2_effective': row[12], 
            'year3_effective': row[13], 
            'year4_effective': row[14], 
            'year5_effective': row[15], 
            'year6_effective': row[16], 
            'unknown_effective': row[17], 
            'total_effective': row[18]
        })

    return 'mycallback( {0} )'.format(json.dumps(schools))

@app.errorhandler(Exception)
def handle_invalid_usage(error):
    return jsonify({"exception" : str(error)})

@app.route('/foo')
def get_foo():
    raise Exception('testing exception throwing')

if __name__ == '__main__':
    app.run(debug=True, port=5002)
