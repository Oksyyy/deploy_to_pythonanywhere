# Program to manage service providers and their services using Flask
# Author: Oksana Abrosimova

from flask import Flask, request, jsonify, render_template
from pa import serviceProviderDAO

app = Flask(__name__)

@app.route('/')
def index():
       return render_template("index.html")

# PROVIDERS

# Get all
# curl http://127.0.0.1:5000/providers

@app.route('/providers', methods=['GET'])
def get_providers():
        return jsonify(serviceProviderDAO.get_all())

# Find by id
# curl http://127.0.0.1:5000/providers/6

@app.route('/providers/<int:id>', methods=['GET'])
def provider_by_id(id):
        provider = serviceProviderDAO.find_by_id(id)
        if provider is None:
                return jsonify({"error": "Provider not found"}), 404

        return jsonify(provider)

# Create
# curl -X POST http://127.0.0.1:5000/providers \-H "Content-Type: application/json" \-d '{"name":"Elaine","email":"elaine_mn@tgmail.com","phone":"086","price_per_hour":47,"service_id":2}'
@app.route('/providers', methods=['POST'])
def create_provider():
        return jsonify(serviceProviderDAO.create_provider(request.json))

# Update
# curl -X PUT http://127.0.0.1:5000/providers/2 \-H "Content-Type: application/json" \-d '{"name":"Jack","email":"some_jack@gmail.com","phone":"123","price_per_hour":61,"service_id":1}'

@app.route('/providers/<int:id>', methods=['PUT'])
def update_provider(id):
        jsonstring = request.json
        existing_provider = serviceProviderDAO.find_by_id(id)
        if existing_provider is None:
                return jsonify({"error": "Provider not found"}), 404

        serviceProviderDAO.update_provider(id, jsonstring)
        return jsonify({"message": "updated"})

# Delete
# curl -X DELETE http://127.0.0.1:5000/providers/1

@app.route('/providers/<int:id>', methods=['DELETE'])
def delete_provider(id):
        existing = serviceProviderDAO.find_by_id(id)
        if existing is None:
                return jsonify({"error": "Provider not found"}), 404

        serviceProviderDAO.delete_provider(id)
        return jsonify({"message": "deleted"})

# SERVICES

# Get all services
# curl http://127.0.0.1:5000/services

@app.route('/services', methods=['GET'])
def get_services():
        return jsonify(serviceProviderDAO.get_all_services())

# Create a service
# curl -X POST http://127.0.0.1:5000/services \-H "Content-Type: application/json" \-d '{"name":"Painting","service_id":2}'
@app.route('/services', methods=['POST'])
def create_service():
        return jsonify(serviceProviderDAO.create_service(request.json))

# Get service and service providers
# curl http://127.0.0.1:5000/providers/service/2
@app.route('/providers/service/<int:service_id>', methods=['GET'])
def get_by_service(service_id):
        return jsonify(serviceProviderDAO.get_by_service(service_id))


if __name__ == "__main__":
        app.run(debug=True, threaded=False)