from flask import Flask, url_for, request
import socket
app = Flask(__name__)

project = ""
type_ = ""
person = ""


@app.route("/welcome")
def index():
    return '''
        <html>
            <div>
            <h1>CNC-Commander V0.1</h1>
            </div>
            <div><hr /></div>
            <div>
            <h4>Log dich ein um die CNC-Fr&auml;se freizuschalten:</h4>
            </div>
            <div><form action="http://bbctrl.local:1337/login" method="POST">
            <h4>Name: <input name="name" type="text" /></h4>
            <h4>Projekttyp:&nbsp;<select name="usage_type">
            <option value="Privat">Privat</option>
            <option value="Gewerblich">Gewerblich</option>
            <option value="Vereinsprojekt">Vereinsprojekt</option>
            </select></h4>
            <p><input type="submit" value="           ENTER             " /></p>
            </form></div>
        </html>
    '''

@app.route("/login",methods=['POST'])
def login():
    name = request.form['name']
    usage_type = request.form['usage_type']
    f=open("/home/bbmc/cnc-commander/user.log",'a+')
    f.write("\n"+"USER: " + "\t" + name +"\t"+usage_type+"\n")
    f.close()
    return '''
        <html>
            <p><a href="#control" target="_blank" rel="noopener">Weiter zur CNC-Steuerung</a></p>
        </html>
    '''

if __name__ == "__main__":
    app.run(port = 1337,debug = True,host = 'bbctrl.local') #debug = True, host = '0.0.0.0',port = 1337

