from flask import Flask, render_template, request, redirect, session
import sqlite3
from email_validator import EmailNotValidError, validate_email # Ferramenta para a função de verificar se o email existe
from werkzeug.security import generate_password_hash, check_password_hash # Ferramenta para deixar a password segura

app = Flask(__name__) # Define a app
app.secret_key = "98734yhdn7q348o5cgyqn578otdhqo38573vmryaow3b85b42888xdnirt2873rbv3" # define a secret key

# Criação do banco de dados:
# Pequena analogia ======================
conexao = sqlite3.connect("database.db") # Cria uma ponte com a base de dados
cursor = conexao.cursor() # Cria o cursor que vai passar essa ponte
cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id TEXT PRIMARY KEY,
                hashpass TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                tips TEXT
            )
        """) # Cria a tabela com 4 colunas, chamada de users
conexao.commit() # Fecha a ponte
cursor.close() # Manda o cursor que atravessou a ponte, embora
conexao.close() # Derruba a ponte

#//ROTAS ==================================================================================================================

@app.route("/login", methods=["POST", "GET"]) # Rota de login
def login():
    if request.method == "POST":
        # Campos preenchidos na pagina de login --->
        Nome =  request.form.get("name") 
        Pass = request.form.get("password")
        maybe_user_data = get(Nome)

        
        if not Nome or not Pass: # Verifica se os dados foram introduzidos
            return render_template("login.html", acontecimento="")
        if maybe_user_data is None: # Verifica se o nome está no banco de dados
            return render_template("login.html", acontecimento="Password or username doesn't match, please try again!")
        if maybe_user_data["id"]:
                if check_password_hash(maybe_user_data["hashpass"], Pass): #Verifica se a pass inserida corresponde com a hash (Pass guardada)
                    session["user"] = Nome #Adiciona o nome do utilizador na sessão
                    return redirect("/")
                else:
                    return render_template("login.html", acontecimento="Password or username doesn't match, please try again!")


    elif request.method == "GET":
        return render_template("login.html", acontecimento="")


@app.route("/signin", methods=["POST", "GET"])
def signin():
    if request.method == "POST":
        # Campos preenchidos na pagina de signin --->
        Nome = request.form.get("name")
        Pass = request.form.get("password")
        hashpass = generate_password_hash(Pass)
        Email = request.form.get("email")
        maybe_user_data = get(Nome)

        if not all([Nome, Pass, hashpass, Email]): # Se algum deles não estiver preenchido, volta a trás
            return render_template("signin.html", acontecimento="Fill all the inputs.")
        # Se o nome já existir no banco de dados, volta a trás
        if maybe_user_data:
                return render_template("signin.html", acontecimento="Username already exists.")
        
        # Se o email não for valido ou já estiver a ser usado, volta a trás
        if not Email_valido(Email):
            return render_template("signin.html", acontecimento="This email isn't valid, or is already in use")
        
        # Se a password não for segura, volta a trás.
        elif not is_pass_safe(Pass):
            return render_template("signin.html", acontecimento="Choose a more secure password.")
        
        # Se estiver tudo bem, salva os dados.
        else:
            add_user(Nome, hashpass, Email)
            return render_template("login.html", acontecimento="User successfully registered.")
    
    # Se for method= GET
    return render_template("signin.html", acontecimento="")



@app.route("/", methods=["GET"]) #Rota da pagina principal
def home():
    if "user" not in session: # Se user não estiver logado, manda-o para o login, caso esteja, vai para a main page
        return redirect("/login")
    return render_template("home.html", user=session["user"])


@app.route("/logout", methods=["GET"]) # Rota do logout
def logout():
    session.pop("user", None)
    return redirect("/login")


@app.route("/aboutme") # Rota do about me
def about_me():
    if "user" in session: # Se user não estiver logado, manda-o para o login, caso esteja, vai para a about me page
        return render_template("aboutme.html", user=session["user"])
    return redirect("/login")


@app.route("/Addtips", methods= ["POST", "GET"]) # Rota das dicas de melhorias
def add_tips():
    if "user" in session and request.method == "POST":
        tip = str(request.form.get("tip")) # Pega a dica 
        user_data = get(session["user"])
        if tip: # Se ouver dica salva-a no banco de dados
            update_tips(user_data["id"], tip)
        return redirect("/aboutme")
    # Se for method= GET
    return redirect("/")
# //DEFS ===================================================================================================================

def is_pass_safe(passe): # Verifica se a password é segura
    return (len(passe) >= 8 and any(c.isdigit() for c in passe) and any(c.isalpha() for c in passe))

def Email_valido(email): # Verifica se o email é seguro
    conexao = sqlite3.connect("database.db")
    cursor = conexao.cursor()
    cursor.execute("SELECT 1 FROM users WHERE email = ? LIMIT 1", (str(email),))
    # Procura na DB onde o email é aquele fornecido, caso não haja, return false
    resultado = cursor.fetchone()
    cursor.close()
    conexao.close()
    try:
        validate_email(email) # Verifica se é válido
        if not resultado: # Se ainda não tiver nada, não entra no if, 
            return True
    except EmailNotValidError: pass
    return False

def exist_user(user):
    conexao = sqlite3.connect("database.db")
    cursor = conexao.cursor()
    cursor.execute("SELECT 1 FROM users WHERE id = ? LIMIT 1", (str(user),))
    # Verifica se o user fornecido está na DB
    resultado = cursor.fetchone()
    if not resultado:
        return False
    cursor.close()
    conexao.close()
    return True

def add_user(novo_id, nova_hashpass, novo_email):
    conexao = sqlite3.connect("database.db")
    cursor = conexao.cursor()
    cursor.execute("""
        INSERT INTO users (id, hashpass, email)
        VALUES (?, ?, ?)
        """, (novo_id, nova_hashpass, novo_email))
    # Insere dentro de users, o ID, a Pass protegida, e o email
    conexao.commit()
    cursor.close()
    conexao.close()

def get(info):
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row # Não sei o que faz, mas ajuda a criar o dicionario com row
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM users WHERE id = ? LIMIT 1", (info,))
    row = cursor.fetchone()
    if row:
        return dict(row) 
    return None

def update_tips(id, tip):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE users SET tips = ? WHERE id = ?",
        (str(tip), str(id))
    )
    conn.commit()
    cursor.close()
    conn.close()


    

app.run(host="0.0.0.0", port=8000, debug=True)
