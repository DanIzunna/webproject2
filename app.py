
from flask import Flask, render_template, request, redirect, url_for, session, jsonify, flash#,Response
from datetime import timedelta      #Check JS for timer
# from flask_mail import *
import hashlib    #To change to one for flask hashing
# import random
import re
from mysql.connector import OperationalError
from datetime import datetime
import pymysql
import datetime
import requests
from flask_caching import Cache
from config import Config



app = Flask(__name__)

app.config.from_object(Config)


# LInk to the online database ffrom Aiven
connection = pymysql.connect(
        host=app.config['DATABASE_HOST'],
        user=app.config['DATABASE_USER'],
        password=app.config['DATABASE_PASSWORD'],
        db=app.config['DATABASE_NAME'],
        port=app.config['DATABASE_PORT'],
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )
    
cursor = connection.cursor()

# For sessions

app.config['PERMANENT_SESSION_LIFETIME'] =  timedelta(minutes=30)


# To Make secret key

app.secret_key = app.config['SECRET_KEY']

# UNSPLASH ACCESS KEY

UNSPLASH_ACCESS_KEY = app.config['UNSPLASH_ACCESS_KEY']

app.config['CACHE_TYPE'] = 'SimpleCache'  # You can also use 'RedisCache', 'FileSystemCache', etc.
app.config['CACHE_DEFAULT_TIMEOUT'] = 300  # Cache timeout (in seconds)

# Initialize Cache
cache = Cache(app)
# _____________________________________________________________________
# PROGRAM STARTS

@cache.cached(timeout=300, key_prefix='unsplash_image')  # Cache for 5 minutes
def get_unsplash_image(query):
    url = f"https://api.unsplash.com/photos/random?query={query}&client_id={UNSPLASH_ACCESS_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()['urls']['regular']
    else:
        return None

# Homepage
@app.route('/')
def index():
    return render_template('index.html')

# Blog 
@app.route("/blog/", methods = ["GET", "POST"])
def blog():
    sql = "select * from Blog order by publish_date desc"
    cursor.execute(sql)
    blogs = cursor.fetchall()
    result = cursor.fetchone()  # Since you're expecting a single result

# Check if a result was found
    if result:
        query = result[0]  # Assign the category to the 'query' variable as a string
    else:
        query = 'Tech'
    if blog:
        image_url = get_unsplash_image(query)
        if image_url:
            return render_template('all_blogs.html', blogs = blogs, image_url = image_url)
    return render_template('all_blogs.html', blogs = blogs)

# Single Blog Post
@app.route("/blog/<blog_link>", methods = ["GET"])
def blog_post(blog_link):
    sql = "select * from Blog where blog_link = '%s'"%blog_link
    cursor.execute(sql)
    blog = cursor.fetchall()
    result = cursor.fetchone()  # Since you're expecting a single result

# Check if a result was found
    if result:
        query = result[0]  # Assign the category to the 'query' variable as a string
    else:
        query = 'Tech'
    if blog:
        image_url = get_unsplash_image(query)
        if image_url:
            return render_template('blog.html', blog = blog, image_url = image_url)
        return render_template('blog.html', blog = blog)
    else:
        return render_template('404.html')


# About Page
@app.route("/about/")
def about():
    return render_template('about.html')

# Display the videos in the site
@app.route('/videos/')
def videos():
    sql_select = "select * from Videos"
    cursor.execute(sql_select)
    videos = cursor.fetchall()
    return render_template('videos.html', videos=videos)


# Admin Panel

# For admin login
@app.route('/admin/login/', methods =['GET', 'POST']) 
def admin_login():
    msg = ''
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
        email = str(request.form['email'])
        _password = str(request.form['password'])
        password = hashlib.sha256(_password.encode()).hexdigest()
        sql_select = "SELECT * FROM Admins WHERE EMAIL = '%s' AND PASSWORD_ = '%s'"%(email, password)
        cursor.execute(sql_select)
        verify = cursor.fetchone()
        if verify:
            session['loggedin'] = True
            session['password'] = verify['PASSWORD_']
            session['email'] = verify['EMAIL']
            session['role'] = 'admin'
            return redirect(url_for('dashboard'))
        else:
            msg = 'Invalid Email Address / Password!!'
            flash(msg, 'error')
    return render_template('login.html')

# Create Admin 
@app.route("/admin/create/", methods = ["GET", "POST"])
def create_admin():
    if 'loggedin' in session:
        if session['role'] == 'admin':
            if request.method == 'POST' and 'first_name'in request.form and 'last_name' in request.form and 'password' in request.form and 'email'  in request.form :
                first_name = request.form['first_name'].upper()
                last_name = request.form['last_name'].upper()
                email = request.form['email']
                _password = request.form['password']
                _password = str(_password)
                password = hashlib.sha256(_password.encode()).hexdigest()
                cursor.execute("SELECT * from Admins WHERE EMAIL = '%s'"%email)
                new_user = cursor.fetchone()
                if new_user:
                    msg = 'Account already exists !'
                    flash(msg, 'error')
                    return render_template('create_admin.html', msg = msg)
                    
                # elif not re.match( r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.tequant\.ng$', email):
                #     msg = 'Invalid email address !'
                else:
                    sql = """INSERT INTO Admins(FIRST_NAME, LAST_NAME, EMAIL, PASSWORD_) VALUES(%s, %s, %s, %s)"""
                    vals = (first_name, last_name, email, password)
                    cursor.execute(sql, vals)
                    connection.commit()
                    # connection.close()
                    msg = 'Posted successfully !!'
                    flash(msg, 'success')
                return redirect(url_for('dashboard'))
            return render_template('create_admin.html')
        else:
            return render_template('403.html')
    msg = 'Session TimeOut'
    flash(msg, 'warning')
    return redirect(url_for('admin_login', next = '/admin/create/' ))
    
# Admin Dashboard
@app.route('/admin/')
def dashboard():
    if 'loggedin' in session:
        if session['role'] == 'admin':
            sql_select = "SELECT * FROM Admins WHERE email = '%s' and password_ = '%s'"%(session['email'],session['password'] )
            cursor.execute(sql_select)
            name = cursor.fetchall()
            sql_select = "select count(*) from Students;"
            cursor.execute(sql_select)
            students = cursor.fetchall()
            sql_select = "select count(*) from Admins"
            cursor.execute(sql_select)
            admins = cursor.fetchall()
            sql_select = "select count(*) from Blog"
            cursor.execute(sql_select)
            blogs = cursor.fetchall()
            sql_select = "select count(*) from Videos"
            cursor.execute(sql_select)
            videos = cursor.fetchall()
            return render_template("dashboard.html", name = name, students = students, admins = admins, blogs = blogs, videos = videos)
        else:
            return render_template('403.html')
    return redirect(url_for('admin_login', next= "url_for('dashboard')"))

# Add Blog Post
@app.route("/admin/blog/add/", methods = ["GET", "POST"])
def add_blog():
    if 'loggedin' in session:
        if session['role'] == 'admin':
            sql ="select first_name, last_name from Admins where email = '%s'"%session['email']
            cursor.execute(sql)
            names = cursor.fetchall()
            publish_date = datetime.date.today()

            if request.method == 'POST' and 'title' in request.form and 'body' in request.form and 'category' in request.form and 'author' in request.form:
                title = request.form['title']
                blog_link = title.lower().replace(' ', '-')
                body = request.form['body']
                category = request.form['category'].title()
                author = request.form['author']
                sql_select = "select * from Blog where blog_link = '%s'"%blog_link
                cursor.execute(sql_select)
                new_blog = cursor.fetchone()
                if new_blog:
                    msg = 'Blog already Posted !!!'
                    flash(msg, 'error')
                    return render_template('add_blog.html', msg = msg)
                else:
                    sql = """insert into Blog (Title, Body, Category, author, publish_date, blog_link) values( %s, %s, %s, %s, %s, %s)"""
                    vals = (title, body, category, author, publish_date, blog_link)
                    cursor.execute(sql, vals)
                    connection.commit()
                    # connection.close()
                    msg = 'Posted successfully !!'
                    flash(msg, 'success')
                return redirect(url_for('read_blog', blog_link = blog_link))
            return render_template('add_blog.html', names = names, publish_date = publish_date)
        else:
            return render_template('403.html')
    msg = 'Session TimeOut'
    flash(msg, 'warning')
    return redirect(url_for('admin_login', next = '/admin/blog/add/' ))

# Edit Blog Post
@app.route("/admin/blog/<blog_link>/edit/", methods =['GET', 'POST'])
def edit_blog(blog_link):
    if 'loggedin' in session:
        if session['role'] == 'admin':
            sql_select = "select * from Blog where blog_link = '%s'"%blog_link
            cursor.execute(sql_select)
            record = cursor.fetchall()
            return render_template('edit_blog.html', record = record)
        else:
            return render_template('403.html')
    return redirect(url_for('admin_login'))

# Save Changes to Blog Post
@app.route('/admin/blog/update/', methods = ['GET', 'POST'])
def save_blog():
    if 'loggedin' in session:
        if session['role'] == 'admin':
            if request.method == 'POST' and 'title' in request.form and 'body' in request.form and 'category' in request.form:
                title = request.form['title']
                blog_link = title.lower().replace(' ', '-')
                body = request.form['body']
                category = request.form['category'].title()
                author = request.form['author']
                sql = """UPDATE Blog SET Title = %s, Body = %s, Category = %s, Author = %s WHERE Blog_Link = %s"""
                vals = (title, body, category, author, blog_link)
                cursor.execute(sql, vals)
                connection.commit()
                # connection.close()
                msg = 'You have successfully updated Blog Post'
                flash(msg, 'success')
            return redirect(url_for('blog_view'))
        else:
            return render_template('403.html')
    return redirect(url_for('admin_login'))

# View blog in Admin Panel
@app.route("/admin/blog/<blog_link>/", methods =['GET', 'POST'])
def read_blog(blog_link):
    if 'loggedin' in session:
        if session['role'] == 'admin':
            sql_select = "select * from Blog where blog_link = '%s'"%blog_link
            cursor.execute(sql_select)
            record = cursor.fetchall()
            result = cursor.fetchone()  # Since you're expecting a single result
            if result:
                query = result[2]  # Assign the category to the 'query' variable as a string
            else:
                query = 'Tech'
            image_url = get_unsplash_image(query)
            if image_url:
                return render_template('read_blog.html', record = record, image_url=image_url)
            else:
                return render_template('read_blog.html', record = record)
        else:
            return render_template('403.html')
    return redirect(url_for('admin_login'))

# View All Blogs
@app.route("/admin/blog/all/", methods = ["GET", "POST"])
def blog_view():
    if 'loggedin' in session:
        if session['role'] == 'admin':
            sql_select = "SELECT * FROM Blog"
            cursor.execute(sql_select)
            record = cursor.fetchall()
            return render_template("blog_view.html", record = record)
        else:
            return render_template('403.html')
    return redirect(url_for('admin_login', next= "/admin/blog/all/"))

# Delete Blog
@app.route('/admin/blog/<blog_link>/delete/', methods = ['GET', 'POST'])
def delete_blog(blog_link):
    if 'loggedin' in session:
        if session['role'] == 'admin':
            if request.method == 'POST' and 'confirm' in request.form:
                confirm = request.form['confirm']
                if confirm == 'YES':
                    sql = "DELETE from Blog WHERE blog_link = '%s'" %blog_link
                    cursor.execute(sql)
                    connection.commit()
                    connection.close()
                    msg = 'You have successfully deleted Blog Post'
                    flash(msg, 'success')
                    return redirect(url_for('blog_view'))
            return render_template('delete_blog.html', blog_link = blog_link)
        else:
            return render_template('403.html')
    return redirect(url_for('admin_login'))

# Add videos site
# Add Video Post
@app.route("/admin/video/add/", methods = ["GET", "POST"])
def add_video():
    if 'loggedin' in session:
        if session['role'] == 'admin':
            upload_date = datetime.date.today()

            if request.method == 'POST' and 'title' in request.form and 'link' in request.form:
                title = request.form['title']
                link = request.form['link']
                sql_select = "select * from Videos where Link = '%s'"%link
                cursor.execute(sql_select)
                new_video = cursor.fetchone()
                if new_video:
                    msg = 'Video already Posted !!!'
                    flash(msg, 'error')
                    return render_template('add_video.html', msg = msg)
                else:
                    sql = """insert into Videos (Title, Link, upload_date) values(%s, %s, %s)"""
                    vals = (title, link, upload_date)
                    cursor.execute(sql, vals)
                    connection.commit()
                    # connection.close()
                    msg = 'Video Posted successfully !!'
                    flash(msg, 'success')
                return redirect(url_for('video_view'))
            return render_template('add_video.html',upload_date = upload_date)
        else:
            return render_template('403.html')
    msg = 'Session TimeOut'
    flash(msg, 'warning')
    return redirect(url_for('admin_login', next = '/admin/video/add/' ))

# All Videos
@app.route("/admin/video/all/", methods = ["GET", "POST"])
def video_view():
    if 'loggedin' in session:
        if session['role'] == 'admin':
            sql_select = 'SELECT * FROM Videos' 
            cursor.execute(sql_select)
            record = cursor.fetchall()
            return render_template("all_videos.html", record = record)
        else:
            return render_template('403.html')
    return redirect(url_for('admin_login', next= "/admin/video/all/"))

# Delete Video
@app.route('/admin/video/<link>/delete/', methods = ['GET', 'POST'])
def delete_video(link):
    if 'loggedin' in session:
        if session['role'] == 'admin':
            if request.method == 'POST' and request.json.get('confirm') == 'YES':
                sql = "DELETE FROM Videos WHERE Link = %s"%link
                cursor.execute(sql)
                connection.commit()
                connection.close()
                return jsonify({'status': 'success', 'message': 'Video deleted successfully'}), 200
            else:
                return jsonify({'status': 'error', 'message': 'Deletion not confirmed'}), 400
        return jsonify({'status': 'error', 'message': 'Unauthorized'}), 403
    return jsonify({'status': 'error', 'message': 'Not logged in'}), 401


#Logout
@app.route('/logout/')
def logout():
   session.pop('loggedin', None)
   session.pop('email', None)
   session.pop('student_ID', None)
   return redirect(url_for('index'))
   

@app.errorhandler(403)
def forbidden(error):
    return render_template("403.html")


@app.errorhandler(404)
def page_not_found(error):
    try:
        if session['role'] == 'admin':
            return render_template("404.html"), 404
        else:
            # To correct to general error
            return render_template("403.html"), 404
    except KeyError:
        return render_template("404.html"), 404


@app.errorhandler(OperationalError)
def handle_db_error(e):
    app.logger.error(f"Database OperationalError: {str(e)}")
    return render_template('db_error.html'), 500












































# Student Stuff
# Register for courses
@app.route("/register/")
def register():
    pass

# For Student Login
@app.route("/login/", methods = ["GET", "POST"])
def login():
    pass



# Create Student
@app.route("/admin/student/create/", methods = ["GET", "POST"])
def student_create():
    pass








































if __name__ == "__main__":
   app.run(host="0.0.0.0", port=5000, debug=True)
    # app.run(host='0.0.0.0', port=5000)





























































































# pip install python-dotenv
# DATABASE_URL=mysql://user:password@host/dbname
# from dotenv import load_dotenv
# load_dotenv()
# export FLASK_APP=app.py
# flask run


# For Flask Mail
# from flask import Flask
# from flask_mail import Mail, Message

# app = Flask(__name__)

# # Flask-Mail configuration for Hostinger's SMTP service
# app.config['MAIL_SERVER'] = 'smtp.hostinger.com'  # or mail.yourdomain.com
# app.config['MAIL_PORT'] = 465  # SSL port, use 587 for TLS
# app.config['MAIL_USE_TLS'] = False  # Use SSL, not TLS
# app.config['MAIL_USE_SSL'] = True  # Enable SSL
# app.config['MAIL_USERNAME'] = 'your-email@yourdomain.com'  # Your email hosted on Hostinger
# app.config['MAIL_PASSWORD'] = 'your-email-password'  # Your email password
# app.config['MAIL_DEFAULT_SENDER'] = 'your-email@yourdomain.com'  # Default sender email address

# # Initialize Flask-Mail
# mail = Mail(app)



# To read forom environment
# set MAIL_USERNAME=your-email@gmail.com
# set MAIL_PASSWORD=your-email-password


# import os

# app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
# app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
