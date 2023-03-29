from flask import Flask, render_template, request, jsonify
from qlearning3 import q_learning
import random
import numpy as np


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

    # 生成一個 n*n 的空字串陣列
    grid = [['' for j in range(n)] for i in range(n)]
    # 將 obstacles 中的位置標記為 'obstacle'
    for obstacle in obstacles:
        i, j = obstacle
        grid[i][j] = 'obstacle'

    new_start = [int(start[0]),int(start[2])]
    new_end = [int(end[0]),int(end[2])]
    policy, q_values = q_learning(grid, new_start, new_end)

    #policy = [[0,0, 'right'], [0,1,'right'], [0,2,'down'],[1,2,'down']]
    #q_values = [[-1,0,0,-1],[-1,0,0,0],[-1,-1,1,0],[0,-1,1,0],[-1,0,0,-1],[-1,0,0,0],[-1,-1,1,0],[0,-1,1,0],[0,-1,1,0]]
    return render_template('solution.html', policy=policy, q_values=q_values,n=n,start=new_start,end=new_end,obstacles=obstacles,grid = grid)
@app.route('/test')
def test():
    start = (0,0)
    end = (2,2)
    policy = [[0,0, 'right'], [0,1,'right'], [0,2,'down'],[1,2,'down']]
    return render_template("test.html", policy=policy,start=start,end=end)
if __name__ == '__main__':
    app.run(debug=True)
