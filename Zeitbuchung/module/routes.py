from module import app
from module.database import check_user, check_email, check_login, create_user, get_time_entries, db_create_time_entry, db_get_time_entry, delete_time_entry, db_update_time_entry

from datetime import datetime, timezone, timedelta
from flask import render_template, request, session, redirect, url_for, flash

@app.route('/')
@app.route('/home')
def home():
    print("---> home()")

    cookie = request.cookies.get( key="name" )

    return render_template( "home.html", cookie=cookie )

@app.route( '/login', methods=[ "GET", 'POST' ] )
def login():
    print( "---> login()" )

    cookie = request.cookies.get( key="name" )

    if cookie:
        print( "Kein Cookie gesetzt!" )
        return redirect( url_for( "time_entries" ) )

    if request.method == 'POST':
        username = request.form.get( "username" )
        password = request.form.get( "password" )
        print(username)
        print(password)

        value = username

        # username kommt zurück, wenn der Login erfolgreich ist
        check_log = check_login( username, password )

        if not check_log:
            flash( "Falscher Username oder Passwort!", "danger" )
            return render_template( "login.html", cookie=None )
        
        expires = datetime.now( timezone.utc ) + timedelta( minutes=10 )
        flash( f"Erfolgreich eingloggt, { check_log }!", "success" )
        response = redirect( url_for( "time_entries" ) )
        response.set_cookie( key="name", value=value, expires=expires )
        return response
    
    return render_template( "login.html", cookie=None )

@app.route( "/logout" )
def logout():
    print( "---> logout()" )

    session.pop( "_flashes", None)
    response = redirect( url_for( "login" ) )
    response.set_cookie( key="name", value="", expires=0 )
    return response

@app.route( "/register", methods=[ "GET", 'POST' ])
def register():
    print( "---> register()" )

    if request.method == "POST":
        username = request.form.get('username')
        email = request.form.get('e_mail')
        password_1 = request.form.get('password_1')
        password_2 = request.form.get('password_2')
        print( username )
        print( email )
        print( password_1 )
        print( password_2 )

        message = ""

        if check_user( username ):
            message += "Benutzer existiert bereits. "
        
        if check_email( email ):
            message += "E-Mail existiert bereits. "

        if password_1 != password_2:
            message += "Passwörter stimmen nicht überein!"

        if message:
            flash( message, "danger" )
            return render_template( "register.html" )
        
        create_user( username, email, password_1 )
        flash( "Erfolgreich registriert! Bitte loggen Sie sich ein.", "success" )
        return redirect( url_for( "login" ) )
    
    return render_template( "register.html" )

@app.route( "/time_entries" )
def time_entries():
    print( "---> time_entries()" )

    cookie = request.cookies.get( key="name" )
    #if "name2" in session:
        #print( f"Name1: {session["name1"]}")
    #else:
        #print("Kein name2")

    if not cookie:
        print("Kein Cookie gesetzt!")
        return redirect( url_for( "login" ) )
    
    entries = get_time_entries()
    #print(entries)
    
    return render_template( "time_entries.html", entries=entries, cookie=cookie )

@app.route( "/create_time_entry", methods=[ "GET", "POST" ] )
def create_time_entry():
    print("---> create_time_entry()")

    cookie = request.cookies.get('name')

    if not cookie:
        print( "Kein Cookie gesetzt!" )
        return redirect( url_for( "login" ) )

    if request.method == "POST":
        date = request.form.get( "date" )
        clockIn = request.form.get( "clockIn" )
        clockOut = request.form.get( "clockOut" )
        description = request.form.get( "description" )

        r = db_create_time_entry( date, clockIn, clockOut, description, cookie )
        print( r )

        resp = redirect( url_for( "time_entries" ) )
        resp.set_cookie( "name", cookie)
        return resp

    return render_template( "create_time_entry.html", cookie=cookie)

@app.route( "/update_time_entry/<int:id>", methods=[ "GET", "POST" ] )
def update_time_entry( id ):
    print("---> update_time_entry()")

    cookie = request.cookies.get('name')
    
    if not cookie:
        print( "Kein Cookie gesetzt!" )
        return redirect( url_for( "login" ) )

    entry = db_get_time_entry( id )

    if request.method == "POST":
        date = request.form.get( "date" )
        clockIn = request.form.get( "clockIn" )
        clockOut = request.form.get( "clockOut" )
        description = request.form.get( "description" )
        print(description)

        r = db_update_time_entry( id, date, clockIn, clockOut, description, cookie )
        print( r )

        resp = redirect( url_for( "time_entries" ) )
        resp.set_cookie( "name", cookie)
        return resp

    return render_template( "update_time_entry.html", entry=entry, cookie=cookie)

@app.route( "/delete_time_entries/<int:id>", methods=[ "GET" ])
def delete_time_entries( id ):
    print("---> delete_time_entries()")

    delete_time_entry( id )

    return redirect( url_for( "time_entries" ) )

@app.template_filter()
def format_timedelta( td ):
    total_seconds = int( td.total_seconds() )
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    return f"{hours:02}:{minutes:02}"
