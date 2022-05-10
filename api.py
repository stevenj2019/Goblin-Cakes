from flask import Flask, jsonify 
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS, cross_origin

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "mssql+pyodbc://localhost/test?driver=ODBC+Driver+17+for+SQL+Server"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config['CORS_HEADERS'] = "Content-Type"

db = SQLAlchemy(app)

def toJSON(inp):
    data = list()
    for entry in inp:
        data.append({
            'Name': entry.Product, 
            'Price': str(entry.Price_Per),
            'Units': str(entry.Units_Sold),
            'Profit': str(int(entry.Price_Per) * int(entry.Units_Sold))
        })
    return jsonify(data)

class GoblinCakeSales(db.Model):
    ID = db.Column(db.Integer, primary_key = True, nullable = False)
    Product = db.Column(db.String(max), nullable = False)
    Product_Type = db.Column(db.String(max), nullable = False)
    Price_Per = db.Column(db.Float, nullable = False)
    Units_Sold = db.Column(db.Integer, nullable = False)
    Quarter = db.Column(db.Integer, nullable = False)

@app.route('/quarters/<quarter>', methods=['GET'])
@cross_origin(origin="*", headers=['Content-Type', 'Authorization'])
def quaters(quarter):
    if quarter == '0':
        cakes = GoblinCakeSales.query.filter_by(Product_Type = "Cake").all()
    if quarter in ['1', '2', '3', '4']:
        cakes = GoblinCakeSales.query.filter_by(Product_Type = "Cake", Quarter = int(quarter))
    return toJSON(cakes)

app.run(debug=True, host='0.0.0.0')
