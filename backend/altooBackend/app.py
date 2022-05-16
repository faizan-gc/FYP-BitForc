from flask import Flask, send_from_directory, request, jsonify
from flask_restful import Api, Resource, reqparse
from flask_cors import CORS #comment this on deployment
import sqlite3
import openai
from ilm_predict import *
from prompt_gpt import *


# conn = sqlite3.connect('database.db')
# conn.execute('CREATE TABLE listings (email TEXT, title TEXT, description TEXT, features TEXT)')

# conn.execute("INSERT INTO studentss (name,addr,city,pin) VALUES (?,?,?,?)",("alt","shk","hyd","123") )
# conn.commit()
# conn.close()

app = Flask(__name__)
CORS(app) #comment this on deployment
api = Api(app)

@app.route('/gendesc', methods = ['GET'])
def generate_description():
    
    args = request.args
    title = args['title'] + "\n\n###\n\n"

    description = openai.Completion.create(
    api_key="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",
    model="curie:ft-beacon-career-services-2022-04-27-00-29-18",
    prompt=title,
    stop = "\n\n###\n\n",
    max_tokens = 256
    )

    desc_text = description["choices"][0]["text"]

    return jsonify(desc_text)

    return jsonify("This is the returned generated desscription from openAI which has high BLEU, BERT and diversity scores. This is the returned generated desscription from openAI which has high BLEU, BERT and diversity scores. This is the returned generated desscription from openAI which has high BLEU, BERT and diversity scores. This is the returned generated desscription from openAI which has high BLEU, BERT and diversity scores.")


@app.route('/gentitle', methods = ['GET'])
def generate_title():
    
    args = request.args
    keywords = args['keywords']

    keywords_lst = keywords.split(",")

    model_input = "".join(keywords_lst)

    model_output = generate(model_input)
    
    return jsonify(model_output)

    return jsonify("Title")


@app.route('/genfeatures', methods = ['POST'])
def generate_features():
    
    args = request.args
    title = args['title']
    keywords = request.json

    keywords_lst = [i["trait_type"] for i in keywords]
    generated_features = list()

    for i in keywords_lst:
        prompt = "[" + title + "]" + "[" + i + "]"
        feature = get_feature(prompt)
        generated_features.append(feature)
  

    return jsonify(generated_features)

    return jsonify(["First feature is this.", "Second feature is this."])


@app.route('/create', methods = ['POST'])
def create_user():
    conn = sqlite3.connect('database.db')

    user_data = request.json
    name = user_data["name"]
    email = user_data["email"]
    password = user_data["password"]

    conn.execute("INSERT INTO sellers (name,email,password) VALUES (?,?,?)",(name, email, password) )
    conn.commit()
    
    conn.close()
    return jsonify("Successfully Created")


@app.route('/login', methods = ['POST'])
def login_user():
    conn = sqlite3.connect('database.db')

    user_data = request.json
    email = user_data["email"]
    password = user_data["password"]

    curr = conn.cursor()
    curr.execute(f"Select * from sellers where email = ?", (email,))
    
    rows = curr.fetchall()

    if (len(rows) == 0):
        conn.close()
        return jsonify("Failed")

    if(rows[0][2] != password):
        conn.close()
        return jsonify("Failed")

    
    
    conn.close()
    return jsonify(rows[0])


@app.route('/savelisting', methods = ['POST'])
def save_listing():
    conn = sqlite3.connect('database.db')

    data = request.json
    email = data["email"]
    title = data["title"]
    description = data["description"]
    features = data["features"]
    
    conn.execute("INSERT INTO listings (email,title,description,features) VALUES (?,?,?,?)",(email,title,description,features) )

    conn.commit()
    conn.close()

    return jsonify("Success")


@app.route('/getlisting', methods = ['POST'])
def get_listings():
    conn = sqlite3.connect('database.db')

    data = request.json
    email = data["email"]

    curr = conn.cursor()
    curr.execute(f"Select * from listings where email = ?", (email,))
    
    rows = curr.fetchall()
    
    conn.close()


    return jsonify(rows)