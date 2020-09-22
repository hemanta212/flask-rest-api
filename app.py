from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    # get data as dict from the database
    data =[
            {
            'url' : 'https://github.com/hemanta212.png',
            'title' : 'title 3',
            'description' : '',
            },
            {
            'url' : 'https://github.com/hemanta212.png',
            'title' : 'title2',
            'description' : 'abc',
            },
            {
            'url' : 'https://github.com/hemanta212.png',
            'title' : 'Yestai t honi boro',
            'description' : None,
            },
            {
            'url' : 'https://github.com/hemanta212.png',
            'title' : 'Yestai t honi boro',
            'description' : """            'url' : 'https://github.com/hemanta212.png',
            'title' : 'Yestai t honi boro',
            'description' : """,
            },
    ]
    return data

@app.route('/post')
def post():
    pass


if __name__ == '__main__':
    app.run(debug=True)
