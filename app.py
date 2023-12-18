from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
import yaml
from agents import AlbumPlaylisterAgent, MoviePlaylisterAgent
from scrappers import Bs4Scrapper, SeleniumScrapper
#from worker import run_threaded, pause_job, resume_job, delete_job
import schedule

with open('config.yaml') as f:
    config = yaml.safe_load(f)

app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://playswap:admin@playswap-db.postgres.database.azure.com/agents'

db = SQLAlchemy(app)
migrate = Migrate(app, db)

class Agent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    run_each = db.Column(db.Integer)
    type = db.Column(db.String)
    scrapper = db.Column(db.String)
    llm_model = db.Column(db.String)
    active = db.Column(db.Boolean)
    job_name = db.Column(db.String, unique=True, nullable=True)
    language = db.Column(db.String)
    url = db.Column(db.String)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email= db.Column(db.String)
    playswap_token = db.Column(db.String)
    password = db.Column(db.String)
    agents = db.relationship('Agent', backref='user', lazy=True)


@app.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    new_user = User(email=data['email'], playswap_token=data['playswap_token'], password=data['password'])
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'New user created', 'user_id': new_user.id}), 201


@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data['email']
    password = data['password']
    user = User.query.filter_by(email=email).first()
    if user is None or password != user.password:
        return jsonify({'message': 'Invalid email or password'}), 401

    return jsonify({'user_id': user.id, 'playswap_token': user.playswap_token}), 200



@app.route('/agents', methods=['POST'])
def create_agent():
    data = request.get_json()
    user_id = data['user_id']  # assuming the user_id is passed in the request
    user = User.query.get_or_404(user_id)
    new_agent = Agent(user=user, run_each=data['run_each'], type=data['type'], active=True, language=data['language'], url=data['url'])
    db.session.add(new_agent)
    db.session.commit()
    job_name = f"agent_{new_agent.id}"
    new_agent.job_name = job_name
    db.session.commit()
    """
    # Schedule the job
    if new_agent.type == 'album':
        #job = schedule.every(new_agent.run_each).days.do(run_threaded, album_playlister_task, new_agent.url, user.playswap_token, new_agent.language)
        album_playlister_task(new_agent.url, user.playswap_token, new_agent.language)
    elif new_agent.type == 'movie':
        #job = schedule.every(new_agent.run_each).days.do(run_threaded, movie_playlister_task, new_agent.url, user.playswap_token, new_agent.language)
        pass
    """
    return jsonify({'message': 'Agent created successfully', 'job_name': job_name}), 201


@app.route('/agents/user/<int:user_id>', methods=['GET'])
def get_agents_by_user(user_id):
    agents = Agent.query.filter_by(user_id=user_id).all()
    output = [{'id': agent.id, 'run_each': agent.run_each, 'type': agent.type, 'language': agent.language, 'url': agent.url} for agent in agents]
    return jsonify(output)


@app.route('/agents/<int:agent_id>/run', methods=['POST'])
def run_agent(agent_id):
    data = request.get_json()
    agent = Agent.query.get_or_404(agent_id)
    user_id = data['user_id']  # assuming the user_id is passed in the request
    user = User.query.get_or_404(user_id)
    # Schedule the job
    if agent.type == 'album':
        #job = schedule.every(new_agent.run_each).days.do(run_threaded, album_playlister_task, new_agent.url, user.playswap_token, new_agent.language)
        album_playlister_task(agent.url, user.playswap_token, agent.language)
    elif agent.type == 'movie':
        #job = schedule.every(new_agent.run_each).days.do(run_threaded, movie_playlister_task, new_agent.url, user.playswap_token, new_agent.language)
        pass
    return jsonify("success"), 200

@app.route('/agents/<int:agent_id>/pause', methods=['POST'])
def pause_agent(agent_id):
    agent = Agent.query.get_or_404(agent_id)
    #pause_job(agent.job_name)
    agent.active = False
    db.session.commit()
    return jsonify({'message': 'Agent paused'}), 200

@app.route('/agents/<int:agent_id>/resume', methods=['POST'])
def resume_agent(agent_id):
    agent = Agent.query.get_or_404(agent_id)
    #resume_job(agent.job_name)
    agent.active = True
    db.session.commit()
    return jsonify({'message': 'Agent resumed'}), 200


@app.route('/agents/<int:id>', methods=['PUT'])
def update_agent(id):
    agent = Agent.query.get_or_404(id)
    data = request.get_json()
    if int(data['user_id']) != agent.user_id:
        return jsonify({'message': 'Unauthorized'}), 401
    agent.run_each = data['run_each']
    agent.type = data['type']
    agent.args = data['args']
    db.session.commit()
    return jsonify({'message': 'Agent updated successfully'})


@app.route('/agents/<int:id>', methods=['DELETE'])
def delete_agent(id):
    agent = Agent.query.get_or_404(id)
    #delete_job(agent.job_name)
    data = request.get_json()
    print(agent.user_id, data['user_id'])
    if int(data['user_id']) != agent.user_id:
        return jsonify({'message': 'Unauthorized'}), 401
    db.session.delete(agent)
    db.session.commit()
    return jsonify({'message': 'Agent deleted successfully'})


def album_playlister_task(url, playswap_token, language):
    scrapper = Bs4Scrapper(url)
    agent = AlbumPlaylisterAgent(scrapper, "gpt-3.5-turbo-1106", playswap_token, language=language, publish=True)
   
    agent.run()

def movie_playlister_task(url, playswap_token, language):
    scrapper = Bs4Scrapper(url)
    agent = MoviePlaylisterAgent(scrapper, "gpt-3.5-turbo-1106", playswap_token, language)
    agent.run()



if __name__ == '__main__':
    app.run(debug=True)
