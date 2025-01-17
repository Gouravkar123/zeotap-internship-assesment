from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Sample data structure to hold spreadsheet data
spreadsheet_data = {}

@app.route('/')
def index():
    return render_template('index.html', data=spreadsheet_data)

@app.route('/update', methods=['POST'])
def update_cell():
    cell = request.json.get('cell')
    value = request.json.get('value')
    spreadsheet_data[cell] = value
    return jsonify(success=True)

@app.route('/calculate', methods=['POST'])
def calculate():
    function = request.json.get('function')
    range_cells = request.json.get('range')
    values = [float(spreadsheet_data.get(cell, 0)) for cell in range_cells]

    if function == 'SUM':
        result = sum(values)
    elif function == 'AVERAGE':
        result = sum(values) / len(values) if values else 0
    elif function == 'MAX':
        result = max(values) if values else 0
    elif function == 'MIN':
        result = min(values) if values else 0
    elif function == 'COUNT':
        result = len([v for v in values if v != 0])
    else:
        result = None

    return jsonify(result=result)

@app.route('/data_quality', methods=['POST'])
def data_quality():
    function = request.json.get('function')
    range_cells = request.json.get('range')
    result = []

    if function == 'TRIM':
        result = [spreadsheet_data[cell].strip() for cell in range_cells]
    elif function == 'UPPER':
        result = [spreadsheet_data[cell].upper() for cell in range_cells]
    elif function == 'LOWER':
        result = [spreadsheet_data[cell].lower() for cell in range_cells]
    elif function == 'REMOVE_DUPLICATES':
        seen = set()
        for cell in range_cells:
            if spreadsheet_data[cell] not in seen:
                seen.add(spreadsheet_data[cell])
                result.append(spreadsheet_data[cell])
    elif function == 'FIND_AND_REPLACE':
        find_text = request.json.get('find')
        replace_text = request.json.get('replace')
        for cell in range_cells:
            if find_text in spreadsheet_data[cell]:
                spreadsheet_data[cell] = spreadsheet_data[cell].replace(find_text, replace_text)
                result.append(spreadsheet_data[cell])

    return jsonify(result=result)

if __name__ == '__main__':
    app.run(debug=True)