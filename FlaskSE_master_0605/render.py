import array
import time
from flask import Flask, render_template, request, redirect, url_for
import json
from web3 import Web3
import datetime

w3 = Web3(Web3.HTTPProvider('HTTP://172.20.224.1:7545'))

w3.eth.default_account = w3.eth.accounts[0]

compiled_contract_path = '/home/william11ya/IPad/block-chain/build/contracts/VotingSystem.json'

deployed_contract_address = '0x4F3859C14be08c0274739D589Dcb9C4B970B42E2'

with open(compiled_contract_path) as file:
    contract_json = json.load(file)
    contract_abi = contract_json['abi']

contract = w3.eth.contract(
    address = deployed_contract_address, abi = contract_abi)

def CreateVote(voteName, candidateNames, endTime):
    Create = contract.functions.CreateVote(voteName, candidateNames, endTime).transact()
    runCreate = w3.eth.wait_for_transaction_receipt(Create)

def getVoteIndex(voteName):
    exist = contract.functions.getVoteIndex(voteName).call()
    return exist

def settle(voteId):
    Settle = contract.functions.settle(voteId).call()
    return Settle

def getAllRunningVote():
    get = contract.functions.getAllRunningVote().call()
    return get

def getAllCandidateName(voteId):
    get = contract.functions.getAllCandidatesName(voteId).call()
    return get

def getEndTime(voteId):
    get = contract.functions.getEndTime(voteId).call()
    return get

def vote(voteId, candidateIndex):
    votecandidate = contract.functions.vote(voteId, candidateIndex).transact()
    runvotecandidate = w3.eth.wait_for_transaction_receipt(votecandidate)

def speedTime(voteId):
    speed = contract.functions.speedTimeForTestingOnly(voteId).transact()
    runspeed = w3.eth.wait_for_transaction_receipt(speed)

def getVoteInfo():
    a = []
    Name = contract.functions.getAllRunningVote().call()
    for x in Name:
        temp = []
        index = contract.functions.getVoteIndex(x).call()
        time = contract.functions.getEndTime(index).call()
        temp = [index,x,time]
        a.append(temp)
    print(a)
    return a

def getAllEndVote():
    get = contract.functions.getAllEndedVote().call()
    return get

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
    info = getVoteInfo()
    now = int(time.time())
    for x in info:
        if x[2] != 0 and x[2] <= now:
            speedTime(int(x[0]))
            print(x[0])

    Vote = getAllRunningVote()
    print(Vote)
    info = getVoteInfo()
    now = int(time.time())
    VoteInfo = []
    for x in info:
        temp = datetime.datetime.fromtimestamp(x[2])
        dt = datetime.datetime.strptime(str(temp), '%Y-%m-%d %H:%M:%S')
        dtt = str(dt).split(' ')
        x[2] = (dtt[0])
        x.append(dtt[1])
        VoteInfo.append(x)
    print(VoteInfo)
    return render_template('test_view/manage-users.html', text=ID, VoteInfo = info)

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
        enddate=request.form['enddate']
        endtime=request.form['endtime']
    
        vote_content={
            'Vote_Name': vote_name,
            'Vote_Count': vote_count,
            'End_Date': enddate,
            'End_Time': endtime
        }

        global vote_people
        vote_people={}
        for i in range(int(vote_count)):
            num=i+1
            name="name"+str(num)
            vote_people[name]=""
        
        endtime = str(vote_content['End_Date']+ ' ' +vote_content['End_Time'])
        epoch = datetime.datetime.strptime(str(endtime), '%Y-%m-%d %H:%M').timestamp() - time.time()
        print(int(epoch))

        return render_template('test_view/add_vote2.html', content=vote_content,text=ID,vote_people=vote_people)
    else:
        return render_template('test_view/add_vote2.html',text=ID)
    
@app.route('/add_vote1',methods=['POST','GET'])
def add_vote2_people():
    global ID
    if request.method == "POST":
        global vote_people
        global vote_count
        global vote_content

        name_array=[]
        for i in range(int(vote_count)):
            num=i+1
            name="name"+str(num)
            vote_people[name]=request.form[name]
            name_array.append(request.form[name])
        
        endtime = str(vote_content['End_Date']+ ' ' +vote_content['End_Time'])
        epoch = datetime.datetime.strptime(str(endtime), '%Y-%m-%d %H:%M').timestamp() - time.time()
        print(epoch)
        CreateVote(vote_content["Vote_Name"],name_array,int(epoch))
        
        return render_template('test_view/add_vote1.html',text=ID)
    else:
        return render_template('test_view/add_vote1.html',text=ID)

@app.route('/student_vote/<index>') 
def student_vote(index):
    global ID
    #Index = getVoteIndex("ww")
    candidate = getAllCandidateName(int(index))
    print(index)
    print(candidate)
    Name = contract.functions.getVoteName(int(index)).call()
    print(Name)
    return render_template('test_view/student_vote.html',text=ID ,candidate = candidate ,index = index, VoteName = Name)

@app.route('/manage_users',methods=['POST','GET'])
def student_vote2():
    global ID
    index=request.form['index']
    voteOptions=request.form['voteOptions']
    VoteCheck = 0
    w3.eth.default_account = w3.eth.accounts[1]
    try:
        vote(index,voteOptions)
    except:
        print("You hava already vote.")
        VoteCheck = 1
    w3.eth.default_account = w3.eth.accounts[0]
    
    return render_template('test_view/manage-users.html', text=ID, VoteCheck = VoteCheck)

@app.route('/winner_candidate')
def winner_candidate():
    global ID

    info = getVoteInfo()
    now = time.time()
    endVote = []
    for x in info:
        if x[2] != 0 and x[2] <= now:
            speedTime(x[0])
    
    temp = getAllEndVote()
    for x in temp:
        name = contract.functions.getVoteName(x).call()
        winner = settle(x)
        endVote.append([x,name,winner])        

    return render_template('/test_view/winner_candidate.html', text = ID ,endVote = endVote)

#----------------------------------------------------------------------

if __name__ == '__main__':
    app.debug = True
    app.run(host="0.0.0.0",port=5000, debug = True)
