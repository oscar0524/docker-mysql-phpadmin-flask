import os

from flask import Flask
from flask import jsonify
import pymysql

app = Flask(__name__)
sql_host = os.environ['APP_SQL_HOST']
sql_port = int(os.environ['APP_SQL_PORT'])
sql_user = os.environ['APP_USER']
sql_password = os.environ['APP_PASSWORD']
sql_db = os.environ['APP_SQL_DATABASE']


class Sql:
    @staticmethod
    def get_db():
        return pymysql.connect(host=sql_host,
                               port=sql_port,
                               user=sql_user,
                               charset='utf8',
                               password=sql_password,
                               database=sql_db,
                               cursorclass=pymysql.cursors.DictCursor
                               )

    @staticmethod
    def query(query: str, args=None, get_last_id=False):
        sql_result = None
        with Sql.get_db() as db:
            with db.cursor() as cursor:
                try:
                    if args is None:
                        cursor.execute(query)
                    else:
                        cursor.execute(query, args)

                    if get_last_id:
                        sql_result = cursor.lastrowid
                    else:
                        sql_result = cursor.fetchall()

                    db.commit()
                except pymysql.ProgrammingError as progErr:
                    print("{} ERROR SQL : [ {} ]", progErr, query)
                except Exception as ex:
                    db.rollback()
                    print("{} ERROR SQL : [ {} ]", ex, query)
        return sql_result


@app.route('/')
def hello_world():
    return 'hello_world'


@app.route('/users')
def get_users():
    result = Sql.query("SELECT * FROM users")
    print(result)
    return jsonify(result)


if __name__ == "__main__":
    app.config["JSON_AS_ASCII"] = False
    app.run(debug=True, host='0.0.0.0', port=5000)
