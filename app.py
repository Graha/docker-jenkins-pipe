from flask import Flask
app = Flask(__name__)


class MyClass(object):
    def __init__(self):
        self.message = 'Hello'
        return self  # Noncompliant
    

@app.route('/')
def get_home():
    return 'I m in RL'

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')
