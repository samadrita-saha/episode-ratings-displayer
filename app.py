from flask import Flask, render_template, request, send_from_directory
import os
import pandas as pd
from show import get_show_info
from main import generate_heatmap, get_num_seasons, get_episode_ratings  

app = Flask(__name__)

if not os.path.exists('static'):
    os.makedirs('static')

@app.route('/', methods=['GET', 'POST'])
def home():
    show_id = None
    show_name = None
    heatmap_image_path = None

    if request.method == 'POST':
        show_name = request.form['show_name']
        if show_name:
            show_id, show_title = get_show_info(show_name)

            num_seasons = get_num_seasons(show_id)
            episode_data = get_episode_ratings(show_id, num_seasons)
            
            df = pd.DataFrame(episode_data)
            heatmap_image_path = generate_heatmap(df, show_title)

    return render_template('index.html', show_name=show_name, heatmap_image_path=heatmap_image_path)

@app.route('/static/<filename>')
def serve_image(filename):
    return send_from_directory('static', filename)

if __name__ == '__main__':
    app.run(debug=True)
