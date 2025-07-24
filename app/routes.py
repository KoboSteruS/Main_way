from flask import Blueprint, render_template

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
@main_bp.route('/<version>')
def index(version=None):
    return render_template('index.html', version=version or '1.0')

@main_bp.route('/test')
def test():
    return render_template('test.html')

@main_bp.route('/debug')
def debug():
    return "Debug route working" 