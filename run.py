from flask import render_template
from flasky import create_app
from flasky.config import ProductionConfig


app = create_app()


@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run()
