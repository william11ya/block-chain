from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

ID=""

@app.route('/index')
def index():
    global ID
    return render_template('test_view/index.html',text=ID)

@app.route('/index',methods=['POST'])
def index_login():
    global ID
    ID=request.form['ID']
    return redirect(url_for('success', name=ID, action="post"))

@app.route('/success/<action>/<name>')
def success(name, action):
    return render_template('test_view/index.html',text=name)

@app.route('/manage_users')
def manage_users():
    global ID
    return render_template('test_view/manage-users.html',text=ID)

@app.route('/preferences')
def preferences():
    global ID
    return render_template('test_view/preferences.html',text=ID)

@app.route('/')
@app.route('/login')
def login():
    return render_template('test_view/login.html')

@app.route('/add_vote1')
def add_vote1():
    global ID
    return render_template('test_view/add_vote1.html',text=ID)

@app.route('/add_vote2')
def add_vote2():
    global ID
    return render_template('test_view/add_vote2.html',text=ID)

@app.route('/add_vote2',methods=['POST','GET'])
def add_vote2_data():
    global ID
    if request.method == "POST":
        global vote_content
        global vote_count
        
        vote_name=request.form['vote_name']
        vote_count=request.form['vote_count']
        startdate=request.form['startdate']
        enddate=request.form['enddate']
        starttime=request.form['starttime']
        endtime=request.form['endtime']
    
        vote_content={
            'Vote_Name': vote_name,
            'Vote_Count': vote_count,
            'Start_Date': startdate,
            'End_Date': enddate,
            'Start_Time': starttime,
            'End_Time': endtime
        }

        global vote_people
        vote_people={}
        for i in range(int(vote_count)):
            num=i+1
            name="name"+str(num)
            vote_people[name]=""

        return render_template('test_view/add_vote2.html', content=vote_content,text=ID,vote_people=vote_people)
    else:
        return render_template('test_view/add_vote2.html',text=ID)
    
@app.route('/add_vote1',methods=['POST','GET'])
def add_vote2_people():
    global ID
    if request.method == "POST":
        global vote_people
        global vote_count
        
        name_array=[]
        for i in range(int(vote_count)):
            num=i+1
            name="name"+str(num)
            vote_people[name]=request.form[name]
            name_array.append(request.form[name])

        return render_template('test_view/add_vote1.html',text=ID)
    else:
        return render_template('test_view/add_vote1.html',text=ID)

@app.route('/student_vote')
def student_vote():
    global ID
    return render_template('test_view/student_vote.html',text=ID)

@app.route('/manage_users',methods=['POST','GET'])
def student_vote2():
    global ID
    return render_template('test_view/manage-users.html',text=ID)

#----------------------------------------------------------------------

if __name__ == '__main__':
    app.debug = True
    app.run(host="0.0.0.0",port=5000)
