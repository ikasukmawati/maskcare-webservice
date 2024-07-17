import os
from itsdangerous import URLSafeTimedSerializer
from flask import Response, render_template, url_for
from werkzeug.utils import secure_filename

from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped, mapped_column
from flask import jsonify

from argon2 import PasswordHasher

from datetime import timedelta,datetime

from flask_jwt_extended import *

import functools

from detect_count import count_object

class Base(DeclarativeBase): 
    pass #Blank body class, but "Base" class inherits "DeclarativeBase" class


UPLOAD_FOLDER = 'static/uploads/'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}


# Instantiate Flask
app = Flask(__name__) 
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root:@127.0.0.1/db_facemask"  #"mysql://username:password@localhost/databasename"  

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Instantiate SQLALchemy
db = SQLAlchemy(model_class=Base) 
db.init_app(app)

# Setup the Flask-JWT-Extended extension
app.config["JWT_SECRET_KEY"] = "super-secret"  # Change this!
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(days=1)
jwt = JWTManager(app)

class User(db.Model): #User class inherit Model class
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(unique=True)
    name: Mapped[str]
    password: Mapped[str]
    avatar: Mapped[str] = mapped_column(nullable=True)
    created_at: Mapped[str]
    updated_at: Mapped[str]

class ApiKey(db.Model): #User class inherit Model class
    api_key: Mapped[str] = mapped_column(primary_key=True)
    

class Artikel(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    judul: Mapped[str]
    konten: Mapped[str]
    
class Gambar(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    pathname: Mapped[str]
    deskripsi: Mapped[str]
   

@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    identity = jwt_data["sub"]
    return User.query.filter_by(id=identity).one_or_none()

def api_key_required(func):
    @functools.wraps(func)
    def check_api_key():
        apiKey = request.headers.get('x-api-key')
        apiKey = ApiKey.query.filter_by(api_key=apiKey).one_or_none()
        if apiKey:
            return func()
        else:
            return {"message": "Please provide a correct API key"}, 400
    return check_api_key


# @app.post('/register')
# def register():
#     name = request.form.get("name")
#     email = request.form.get("email")
#     password = request.form.get("password")
    
#     if not email:
#         return {"message": "Email harus diisi"}, 400

#     existing_user = User.query.filter_by(email=email).first()
#     if existing_user:
#         return {"error": True, "message": "Email sudah terdaftar. Silakan gunakan email lain."}, 400
        
#     hashed_password = PasswordHasher().hash(password)
#     created_at = datetime.now()
#     updated_at = datetime.now()

#     new_user = User(
#         email=email,
#         name=name,
#         password=hashed_password,  
#         created_at=created_at,
#         updated_at=updated_at
#     )
#     db.session.add(new_user)
#     db.session.commit()

#     # Generate verification token
#     token = generate_verification_token(email)
#     verification_url = url_for('verify_email', token=token, _external=True)
#     html = render_template('verify_email.html', verification_url=verification_url)

#     # Send verification email
#     msg = Message('Please verify your email', recipients=[email])
#     msg.body = f'Thanks for signing up! Please verify your email by clicking on the following link: {verification_url}'
#     msg.html = html
#     mail.send(msg)
    
#     return {"message": "Sukses melakukan registrasi. Silakan periksa email Anda untuk verifikasi.", "error": False}, 201

# @app.route('/verify_email/<token>')
# def verify_email(token):
#     try:
#         email = confirm_verification_token(token)
#     except:
#         return {"message": "The confirmation link is invalid or has expired."}, 400

#     user = User.query.filter_by(email=email).first_or_404()
#     if user.is_verified:
#         return {"message": "Account already verified. Please login."}, 200
#     else:
#         user.is_verified = True
#         user.updated_at = datetime.now()
#         db.session.add(user)
#         db.session.commit()
#         return {"message": "You have confirmed your account. Thanks!"}, 200

@app.route("/user", methods=['GET','POST','PUT','DELETE'])
@jwt_required()
def user():
    if request.method == 'POST':
        dataDict = request.get_json() #It return dictionary.
        email = dataDict["email"]
        name = dataDict["name"]
        password = dataDict["password"]
        
        hashed_password = PasswordHasher().hash(password)
        
        created_at= datetime.now()
        updated_at= datetime.now()
        
        user = User(
            email= email,
            name = name,
            password=hashed_password,
            created_at = created_at,
            updated_at = updated_at
        )
        db.session.add(user)
        db.session.commit()
        
        user_id = user.id
        res = {
            "id": user_id,
            "name" : user.name,
            "email" : user.email
        }
        
        return {
            "data": res,
            "message": "Successfull",
        },200
        
        
    elif request.method == 'PUT':
        dataDict = request.get_json()
        id = dataDict["id"]
        email = dataDict["email"]
        name = dataDict["name"]
        
        if not id:
            return {
                "message": "ID required"
            },400
        
        row = db.session.execute(
            db.select(User) #Select from user model
            .filter_by(id=id) #where ID=1  by id
            ).scalar_one() # Return a list of rows.
        if "email" in dataDict : 
            row.email = dataDict["email"]
            
        if "name" in dataDict :
            row.name = dataDict["name"]
        
        row.updated_at=datetime.now()

        db.session.commit()
        return {
            "message": "Success update data user"
        }, 200
        
    elif request.method == 'DELETE':
        dataDict = request.get_json() #It return dictionary.
        id = dataDict["id"]
        
        if not id:
            return {
                "message": "ID required"
            },400
        
        row = db.session.execute(
            db.select(User) #Select from user model
            .filter_by(id=id) #where ID=1  by id
            ).scalar_one() # Return a list of rows.
        
        db.session.delete(row)
        db.session.commit()
        return {
            "message": "Successfull!"
        }, 200
    else : #GET
        rows = db.session.execute(
            db.select(User).order_by(User.id)
            ).scalars()
        
        users =[]
        for row in rows:
            users.append({
                "id" : row.id,
                "email" : row.email,
                "name" : row.name,
                "avatar" : row.avatar
            })
        return {
            "data" : users,
            "message" : "Sukses menampilkan data user"
        },200
        

@app.post('/signup')
def signup():
    name = request.form.get("name")
    email = request.form.get("email")
    password = request.form.get("password")
    # re_password = request.form.get("re_password")
    
    created_at= datetime.now()
    updated_at= datetime.now()
    
    # Memeriksa apakah password sama dengan re_password
    # if password != re_password:
    #     return {
    #         "message" : "Password tidak sama!"
    #     }, 400
    
    # Memeriksa apakah email terisi
    if not email:
        return {
            "message" : "Email harus diisi"
        }, 400
        
    # Mengecek apakah email sudah terdaftar sebelumnya
    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        return {
            "error" : True,
            "message": "Email sudah terdaftar. Silakan gunakan email lain."
        }, 400
        
    # Menghash password menggunakan Argon2
    hashed_password = PasswordHasher().hash(password)
    
    # Pastikan properti ini sesuai dengan definisi model
    new_user = User(
        email=email,
        name=name,
        password=hashed_password,  
        created_at=created_at,
        updated_at=updated_at
    )
    db.session.add(new_user)
    db.session.commit()
    
    return {

        "message" : "Sukses melakukan registrasi",
        "error": False
        
    },201   
        
    

@app.post("/signin")
def signin():
    email = request.form.get("email")
    password = request.form.get("password")
    
    # Memanggil data email pada database
    user = db.session.execute(
        db.select(User)
        .filter_by(email=email)
    ).scalar_one()
    
    if not user or not PasswordHasher().verify(user.password, password):
        return {
            "message": "wrong password or email!"
        },400
    #End Authentication    
    #Start Generate JWT Token
    access_token = create_access_token(identity=user.id)
    #End Generate JWT Token
    return {
        "access_token" : access_token,
    },200
    
@app.route('/change_password', methods=['PUT'])
@jwt_required()
def change_password():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    
    if not user:
        return jsonify({"message": "User not found"}), 404
    
    current_password = request.form.get("current_password")
    new_password = request.form.get("new_password")
    
    
    if not current_password or not new_password:
        return jsonify({"message": "Current and new passwords are required"}), 400
    
    # Verify current password
    try:
        PasswordHasher().verify(user.password, current_password)
    except:
        return jsonify({"message": "Current password is incorrect"}), 400
    
    # Hash new password
    hashed_password = PasswordHasher().hash(new_password)
    
    # Update user's password
    user.password = hashed_password
    user.updated_at = datetime.now()
    db.session.commit()
    
    return jsonify({"message": "Password updated successfully"}), 200


@app.get('/protected')
@jwt_required()
def protected():
    current_user_id = get_jwt_identity()
    user = db.session.get(User, current_user_id)
    return jsonify(name=user.name, email=user.email,avatar=user.avatar), 200
    

@app.route("/artikel", methods=['GET','POST'])
# @api_key_required
# @jwt_required()
def artikel():
    if request.method == 'POST':
        dataDict = request.get_json()  # Menggunakan request.form untuk mendapatkan data formulir dari permintaan
        judul = dataDict["judul"]
        konten = dataDict["konten"]
        
        artikel = Artikel(
            judul=judul,
            konten=konten,
            
        )
        db.session.add(artikel)
        db.session.commit()
        
        return {
            "message": "Artikel berhasil dibuat",
            "data": {"judul": judul, "konten": konten}
        }, 200 
    else : #GET
        rows = db.session.execute(
            db.select(Artikel).order_by(Artikel.id)
            ).scalars()
        
        artikels =[]
        for row in rows:
            artikels.append({
                "id" : row.id,
                "judul" : row.judul,
                "konten" : row.konten,
            })
        return artikels, 200

@app.route("/artikel/<id>", methods=['PUT','DELETE'])
# @jwt_required()
def detailartikel(id):
    if request.method == 'PUT':
        dataDict = request.get_json() #It return dictionary.
        judul = dataDict["judul"]
        konten = dataDict["konten"]
        
        artikel_id = Artikel.query.filter_by(id=id).first()

        if not artikel_id:
            return {
                "message": "ID tidak tersedia"
            },400
        
        row = db.session.execute(
            db.select(Artikel) #Select from user model
            .filter_by(id=id) #where ID=1  by id
            ).scalar_one() # Return a list of rows.
        
        row.judul = judul
        row.konten = konten
            
        db.session.commit()
        
        return {
            "message": "Success update article!"
        }, 200  
    else:
                
        if not id:
            return {
                "message": "ID required"
            },400
            
        row = db.session.execute(
            db.select(Artikel) #Select from user model
            .filter_by(id=id) #where ID=1  by id
            ).scalar_one() # Return a list of rows.

        
        db.session.delete(row)
        db.session.commit()
        return {
            "message": "Succes menghapus data artikel!"
        }, 200

        
@app.route("/user/<id>", methods=['GET','PUT','DELETE'])
# @jwt_required()
def detailUser(id):
    
    if request.method == 'PUT':
        dataDict = request.get_json()
        name = dataDict["name"]
        email = dataDict["email"]
        password = dataDict["password"]
        
        hashed_password = PasswordHasher().hash(password)
        
        if not id:
            return {
                "message": "ID required"
            },400
        
        row = db.session.execute(
            db.select(User) #Select from user model
            .filter_by(id=id) #where ID=1  by id
            ).scalar_one() # Return a list of rows.
        
        row.name = name
        row.email = email
        row.password = hashed_password
        row.updated_at=datetime.now()
        
        # if "email" in dataDict : 
        #     row.email = dataDict["email"]
            
        # if "name" in dataDict :
        #     row.name = dataDict["name"]
        db.session.commit()
        return {
            "message": "Success update data user"
        }, 200
        
    elif request.method == 'DELETE':
        
        user_id = User.query.filter_by(id=id).first()
        if not user_id:
            return {
                "error": True,
                "message": "ID diperlukan"
            }, 400
        
        row = db.session.execute(
            db.select(User) #Select from user model
            .filter_by(id=id) #where ID=1  by id
            ).scalar_one() # Return a list of rows.
        
        db.session.delete(row)
        db.session.commit()
        return {
            "message": "Suksek Menghapus Data!"
        }, 200
        
    else : #GET
        
        user_id = User.query.filter_by(id=id).first()
        if not user_id:
            return {
                "error": True,
                "message": "ID diperlukan"
            }, 400

        rows = db.session.execute(
            db.select(User)
            .filter_by(id=id)
            ).scalar_one()
        
        user_data = {
            "id": rows.id,
            "email": rows.email,
            "name": rows.name,
            "created_at" : rows.created_at,
            "updated_at" : rows.updated_at
        }
        
        return {
            "data" : user_data,
            "message" : "Sukses menampilkan data user by id"
        },200
        
def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
            
@app.route('/edit_profile', methods=['PUT'])
@jwt_required()
def edit_profile():
    current_user_id = get_jwt_identity()
    user = db.session.get(User, current_user_id)
    if not user:
        return jsonify({"message": "User not found"}), 404
    
    data = request.form if request.form else request.json
    
    if 'name' in data:
        user.name = data['name']

    if 'email' in data:
        user.email = data['email']
    
    if 'file' in request.files:
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            user.avatar = url_for('static', filename='uploads/' + filename, _external=True)

    user.updated_at = datetime.now()
    db.session.commit()

    return jsonify({
        "message": "Profile updated successfully",
    }), 200
    
    
# Realtime Object Detection & Counting
@app.route('/realtime')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(count_object(), mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    app.run(host='192.168.229.120', port=5000, debug=True)