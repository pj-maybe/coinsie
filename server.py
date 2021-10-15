from flask import Flask, json, request

import server_func

testdata = [{"id": 1, "name": "testdata One"}, {"id": 2, "name": "testdata Two"}]

api = Flask(__name__)

@api.route('/testapi', methods=['GET'])
def testapi():
    print("called testapi!")
    return json.dumps(testdata)

@api.route('/init_demo', methods=['GET'])
def init_demo():
    print("called init_demo!")
    server_func.init_demo_calls()
    return "done"

@api.route('/add_owner', methods=['GET', 'POST'])
def add_owner():
    user_data = request.get_json()

    print("called add_owner!")
    r = server_func.add_demo_owner(user_data["usertype"], user_data["username"], user_data["user_lcoin"], user_data["user_ccoin"])
    return r.text

@api.route('/show_data', methods=['GET'])
def show_data():
    print("called show_data!")
    r = server_func.show_whole_data()
    return r

@api.route('/get_holdings', methods=['GET'])
def get_holdings():
    print("called get_holdings!")
    r = server_func.get_holdings()    
    return r

@api.route('/transfer_cap2', methods=['GET', 'POST'])
def transfer_cap2():
    user_data = request.get_json()
    print("called transfer_cap2!")
    r = server_func.transfer_cap2(user_data["username_from"], user_data["username_to"], user_data["shapename"], user_data["color"], user_data["amount"])    
    return r.text

if __name__ == '__main__':
    api.run() 