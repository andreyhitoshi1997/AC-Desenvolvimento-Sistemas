from flask import Flask, render_template
from flask_restful import Api
from resources.vendedores import Vendedor, Vendedores
from resources.usuario import User, UserRegister,  UserLogin




app = Flask(__name__, template_folder='templates')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///banco.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
api = Api(app)



@app.before_first_request
def cria_banco():
    banco.create_all()


@app.route('/cadastro')
def inicio():
    return render_template('cadastro_vendedores.html')


api.add_resource(Vendedores, '/vendedores')
api.add_resource(Vendedor, '/vendedores/<int:id_vendedor>')
api.add_resource(User, '/usuarios/<int:id_usuario>')
api.add_resource(UserRegister, '/cadastro')
api.add_resource(UserLogin, '/login')


if __name__ == '__main__':
    from sql_alchemy import banco
    banco.init_app(app)
    app.run(debug=True)
