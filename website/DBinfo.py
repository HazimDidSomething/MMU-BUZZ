from flask import Blueprint ,render_template,request,flash,redirect,url_for
from sqlalchemy import inspect
from . import db

DBinfo = Blueprint('DBinfo',__name__)

@DBinfo.route('/DB_INFO')
def show_db_info():
    inspector = inspect(db.engine)
    tables_info = {}

    # Loop through all tables
    for table_name in inspector.get_table_names():
        columns = inspector.get_columns(table_name)
        tables_info[table_name] = [col["name"] + " (" + str(col["type"]) + ")" for col in columns]

    # Print to console
    print("=== Database Info ===")
    for table, cols in tables_info.items():
        print(f"Table: {table}")
        for col in cols:
            print(f"  - {col}")

    # Return in browser too
    return tables_info, render_template("home.html") 