from flask import Blueprint
from flask_restx import Api, Resource, fields
from models import StateData

blueprint = Blueprint('api', __name__)
api = Api(blueprint)

state_data_model = api.model("State Data", {
    "month_name": fields.String,
    "Qindex": fields.Integer
})


@api.route("/StateData/<string:state>")
class StateDataAPI(Resource):
    
    @api.marshal_with(state_data_model,  envelope='data')
    def get(self, state):
        """State Data
        Returns monthly QIndex data for a given state
        """
        state_data = StateData()
        data = state_data.get_QIndex(state)
        return data

state_count_model = api.model("State Count", {
    "state_name": fields.String,
    "count": fields.Integer
})

@api.route("/StateCount")
class StateCountAPI(Resource):
    
    @api.marshal_with(state_count_model,  envelope='data')
    def get(self):
        """State Count
        Returns the count of records for each state
        """
        state_data = StateData()
        data = state_data.state_count()
        return [{"state_name": row[0], "count": row[1]} for row in data]

graph_data_model = api.model("Graph Data", {
    "x_value": fields.String,
    "y_value": fields.Float
})

@api.route("/graph")
class GraphAPI(Resource):
    
    @api.marshal_with(graph_data_model,  envelope='data')
    def get(self):
        """Graph Data
        Returns the last 7 days of graph data
        """
        state_data = StateData()
        data = state_data.get_graph()
        results = [{"x_value": row[0], "y_value": row[1]} for row in data]
        return results
        
wave_data_model = api.model("Wave Data", {
    "x_value": fields.String,
    "y_value": fields.Float
})

@api.route("/wave")
class GraphAPI(Resource):
    
    @api.marshal_with(wave_data_model,  envelope='data')
    def get(self):
        """Graph Data
        Returns the last 7 days of graph data
        """
        state_data = StateData()
        data = state_data.get_wave()
        results = [{"x_value": row[0], "y_value": row[1]} for row in data]
        return results        

