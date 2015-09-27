from flask import Flask, render_template, url_for, request, jsonify
from SPARQLWrapper import SPARQLWrapper, RDF, JSON
import requests
import json

app = Flask(__name__)

@app.route('/')
def main():
    app.logger.debug('Loading %s' % (url_for('main')))
    return render_template('index.html')

@app.route('/sparql', methods=['GET'])
def sparql():
    app.logger.debug('You arrived at ' + url_for('sparql'))
    app.logger.debug('I received the following arguments' + str(request.args) )

    endpoint = request.args.get('endpoint', None)
    query = request.args.get('query', None)
    reasoning = request.args.get('reasoning', None)

    return_format = request.args.get('format','JSON')

    if endpoint and query :
        sparql = SPARQLWrapper(endpoint)

        sparql.setQuery(query)

        if return_format == 'RDF':
            sparql.setReturnFormat(RDF)
        else :
            sparql.setReturnFormat(JSON)
            sparql.addParameter('Accept','application/sparql-results+json')

        sparql.addParameter('reasoning', reasoning)

        app.logger.debug('Query:\n{}'.format(query))

        app.logger.debug('Querying endpoint {}'.format(endpoint))


        try :
            response = sparql.query().convert()
            app.logger.debug('Results were returned, yay!')

            if len(response['results']['bindings']) == 0:
                app.logger.debug('No results')
                return jsonify({'result': 'None'})
            elif return_format == 'RDF':
                app.logger.debug('Serializing to Turtle format')
                return response.serialize(format='nt')
            else :
                app.logger.debug('Directly returning JSON format')
                return jsonify(response)
        except Exception as e:
            app.logger.error('Something went wrong')
            app.logger.error(e)
            return jsonify({'result': 'Error'})

    else :
        return jsonify({'result': 'Error'})

if __name__ == '__main__':
    app.run(debug=True)
