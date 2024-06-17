from sqlalchemy import create_engine, text, exc

USERNAME = 'root'
PASSWORD = 'root'
HOST = 'localhost'
PORT = '3306'
DATABASE = 'time_management'

CONNECTION_STRING = f"mariadb+pymysql://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}"
engine = create_engine(CONNECTION_STRING)

def create_user( name, email, password ):
    query = f"""INSERT INTO users (name, email, password) 
                VALUES ( '{name}', '{ email }', '{ password }');"""
    print(text(query))
    with engine.connect() as connection:
        connection.execute( text( query ) )
        connection.commit()

def check_user( user ):
    query = f"SELECT * FROM users WHERE name = '{ user }';"
    with engine.connect() as connection:
        result = connection.execute( text( query ) ).fetchone()
        print( result )

        if result:
            return True
        return False

def check_email( email ):
    query = f"SELECT * FROM users WHERE email = '{ email }';"
    with engine.connect() as connection:
        result = connection.execute( text( query ) ).fetchall()
        print( result )

        if result:
            return True
        return False

def check_login( username, password ):
    query = f"select name from users where name = '{ username }' and password = '{ password }'"
    print( query )
    with engine.connect() as connection:
        result = connection.execute( text( query ) ).fetchall()
        print( result )
        return result
    
def db_create_time_entry(date, clock_in, clock_out, description, name):
    query = text("INSERT INTO time (date, clockIn, clockOut, description, name) VALUES (:date, :clock_in, :clock_out, :description, :name);")
    try:
        with engine.connect() as connection:
            connection.execute( query, { 'date': date, 'clock_in': clock_in, 'clock_out': clock_out, 'description': description, 'name': name } )
            connection.commit()
        return "Time entry created successfully"
    except exc.SQLAlchemyError as e:
        return f"Error creating time entry: { e }"

def db_update_time_entry(entry_id, date=None, clock_in=None, clock_out=None, description=None, name=None):
    updates = []
    params = {}
    if date:
        updates.append( "date = :date" )
        params[ "date" ] = date
    if clock_in:
        updates.append( "clockIn = :clock_in" )
        params[ "clock_in" ] = clock_in
    if clock_out:
        updates.append( "clockOut = :clock_out" )
        params[ "clock_out" ] = clock_out
    if description:
        updates.append( "description = :description" )
        params[ "description" ] = description
    if name:
        updates.append( "name = :name" )
        params[ "name" ] = name

    update_statement = ", ".join(updates)
    query = text(f"UPDATE time SET { update_statement } WHERE id = :entry_id;")
    params[ "entry_id" ] = entry_id

    try:
        with engine.connect() as connection:
            connection.execute(query, params)
            connection.commit()
        return "Time entry updated successfully"
    except exc.SQLAlchemyError as e:
        return f"Error updating time entry: { e }"

def get_time_entries():
    query = text("SELECT * FROM time;")
    try:
        with engine.connect() as connection:
            result = connection.execute(query).fetchall()
        return result
    except exc.SQLAlchemyError as e:
        return f"Error retrieving time entries: { e }"

def db_get_time_entry(entry_id):
    query = text("SELECT * FROM time WHERE id = :entry_id;")
    try:
        with engine.connect() as connection:
            result = connection.execute(query, {'entry_id': entry_id}).fetchone()
        return result
    except exc.SQLAlchemyError as e:
        return f"Error retrieving time entry: {e}"

def delete_time_entry(entry_id):
    query = text("DELETE FROM time WHERE id = :entry_id;")
    try:
        with engine.connect() as connection:
            connection.execute(query, {'entry_id': entry_id})
            connection.commit()
        return "Time entry deleted successfully"
    except exc.SQLAlchemyError as e:
        return f"Error deleting time entry: {e}"
