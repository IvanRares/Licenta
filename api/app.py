from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from werkzeug.utils import secure_filename
import os
import sys
import matplotlib.pyplot as plt
import numpy as np
import base64

app = Flask(__name__)
CORS(app)

def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")

def run_script(script, transmission_rate, mortality_rate, incubation_period):
    original_cwd = os.getcwd()
    
    script_dir = os.path.dirname(script)
    script_parent_dir = os.path.dirname(script_dir)
    os.chdir(script_dir)
    
    try:
        sys.path.append(script_parent_dir)
        
        with open(script, 'r') as script_file:
            script_contents = script_file.read()
        scripts_globals = {
            "output_image_paths": [],
            "script_dir": script_dir,
            "sys": sys,
            "mortality_rate": mortality_rate,
            "transmission_rate": transmission_rate,
            "incubation_period": 1 / incubation_period
        }
        
        exec(script_contents, scripts_globals)
        
        image_paths = scripts_globals["output_image_paths"]
        
        encoded_images = [encode_image(image_path) for image_path in image_paths]
        
        os.chdir(original_cwd)
        
        return jsonify({'success': True, 'images': encoded_images})
    except Exception as e:
        os.chdir(original_cwd)
        return jsonify({'success': False, 'error': str(e)}), 400



        
        
@app.route('/api/run_draw_map', methods=['POST'])
def run_draw_map():
    data = request.get_json()
    country = data.get('country')
    transmission_rate = data.get('transmissionRate')
    mortality_rate = data.get('mortalityRate')
    incubation_period = data.get('incubationPeriod')
    
    script_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), f'{country.lower()}', 'draw_map.py')
    
    return run_script(script_path,transmission_rate, mortality_rate, incubation_period)
    
@app.route('/api/run_plots', methods=['POST'])
def run_plots():
    data = request.get_json()
    country = data.get('country')
    transmission_rate = data.get('transmissionRate')
    mortality_rate = data.get('mortalityRate')
    incubation_period = data.get('incubationPeriod')
    
    script_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), f'{country.lower()}', 'plots.py')
    
    return run_script(script_path,transmission_rate, mortality_rate, incubation_period)
    
@app.route('/api/run_spread_map_first_weeks', methods=['POST'])
def run_spread_map_first_weeks():
    data = request.get_json()
    country = data.get('country')
    transmission_rate = data.get('transmissionRate')
    mortality_rate = data.get('mortalityRate')
    incubation_period = data.get('incubationPeriod')
    
    script_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), f'{country.lower()}', 'spread_map_first_weeks.py')
    
    return run_script(script_path,transmission_rate, mortality_rate, incubation_period)
  
if __name__ == '__main__':
    app.run(debug=True)

    