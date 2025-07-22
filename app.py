from flask import Flask, request, jsonify
from agent_sdk import Agentforce, AgentUtils
from agent_sdk.models.agent import Agent
from agent_sdk.models.topic import Topic
from agent_sdk.models.action import Action
from agent_sdk.models.input import Input
from agent_sdk.models.output import Output
from agent_sdk.models.system_message import SystemMessage
from agent_sdk.models.variable import Variable
from agent_sdk.core.auth import BasicAuth

app = Flask(__name__)

@app.route('/create_agent', methods=['POST'])
def create_agent():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'error': 'Username and password required'}), 400

    try:
        auth = BasicAuth(username=username, password=password)
        agentforce = Agentforce(auth=auth)

        action = Action(
            name="findOrder sdk",
            description="Find order details using an order ID",
            inputs=[
                Input(
                    name="orderID",
                    description="Order identification number",
                    data_type="string",
                )
            ],
            outputs=[
                Output(
                    name="orderDetails", description="Details of the order", data_type="object"
                )
            ],
        )

        topic = Topic(
            name="Order Management test",
            description="Handles all user requests related to finding and managing orders",
            scope="public",
            instructions=[
                "If a user cannot find their order, attempt to locate it using the order ID",
                "If a user wants to check the status of their order, retrieve the order details",
            ],
            actions=[action],
        )

        agent = Agent(
            name="SDK Agent",
            description="An agent created programmatically for order management",
            agent_type="External",
            agent_template_type="EinsteinServiceAgent",
            company_name="Example Corp",
            sample_utterances=["What's the status of my order?", "I need to find my order"],
            system_messages=[
                SystemMessage(message="Welcome to Order Management!", msg_type="welcome"),
                SystemMessage(message="I'm sorry, I encountered an error.", msg_type="error"),
            ],
            variables=[
                Variable(
                    name="apiKey",
                    data_type="string",
                    var_type="conversation",
                    visibility="Internal",
                    developer_name="apiKey",
                    label="API Key"
                )
            ],
            topics=[topic],
        )

        result = agentforce.create(agent)
        return jsonify({"status": "success", "message": "Agent created successfully", "result": str(result)})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/', methods=['GET'])
def root():
    return jsonify({"status": "success", "message": "API is running"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True) 