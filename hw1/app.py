from flask import Flask, render_template, request, jsonify
from qlearning import q_learning

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/square')
def square():
    n = int(request.args.get('n'))
    return render_template('square.html', n=n)

@app.route('/solve', methods=['POST'])
def solve():
    start = request.form.get('start')
    end = request.form.get('end')
    obstacles = request.form.getlist('obstacle')
    n = int(request.form.get('n'))
    #policy, q_values = q_learning(n, start, end, obstacles)
    #return render_template('solution.html', policy=policy, q_values=q_values)
    policy = [[0,0, 'right'], [0,1,'left'], [0,2,'down'],[1,2,'down']]
    q_values = [[-1,0,0,-1],[-1,0,0,0],[-1,-1,1,0],[0,-1,1,0],[-1,0,0,-1],[-1,0,0,0],[-1,-1,1,0],[0,-1,1,0],[0,-1,1,0]]


    return render_template('solution.html', policy=policy, q_values=q_values,n=n)
if __name__ == '__main__':
    app.run(debug=True)
