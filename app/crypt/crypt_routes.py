from . import crypt
from flask import  request, jsonify
import requests
from flask_jwt_extended import jwt_required


@crypt.route('/api/v3/markets/summaries', methods=['GET'])
# @jwt_required
def get_market_data():
    """
    Get all market summaries
    ---
    responses:
      200:
        description: Markets data received
    """
    response = requests.get('https://api.bittrex.com/v3/markets/summaries', verify=False)
    markets = response.json()
    return jsonify({'result': markets, 'message': 'markets data received'})


@crypt.route('/api/v3/markets/<symbol_type>/summary', methods=['GET'])
def get_market_summary(symbol_type):
    """
    Get market summary for a specific symbol
    ---
    parameters:
      - in: path
        name: symbol_type
        required: true
        type: string
        description: Symbol of the market
    responses:
      200:
        description: Market data received
    """
    try:
        response = requests.get('https://api.bittrex.com/v3/markets/' + symbol_type + '/summary', verify=False)
        market = response.json()
        return jsonify(market)
    except Exception as e:
        return jsonify({'msg': 'Error occurred'+str(e)})

get_market_summary = jwt_required(get_market_summary)
get_market_data = jwt_required(get_market_data)
