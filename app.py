from flask import *
import sqlite3
from subprocess import *
import pycurl
from io import BytesIO

app = Flask(__name__)
app.config["SECRET_KEY"]='secret12345' #the problem is here
db = sqlite3.connect("./database.db",check_same_thread=False)

@app.route("/")
def home():
    return render_template("home.html")

###########################################idor vuln##################################################################

@app.route("/idor")
def render_idor():
    return redirect("/idor/user/1")
@app.route("/idor/user/<int:id>")
def idor(id):
    cur = db.cursor()
    cur.execute("select * from users where id=?",str(id)) # problem is here
    data = cur.fetchone()
    cur.close()
    return render_template("idor.html",id=data[0],name=data[1],email=data[2],location=data[3])

########################################sql injection vuln###########################################################
@app.route('/sqli/get_user_info',methods=["GET","POST"])
def sqli():
    if request.method == "GET":
        return render_template("sqli.html")
    elif request.method == "POST":
        username = request.json["name"]
        cur = db.cursor()
        cur.execute(f"select * from users where name = '{username}'") #problem is in this line
        data = cur.fetchone()
        cur.close()
        if data:
            try:
                return jsonify({"id":data[0],"name":data[1],"email":data[2]})
            except:
                return "internal server error",500
        else:
            return jsonify({"id":"id not found","name":"user not found","email":"email not found"}),404
    else:
        pass

########################################cross site scripting vuln####################################################
@app.route("/xss/search",methods=["POST","GET"])
def xss():
    if request.method == "GET":
        return render_template("xss.html")
    elif request.method == "POST":
        name = request.json["searchTerm"]
        return jsonify({"name":name})
    else:
        pass

########################################server side template injection vuln##########################################

@app.route("/ssti/search")
def ssti():
    if request.method == "GET" and request.args.get("user"):
        template = """<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"><title>Admin Search Page</title><link rel="stylesheet" href="/static/temp.css"></head><body><div class="container"><h1>Admin Searching Page</h1><form action="/ssti/search" method="GET"><div class="search-bar"><input type="text" id="searchInput" name="user" placeholder="Enter your search name"><input type="submit" class="btn" value="Search"></div></form><div id="searchResults">{%if user%}<div class="result-item"><h3>You Searched About :</h3><p><strong>Name:</strong> """+request.args.get("user")+"""</p></div>{%endif%}</div></div></body></html>"""
        return render_template_string(template,user=request.args.get("user")) # problem is here
    else:
        return render_template("ssti.html")

########################################server side request forgery vuln##########################################

@app.route("/ssrf/fetch")
def ssrf():
    if request.method == "GET" and request.args.get('url'):
        url = request.args.get('url')
        try:
            buffer = BytesIO()
            c = pycurl.Curl()
            c.setopt(pycurl.URL, url) # problem is here
            c.setopt(pycurl.WRITEDATA, buffer)
            c.perform() # problem is here
            c.close()
            body = buffer.getvalue().decode('utf-8')
            return (body)
        except Exception as e:
            return str(e), 500
    else:
        return render_template("ssrf.html")

@app.route("/lfi/index")
def lfi():
    if request.method == "GET" and request.args.get('page'):
        page = request.args.get('page')
        return open("templates/lfi_files/"+page).read() # problem is here
    else:
        return render_template("lfi_files/dashboard.html")

########################################logic bug vuln##########################################

@app.route("/logic")
def logic():
    return render_template('logic.html')
@app.route("/logic/purchase",methods=["POST","GET"])
def purchase_logic():
    if request.method == "POST":
        quantity = int(request.form['quantity']) #problem is here
        price = float(request.form['price']) #problem is here
        total_cost = price * quantity
        return render_template('logic_purchase.html', quantity=quantity, total_cost=total_cost)
    return render_template('logic_purchase.html')


########################################weak secret_key session vuln##########################################

@app.route("/weaksession/profile")
def weaksession():
    if "user" not in session:
        session["user"] = 'user'
    return render_template("weaksession_profile.html",user=session["user"],email=session["user"]+"@teleworm.us",address="3453 Marietta Street Fremont, CA 94539")

########################################weak secret_key session vuln##########################################

@app.route("/rce/pingme",methods=["GET","POST"])
def rce():
    if request.method == "POST":
        url = str(request.form.get('url'))
        output = Popen(["ping -c 1 " + url],shell=True,stdout=PIPE , stderr=STDOUT).stdout.read().decode()
        return render_template("rce.html",response=output)
    return render_template("rce.html")


if __name__ == "__main__":
    app.run(debug=True,port=80,host='0.0.0.0')

#some resources :
#    elzero php security
#    dvwa src
#    snyk