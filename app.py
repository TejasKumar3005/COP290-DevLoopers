from flask import Flask, render_template, session, redirect, request
import pymysql
from help import login_required,is_logged_in,upload_file_to_s3
from werkzeug.security import check_password_hash, generate_password_hash
from flask_session import Session

app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

connection = pymysql.connect(host='localhost',
                             user='newuser',
                             password='password',
                             database='zenfit',
                             cursorclass=pymysql.cursors.DictCursor)

def setup():
  # with connection:
    with connection.cursor() as cursor:

      cursor.execute("""CREATE TABLE IF NOT EXISTS `user` (
        `id` int NOT NULL AUTO_INCREMENT,
        `email` varchar(255) NOT NULL,
        `username` varchar(255) NOT NULL,
        `password` varchar(255) NOT NULL,
        `name` varchar(255) NOT NULL,
        `age` int NOT NULL,
        `height` int NOT NULL,
        `weight` int NOT NULL,
        PRIMARY KEY (`id`),
        UNIQUE KEY `username` (`username`)
      )""")

      cursor.execute("""CREATE TABLE IF NOT EXISTS `product` (
        `id` int NOT NULL AUTO_INCREMENT,
        `product_name` varchar(255) DEFAULT NULL,
        `rating` int DEFAULT NULL,
        `product_description` text DEFAULT NULL,
        `product_price` int DEFAULT NULL,
        `product_seller_id` int DEFAULT NULL,
        PRIMARY KEY (`id`),
        FOREIGN KEY (`product_seller_id`) REFERENCES `user` (`id`)
      )""")

      cursor.execute("""CREATE TABLE IF NOT EXISTS `order_product` (
        `id` int NOT NULL AUTO_INCREMENT,
        `order_id` int DEFAULT NULL,
        `product_id` int DEFAULT NULL,
        `quantity` int DEFAULT NULL,
        PRIMARY KEY (`id`),
        FOREIGN KEY (`product_id`) REFERENCES `product` (`id`)
        )""")

      cursor.execute("""CREATE TABLE IF NOT EXISTS `address` (
        `id` int NOT NULL AUTO_INCREMENT,
        `street` varchar(255) DEFAULT NULL,
        `city` varchar(255) DEFAULT NULL,
        `state` varchar(255) DEFAULT NULL,
        `zip` varchar(255) DEFAULT NULL,
        `user_id` int DEFAULT NULL,
        PRIMARY KEY (`id`),
        FOREIGN KEY (`user_id`) REFERENCES `user` (`id`)
      )""")

      cursor.execute("""CREATE TABLE IF NOT EXISTS `post` (
        `id` int NOT NULL AUTO_INCREMENT,
        `post_title` varchar(255) DEFAULT NULL,
        `post_time` datetime DEFAULT NULL,
        `post_text` text DEFAULT NULL,
        `user_id` int DEFAULT NULL,
        PRIMARY KEY (`id`),
        FOREIGN KEY (`user_id`) REFERENCES `user` (`id`)
      )""")

      cursor.execute("""CREATE TABLE IF NOT EXISTS `event` (
        `id` int NOT NULL AUTO_INCREMENT,
        `event_title` varchar(255) DEFAULT NULL,
        `event_organizer` varchar(255) DEFAULT NULL,
        `event_description` text DEFAULT NULL,
        `event_start` datetime DEFAULT NULL,
        `event_end` datetime DEFAULT NULL,
        PRIMARY KEY (`id`)
      )""")

      cursor.execute("""CREATE TABLE IF NOT EXISTS `note` (
        `id` int NOT NULL AUTO_INCREMENT,
        `note_title` varchar(255) DEFAULT NULL,
        `note_text` text DEFAULT NULL,
        `note_creation_time` datetime DEFAULT NULL,
        `note_update_time` datetime DEFAULT NULL,
        `note_taker_id` int NOT NULL,
        PRIMARY KEY (`id`),
        FOREIGN KEY (`note_taker_id`) REFERENCES `user` (`id`)
      )""")

      cursor.execute("""CREATE TABLE IF NOT EXISTS `order` (
        `id` int NOT NULL AUTO_INCREMENT,
        `order_id` int DEFAULT NULL,
        `order_status` int DEFAULT NULL,
        `user_id` int DEFAULT NULL,
        PRIMARY KEY (`id`),
        FOREIGN KEY (`user_id`) REFERENCES `user` (`id`)
      )""")

      cursor.execute("""CREATE TABLE IF NOT EXISTS `category` (
        `id` int NOT NULL AUTO_INCREMENT,
        `name` varchar(255) NOT NULL,
        PRIMARY KEY (`id`),
        UNIQUE KEY `name` (`name`)
        )""")

      cursor.execute("""CREATE TABLE IF NOT EXISTS `product_category` (
        `id` int NOT NULL AUTO_INCREMENT,
        `product_id` int DEFAULT NULL ,
        `category_id` int DEFAULT NULL,
        PRIMARY KEY (`id`),
        FOREIGN KEY (`product_id`) REFERENCES `product` (`id`),
        FOREIGN KEY (`category_id`) REFERENCES `category` (`id`)
      )""")

setup()

@app.route('/')
def index():
    if is_logged_in():
        return render_template('index.html', logged=1,userid=session["user_id"])
    return render_template('index.html', logged=0)

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            print(1)
            return "sad life"

        # Ensure password was submitted
        elif not request.form.get("password"):
            print(2)
            return "sad life"

        # Query database for username
        with connection.cursor() as cursor:
            sql = """SELECT * FROM `user` WHERE `username`=%s"""
            cursor.execute(sql,request.form.get("username"))
            rows = cursor.fetchall()

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["password"], request.form.get("password")):
            print(rows)
            print(3)
            return "sad life"

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return redirect("/")

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == 'POST':
        username = request.form.get("username")
        name = request.form.get("name")
        age = int(request.form.get("age"))
        height = int(request.form.get("height"))
        weight = int(request.form.get("weight"))
        password = request.form.get("password")
        email = request.form.get("email")
        confirmation = request.form.get("confirmation")
        hash = generate_password_hash(password)

        with connection.cursor() as cursor:
            sql = """SELECT * FROM `user` WHERE `username`=%s"""
            cursor.execute(sql,username)
            rows = cursor.fetchall()

        if rows or not username:
            return "name exists or empty"

        if password != confirmation or not password:
            return "passwords do not match or empty"

        with connection.cursor() as cursor:
            sql = f"INSERT INTO user (username,email,name,age,height,weight,password) VALUES (%s,%s,%s,%s,%s,%s,%s)"
            cursor.execute(sql, (username,email,name,age,height,weight,hash))
            connection.commit()

        return redirect("/")

    else:
        return redirect("/")

@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")

@app.route("/profile/<userid>")
@login_required
def profile(userid):
    if session["user_id"] == int(userid):
        return render_template("profile.html")
    else:
        return redirect("/")

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# function to check file extension
def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/post",methods=["GET"])
def post():
    return render_template("post.html")

@app.route("/upload", methods=["POST"])
def create():

    # check whether an input field with name 'user_file' exist
    if 'user_file' not in request.files:
        return "user file not found"

    # after confirm 'user_file' exist, get the file from input
    file = request.files['user_file']

    # check whether a file is selected
    if file.filename == '':
        return "no file selected"

    # check whether the file extension is allowed (eg. png,jpeg,jpg,gif)
    if file and allowed_file(file.filename):
        output = upload_file_to_s3(file)
        print(output) 
        
        # if upload success,will return file name of uploaded file
        if output:
            # write your code here 
            # to save the file name in database
            return "uploaded"

        # upload failed, redirect to upload page
        else:
            return "Unable to upload, try again"
        
    # if file extension not allowed
    else:
        return "File type not accepted,please try again."

@app.route("/store",methods=["GET","POST"])
def store():
        with connection.cursor() as cursor:
            sql = """SELECT * FROM `product`"""
            cursor.execute(sql)
            rows = cursor.fetchall()

        print(rows)

        return render_template("store-page.html",products=[rows])

@app.route("/product/<productid>",methods=["GET","POST"])
@login_required
def product(productid):
    
