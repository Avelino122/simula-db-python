from flask import Flask, request, render_template_string

app = Flask(__name__)

class SimpleDB:
    def __init__(self):
        self.db = []  

    def insert(self, data):
        self.db.append(data)

    def search(self, query):
        return [record for record in self.db if query(record)]

db = SimpleDB()

@app.route('/', methods=['GET', 'POST'])
def home():
    results = []
    if request.method == 'POST':
        if 'nome' in request.form:  # Verifica se estamos no formulário de inserção
            nome = request.form['nome']
            idade = request.form['idade']
            email = request.form['email']
            db.insert({'nome': nome, 'idade': int(idade), 'email': email})
        elif 'idade_search' in request.form:  # Verifica se estamos no formulário de busca
            idade = int(request.form['idade_search'])
            results = db.search(lambda user: user['idade'] == idade)
    
    return render_template_string('''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Formulário | Thierry </title>
        <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
        <link href="https://fonts.googleapis.com/css?family=Fjalla+One&display=swap" rel="stylesheet">
        <script src="https://code.jquery.com/jquery-3.5.1.slim.min.js"></script>
        <script src="https://cdn.jsdelivr.net/npm/@popperjs/core@2.9.9/dist/umd/popper.min.js"></script>
        <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/js/bootstrap.min.js"></script>
    </head>
        <style>
        body {
            background: url('https://s3-us-west-2.amazonaws.com/s.cdpn.io/38816/image-from-rawpixel-id-2210775-jpeg.jpg') center center no-repeat;
            background-size: cover;
            width: 100vw;
            height: 100vh;
            display: grid;
            align-items: center;
            justify-items: center;
            margin: 0;
            padding: 0;
            font-family: 'Fjalla One', sans-serif;
            color: #2A293E;
        }
        .form-group input, .form-group button {
            display: block;
            width: 100%;
            font-size: 14pt;
            line-height: 28pt;
            font-family: 'Fjalla One', sans-serif;
            margin-bottom: 28pt;
            border: none;
            border-bottom: 5px solid rgba(0,0,0,1);
            background: #f8f4e5;
            padding-left: 5px;
            outline: none;
            color: rgba(0,0,0,1);
        }
        .form-group input:focus {
            border-bottom: 5px solid #ffa580;
        }
        button {
            display: block;
            margin: 0 auto;
            line-height: 28pt;
            padding: 0 20px;
            background: #ffa580;
            letter-spacing: 2px;
            transition: .2s all ease-in-out;
            outline: none;
            border: 1px solid rgba(0,0,0,1);
            box-shadow: 3px 3px 1px #95a4ff, 3px 3px 1px 2px rgba(0,0,0,1);
            color: #2A293E;
            cursor: pointer;
        }
        button:hover {
            background: rgba(0,0,0,1);
            color: white;
        }
    </style>
</head>
<body>
    <div class="container">
        <form method="post" class="mb-3">
            <div class="form-group">
                <label for="nome">Nome:</label>
                <input type="text" name="nome" id="nome" required>
            </div>
            <div class="form-group">
                <label for="idade">Idade:</label>
                <input type="number" name="idade" id="idade" required>
            </div>
            <div class="form-group">
                <label for="email">Email:</label>
                <input type="email" name="email" id="email" required>
            </div>
            <button type="submit">Inserir</button>
        </form>
                    <h2>Buscar Usuário por Idade</h2>
        <form method="post" class="mb-3">
            <div class="form-group">
                <label for="idade_search">Idade:</label>
                <input type="number" class="form-control" name="idade_search" id="idade_search" required>
            </div>
            <button type="submit" >Buscar</button>
        </form> 
        </div>

        <!-- Modal -->
        <div class="modal" id="searchModal" tabindex="-1" role="dialog">
            <div class="modal-dialog" role="document">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title">Resultados da Busca</h5>
                        <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                            <span aria-hidden="true">&times;</span>
                        </button>
                    </div>
                    <div class="modal-body">
                        {% if results %}
                            {% for user in results %}
                                <p>Nome: {{ user['nome'] }}, Idade: {{ user['idade'] }}, Email: {{ user['email'] }}</p>
                            {% endfor %}
                        {% else %}
                            <p>Nenhum usuário encontrado.</p>
                        {% endif %}
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-secondary" data-dismiss="modal">Fechar</button>
                    </div>
                </div>
            </div>
        </div>

        {% if results %}
            <script>
                $(document).ready(function(){
                    $('#searchModal').modal('show');
                });
            </script>
        {% endif %}
    </body>
    </html>
    ''', results=results)

if __name__ == '__main__':
    app.run(debug=True)
