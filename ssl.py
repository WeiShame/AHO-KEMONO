from flask import Flask, send_from_directory
server = Flask(__name__)
@server.route('/.well-known/pki-validation/<filename>')
def ssl(filename):
    return send_from_directory("data",filename,as_attachment=True)


if __name__=="__main__":
    server.run("0.0.0.0", 80)