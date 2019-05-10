from flask import Flask, render_template
from .forms import find_form
from .. import ConnectingFlights, Database
import os

app = Flask(__name__)
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY
db = Database('localhost', 27017, "connecting_flight")
cf = ConnectingFlights(db)

@app.route("/", methods=["GET", "POST"])
def index():
    form = find_form()
    dbresult = []
    result = []
    total = ""

    if (form.orig.data, form.dest.data, form.cri.data) != (None, None, None):
        cri = Database.Criterion[form.cri.data]
        search_orig = form.orig.data.split()[0].upper()
        search_dest = form.dest.data.split()[0].upper()
        dbresult = cf.get_shortest_floyd_warshal(cri, search_orig, search_dest)
        for flight in dbresult["path"]:
            orig = flight[0]
            dest = flight[1]
            weight = cf.get_str_from_cri(cri, flight[2])
            airline, no = flight[3]
            result.append({"orig": orig, "dest": dest, "weight": weight, 
                           "airline": airline, "no": no})
        total = cf.get_str_from_cri(cri, dbresult["total_weight"])
        print(result)
    return render_template("index.html", form=form, result=result, 
                           total=total)

def get_app():
    return app

if __name__ == "__main__":
    app.run()
