from flask import render_template, Blueprint

routes_blueprint = Blueprint('routes', __name__)

@routes_blueprint.route("/")
def hello_world():
    return render_template("index.html")
