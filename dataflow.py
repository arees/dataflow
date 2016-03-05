#
#  DDDDDDDDDDDDD                                 tttt                               ffffffffffffffff  lllllll
#  D::::::::::::DDD                           ttt:::t                              f::::::::::::::::f l:::::l
#  D:::::::::::::::DD                         t:::::t                             f::::::::::::::::::fl:::::l
#  DDD:::::DDDDD:::::D                        t:::::t                             f::::::fffffff:::::fl:::::l
#    D:::::D    D:::::D  aaaaaaaaaaaaa  ttttttt:::::ttttttt      aaaaaaaaaaaaa    f:::::f       ffffff l::::l    ooooooooooo wwwwwww           wwwww           wwwwwww
#    D:::::D     D:::::D a::::::::::::a t:::::::::::::::::t      a::::::::::::a   f:::::f              l::::l  oo:::::::::::oow:::::w         w:::::w         w:::::w
#    D:::::D     D:::::D aaaaaaaaa:::::at:::::::::::::::::t      aaaaaaaaa:::::a f:::::::ffffff        l::::l o:::::::::::::::ow:::::w       w:::::::w       w:::::w
#    D:::::D     D:::::D          a::::atttttt:::::::tttttt               a::::a f::::::::::::f        l::::l o:::::ooooo:::::o w:::::w     w:::::::::w     w:::::w
#    D:::::D     D:::::D   aaaaaaa:::::a      t:::::t              aaaaaaa:::::a f::::::::::::f        l::::l o::::o     o::::o  w:::::w   w:::::w:::::w   w:::::w
#    D:::::D     D:::::D aa::::::::::::a      t:::::t            aa::::::::::::a f:::::::ffffff        l::::l o::::o     o::::o   w:::::w w:::::w w:::::w w:::::w
#    D:::::D     D:::::Da::::aaaa::::::a      t:::::t           a::::aaaa::::::a  f:::::f              l::::l o::::o     o::::o    w:::::w:::::w   w:::::w:::::w
#    D:::::D    D:::::Da::::a    a:::::a      t:::::t    tttttta::::a    a:::::a  f:::::f              l::::l o::::o     o::::o     w:::::::::w     w:::::::::w
#  DDD:::::DDDDD:::::D a::::a    a:::::a      t::::::tttt:::::ta::::a    a:::::a f:::::::f            l::::::lo:::::ooooo:::::o      w:::::::w       w:::::::w
#  D:::::::::::::::DD  a:::::aaaa::::::a      tt::::::::::::::ta:::::aaaa::::::a f:::::::f            l::::::lo:::::::::::::::o       w:::::w         w:::::w
#  D::::::::::::DDD     a::::::::::aa:::a       tt:::::::::::tt a::::::::::aa:::af:::::::f            l::::::l oo:::::::::::oo         w:::w           w:::w
#  DDDDDDDDDDDDD         aaaaaaaaaa  aaaa         ttttttttttt    aaaaaaaaaa  aaaafffffffff            llllllll   ooooooooooo            www             www

from flask import Flask, request, render_template, session, g, _app_ctx_stack, url_for, redirect, jsonify
from sqlite3 import dbapi2 as sqlite3
from werkzeug import generate_password_hash, check_password_hash
import os, json

app = Flask(__name__)

app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'dataflow.db'),
    DEBUG=True,
    SECRET_KEY='development key'
))

def get_json(path, one=True):
     json_file = open('json1')
     json_str = json_file.read()
     json_data = json.load(json_str)
     return json_data[0] if one else json_data

def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    top = _app_ctx_stack.top
    if not hasattr(top, 'sqlite_db'):
        top.sqlite_db = sqlite3.connect(app.config['DATABASE'])
        top.sqlite_db.row_factory = sqlite3.Row
    return top.sqlite_db


@app.teardown_appcontext
def close_database(exception):
    """Closes the database again at the end of the request."""
    top = _app_ctx_stack.top
    if hasattr(top, 'sqlite_db'):
        top.sqlite_db.close()


def init_db():
    """Initializes the database."""
    db = get_db()
    with app.open_resource('schema.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()


@app.cli.command('initdb')
def initdb_command():
    """Creates the database tables."""
    init_db()
    print('Initialized the database.')


def query_db(query, args=(), one=False):
    """Queries the database and returns a list of dictionaries."""
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    return (rv[0] if rv else None) if one else rv

@app.before_request
def before_request():
    g.user = None
    if 'user_id' in session:
        g.user = query_db('select * from user where user_id = ?',
                          [session['user_id']], one=True)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/register", methods=["POST"])
def register():
    if request.method == 'POST':
        db = get_db()
        user = request.form['user']
        password = request.form['pswd']
        password_hash = generate_password_hash(password)
        email = request.form['email']
        company_short_name = request.form['csn']
        company_long_name = request.form['cln']
        region = request.form['company-region']
        company_type = request.form['company-type']
        datacoin = db.execute('insert into datacoin (datacoin_value, trust) values (?, ?)', [50,50])
        datacoin_id = datacoin.lastrowid
        money = db.execute('insert into money (money_value) values (?)', [50])
        money_id = money.lastrowid

        print(request.form)

        if company_type == "isp":
            db.execute('insert into isp (short_name, long_name, region_id, datacoin_id, money_id, reputation, password_hash, username, coverage) values(?, ?, ?, ?, ?, ?, ?, ?, ?)', [company_short_name, company_long_name, region, datacoin_id, money_id, 15, password_hash, user, 5])
        elif company_type == "dev":
            isp_id = request.form['company-isp']
            db.execute('insert into developer(short_name, long_name, region_id, datacoin_id, money_id, isp_id, reputation, password_hash, username) values(?, ?, ?, ?, ? , ?, ? , ?, ?)', [company_short_name, company_long_name, region, datacoin_id, money_id, isp_id, 15, password_hash, user])

        db.commit()
        return redirect(url_for('index'))


@app.route('/get_isps_region')
def get_isp_per_region():
    region_id = request.args.get('region', 1, type=int)
    isps = query_db('select * from isp where region_id = ?', [region_id])
    isp_list = []
    for isp in isps:
        new_isp = {}
        new_isp['long_name'] = isp['long_name']
        new_isp['id'] = isp['isp_id']
        isp_list.append(new_isp)

    return jsonify(isps=isp_list)

if __name__ == "__main__":
    app.run(host='0.0.0.0')
