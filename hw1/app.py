from flask import Flask, render_template, request, jsonify
from qlearning import q_learning
import random

app = Flask(__name__)
obstacles = []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/square')
def square():
    global obstacles
    n = int(request.args.get('n'))
    obstacles = random.sample([(i, j) for i in range(n) for j in range(n)], 3)
    return render_template('square.html', n=n, obstacles=obstacles)

@app.route('/solve', methods=['POST'])
def solve():
    global obstacles
    start = request.form.get('start')
    end = request.form.get('end')
    #obstacles = request.form.getlist('obstacle')
    n = int(request.form.get('n'))
    #policy, q_values = q_learning(n, start, end, obstacles)
    policy = [[0,0, 'right'], [0,1,'left'], [0,2,'down'],[1,2,'down']]
    q_values = [[-1,0,0,-1],[-1,0,0,0],[-1,-1,1,0],[0,-1,1,0],[-1,0,0,-1],[-1,0,0,0],[-1,-1,1,0],[0,-1,1,0],[0,-1,1,0]]


    return render_template('solution.html', policy=policy, q_values=q_values,n=n,start=start,end=end,obstacles=obstacles)
if __name__ == '__main__':
    app.run(debug=True)
