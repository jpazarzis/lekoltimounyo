from flask import Flask
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


select_sql = '''select school_id, school_name from schools where school_name like '{}%' LIMIT 30'''

select_school_sql = '''select grouping, departement , community , city, neighborhood, grant_suggested_by, school_name,
    director_name, address, telephone, year1_effective, year2_effective, year3_effective,
    year4_effective, year5_effective, year6_effective, unknown_effective, total_effective 
    from schools where school_id = {}
    '''

config = ConfigParser.RawConfigParser()
config.read('config.ini')

app = Flask(__name__)

HOSTNAME = config.get('dbsettings', 'HOSTNAME') 
USER = config.get('dbsettings', 'USER') 
PASSWORD = config.get('dbsettings', 'PASSWORD') 
DATABASE = config.get('dbsettings', 'DATABASE') 

db = MySQLdb.connect(host=HOSTNAME, user=USER, passwd=PASSWORD, db=DATABASE)


@app.route('/school/<school_id>')
def get_school_data(school_id):
    cur = db.cursor()
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

@app.route('/matches/<school_name>')
def get_matching_schools(school_name):
    cur = db.cursor()
    sql = select_sql.format(school_name)
    logger.info("executing: {0}".format(sql))
    cur.execute(sql)
    schools = []
    for row in cur.fetchall():
        schools.append({'id': row[0], 'name': row[1]})

    return 'mycallback( {0} )'.format(json.dumps(schools))

@app.errorhandler(Exception)
def handle_invalid_usage(error):
    return jsonify({"exception" : str(error)})

@app.route('/foo')
def get_foo():
    raise Exception('testing exception throwing')


if __name__ == '__main__':
    app.run(debug=True, port=5002)
