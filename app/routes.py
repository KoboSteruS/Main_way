from flask import Blueprint, render_template

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    return render_template('index.html')

@main_bp.route('/test')
def test():
    return render_template('test.html')

@main_bp.route('/debug')
def debug():
    return "Debug route working" 