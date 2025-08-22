from flask import Flask, render_template, request, redirect, url_for
import pymysql

app = Flask(__name__)

def get_db_connection():
    return pymysql.connect(
        host='localhost',
        user='root',
        password='',  # coloque sua senha aqui, se tiver
        db='protagonize'
    )

@app.route('/')
def index():
    conn = get_db_connection()
    with conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM estudantes")
            estudantes = cursor.fetchall()
            cursor.execute("SELECT * FROM instituicoes")
            instituicoes = cursor.fetchall()
    return render_template('index.html', estudantes=estudantes, instituicoes=instituicoes)

@app.route('/cadastrar_estudante', methods=['GET', 'POST'])
def cadastrar_estudante():
    if request.method == 'POST':
        nome = request.form['nome']
        cpf = request.form['cpf']
        email = request.form['email']
        telefone = request.form['telefone']
        idade = request.form['idade']
        endereco = request.form['endereco']
        conn = get_db_connection()
        with conn:
            with conn.cursor() as cursor:
                cursor.execute("INSERT INTO estudantes (nome, cpf,email,telefone,idade,endereco) VALUES (%s, %s, %s, %s,%s,%s)", 
                (nome, cpf,email,telefone,idade,endereco))
                conn.commit()
        return redirect(url_for('index'))
    return render_template('cadastrar_estudante.html')

@app.route('/cadastrar_instituicao', methods=['GET', 'POST'])
def cadastrar_instituicao():
    if request.method == 'POST':
        nome = request.form['nome']
        cnpj = request.form['cnpj']
        endereco = request.form ['endereco']
        telefone = request.form['telefone']
        descricao = request.form['descricao']
        senha = request.form['senha']
        conn = get_db_connection()
        with conn:
            with conn.cursor() as cursor:
                cursor.execute("INSERT INTO instituicoes (nome, cnpj, endereco, telefone, descricao, senha) VALUES (%s, %s, %s, %s, %s, %s)", 
                (nome,cnpj,endereco,telefone, descricao,senha))
                conn.commit()
        return redirect(url_for('index'))
    return render_template('cadastrar_instituicao.html')

# Rota de login agora é '/login'
@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    Rota de login.
    No POST, verifica as credenciais e, se corretas, busca os estudantes.
    """
    if request.method == 'POST':
        cnpj = request.form['login_acesso']
        senha = request.form['senha_acesso']
        conn = get_db_connection()
        
        # Conecta para verificar as credenciais
        with conn:
            with conn.cursor(pymysql.cursors.DictCursor) as cursor:
                query = "SELECT * FROM instituicoes WHERE cnpj = %s AND senha = %s"
                cursor.execute(query, (cnpj, senha))
                resultado = cursor.fetchone()

            if resultado:
                # Se o login for bem-sucedido, busca a lista de estudantes
                with conn.cursor(pymysql.cursors.DictCursor) as cursor:
                    cursor.execute("SELECT nome, endereco,idade FROM estudantes")
                    estudantes = cursor.fetchall()
                # Renderiza a página de login novamente, agora com os dados dos estudantes
                return render_template('login.html', estudantes=estudantes, sucesso="Login realizado com sucesso!")
            else:
                # Se o login falhar, retorna uma mensagem de erro
                return render_template('login.html', erro="CNPJ ou senha incorretos.")
    return render_template('login.html')

@app.route('/planos')
def planos():
    return render_template('planos.html', valor=1500, descricao=(
        "Ao aderir ao plano no valor de R$ 1.500,00, sua instituição 5 receberá voluntários capacitados "
        "para atuar diretamente na casa de acolhimento, além de acesso a conteúdos exclusivos e rede de apoio."
    ))
if __name__ == '__main__':
    app.run(debug=True)
