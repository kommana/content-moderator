"""
Content Moderator
Author: Raj Kommana
License: MIT
Credits: Content moderation model by Duc Haba (https://huggingface.co/duchaba)
"""

from flask import Flask, request, jsonify, render_template
from gradio_client import Client
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.ticker import ScalarFormatter
import io
import base64
import json

app = Flask(__name__)
client = Client("https://duchaba-friendly-text-moderation.hf.space")

def clean_result_data(result_data):
    """Clean up the result data to remove duplicate categories"""
    # Categories we want to keep (using underscore version)
    main_categories = {
        'harassment': ['harassment', 'harassment_threatening'],
        'hate': ['hate', 'hate_threatening'],
        'self_harm': ['self_harm', 'self_harm_instructions', 'self_harm_intent'],
        'sexual': ['sexual', 'sexual_minors'],
        'violence': ['violence', 'violence_graphic']
    }
    
    # Keep metadata
    metadata = {
        'is_flagged': result_data.get('is_flagged', False),
        'is_safer_flagged': result_data.get('is_safer_flagged', False),
        'max_key': result_data.get('max_key', ''),
        'max_value': result_data.get('max_value', 0),
        'sum_value': result_data.get('sum_value', 0),
        'safer_value': result_data.get('safer_value', 0.02),
        'message': result_data.get('message', '')
    }
    
    # Create cleaned result with only underscore versions
    cleaned_result = {}
    
    # Add main categories and their subcategories
    for main_cat, sub_cats in main_categories.items():
        for sub_cat in sub_cats:
            if sub_cat in result_data:
                cleaned_result[sub_cat] = result_data[sub_cat]
    
    # Add metadata
    cleaned_result.update(metadata)
    
    return cleaned_result

def create_plot(result_data):
    try:
        plt.clf()
        plt.close('all')
        
        # Define main categories and their colors
        main_categories = {
            'harassment': '#FF6B6B',
            'hate': '#4ECDC4',
            'self_harm': '#95A5A6',
            'sexual': '#F7B731',
            'violence': '#6C5CE7'
        }
        
        # Get the maximum value for normalization
        max_value = float(result_data.get('max_value', 0))
        if max_value == 0:
            max_value = 1  # Prevent division by zero
        
        # Extract values and convert to percentages of max risk
        values = []
        labels = []
        colors = []
        
        for cat, color in main_categories.items():
            value = float(result_data.get(cat, 0))
            percentage = (value / max_value) * 100  # Convert to percentage of max risk
            
            # Determine risk level
            if value < 0.01:
                risk_level = "VERY SAFE"
            elif value < 0.5:
                risk_level = "SAFE"
            else:
                risk_level = "FLAGGED"
            
            label = f"{cat}\n{value:.2e}\n({risk_level})"
            
            values.append(percentage)
            labels.append(label)
            colors.append(color)
        
        # Create figure and axis
        fig, ax = plt.subplots(figsize=(12, 6))
        
        # Create bars
        bars = ax.bar(range(len(values)), values, color=colors)
        
        # Set x-axis labels
        plt.xticks(range(len(values)), labels, rotation=45, ha='right')
        
        # Set title and labels
        plt.title('Content Moderation Analysis - Relative Risk Levels\n'
                 f'Percentages relative to highest risk: {result_data.get("max_key", "N/A")} ({max_value:.2e})', 
                 pad=20)
        plt.ylabel('Relative Risk (% of highest risk)')
        
        # Add value labels on top of bars
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{height:.1f}%',
                   ha='center', va='bottom')
        
        # Add info text
        info_text = (
            f"Highest Risk Category: {result_data.get('max_key', 'N/A')} = {max_value:.2e}\n"
            f"Total Risk Score: {float(result_data.get('sum_value', 0)):.2e}\n"
            f"Safety Threshold: {float(result_data.get('safer_value', 0.02)):.2f}\n"
            f"Message Status: {'SAFE - No content warnings' if not result_data.get('is_flagged', False) else 'FLAGGED'}"
        )
        plt.figtext(0.02, 0.02, info_text, fontsize=8, bbox=dict(facecolor='white', alpha=0.8))
        
        # Set y-axis to go from 0 to 100%
        ax.set_ylim(0, 110)  # 110 to give space for value labels
        
        # Add grid for better readability
        ax.yaxis.grid(True, linestyle='--', alpha=0.7)
        ax.set_axisbelow(True)  # Put grid behind bars
        
        # Adjust layout
        plt.tight_layout()
        
        # Save to buffer
        buffer = io.BytesIO()
        plt.savefig(buffer, format='png', dpi=300, bbox_inches='tight')
        buffer.seek(0)
        image_png = buffer.getvalue()
        buffer.close()
        
        # Encode and cleanup
        graphic = base64.b64encode(image_png).decode('utf-8')
        plt.close('all')
        
        return graphic
        
    except Exception as e:
        print(f"Plot error: {str(e)}")
        return None
    
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/moderate', methods=['POST'])
def moderate():
    try:
        data = request.get_json()
        if not data or 'text' not in data:
            return jsonify({'error': 'Please enter text to moderate'}), 400
        
        text = data['text']
        safer_value = float(data.get('safer', 0.02))
        
        print(f"Processing text: {text} with safety value: {safer_value}")
        
        try:
            result = client.predict(
                text,
                safer_value,
                fn_index=0
            )
            print(f"Raw result: {result}")
            
            if isinstance(result, tuple):
                result_data = json.loads(result[1])
            else:
                result_data = json.loads(result)
            
            # Clean up the result data
            result_data = clean_result_data(result_data)
            
        except Exception as e:
            print(f"Prediction error: {str(e)}")
            return jsonify({'error': 'Model prediction failed'}), 500
        
        plot_url = create_plot(result_data)
        if plot_url is None:
            return jsonify({'error': 'Failed to create plot'}), 500
        
        return jsonify({
            "result": result_data,
            "plot": plot_url
        })
        
    except Exception as e:
        print(f"General error: {str(e)}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)