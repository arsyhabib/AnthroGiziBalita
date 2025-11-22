#!/usr/bin/env python3
"""
anthroGizi v4.0.0 - Enhanced Child Nutrition and Growth Monitoring Platform
Integrated with features from anthrohpk-app
Author: Habib Arsy and TIM
"""

import os
import json
import random
from datetime import datetime, timedelta
from functools import wraps
from flask import Flask, render_template, request, jsonify, redirect, url_for, flash, session, send_file
from werkzeug.utils import secure_filename
import pandas as pd
import plotly.graph_objs as go
import plotly.utils
from config import Config

# Initialize Flask app
app = Flask(__name__)
app.config.from_object(Config)

# Ensure secret key is set
if not app.config.get('SECRET_KEY'):
    app.config['SECRET_KEY'] = 'dev-secret-key-change-in-production'

# Initialize session and cache
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_FILE_DIR'] = './flask_session'

# Global variables for demo data
demo_children = []
growth_velocity_data = []
kpsp_results = []

class ChildNutritionCalculator:
    """Enhanced WHO calculator with all measurement types"""
    
    @staticmethod
    def calculate_all_indices(weight, height, age_months, gender, head_circumference=None):
        """Calculate all WHO indices"""
        results = {}
        
        # Mock calculations for demo - in production, use pygrowup
        results['waz'] = round(random.uniform(-2.5, 2.5), 2)  # Weight-for-Age
        results['haz'] = round(random.uniform(-2.5, 2.5), 2)  # Height-for-Age
        results['whz'] = round(random.uniform(-2.5, 2.5), 2)  # Weight-for-Height
        results['baz'] = round(random.uniform(-2.5, 2.5), 2)  # BMI-for-Age
        
        if head_circumference:
            results['hcz'] = round(random.uniform(-2.5, 2.5), 2)  # Head Circumference-for-Age
        
        # Add interpretations
        for index, value in results.items():
            if value < -3:
                results[f'{index}_status'] = 'Gizi Buruk'
                results[f'{index}_color'] = 'danger'
            elif value < -2:
                results[f'{index}_status'] = 'Gizi Kurang'
                results[f'{index}_color'] = 'warning'
            elif value > 2:
                results[f'{index}_status'] = 'Gizi Lebih'
                results[f'{index}_color'] = 'info'
            else:
                results[f'{index}_status'] = 'Gizi Baik'
                results[f'{index}_color'] = 'success'
        
        return results
    
    @staticmethod
    def calculate_age_in_days(birth_date, measurement_date):
        """Calculate age in days"""
        birth = datetime.strptime(birth_date, '%Y-%m-%d')
        measurement = datetime.strptime(measurement_date, '%Y-%m-%d')
        return (measurement - birth).days
    
    @staticmethod
    def get_normal_ranges(age_months, gender):
        """Get normal weight and height ranges for easy mode"""
        # Mock data - in production, use WHO reference tables
        if gender == 'L':
            weight_range = {
                6: {'min': 6.5, 'max': 9.5},
                12: {'min': 8.5, 'max': 12.5},
                24: {'min': 11.0, 'max': 16.0}
            }
            height_range = {
                6: {'min': 63, 'max': 73},
                12: {'min': 73, 'max': 83},
                24: {'min': 83, 'max': 93}
            }
        else:
            weight_range = {
                6: {'min': 5.8, 'max': 8.8},
                12: {'min': 7.8, 'max': 11.8},
                24: {'min': 10.2, 'max': 15.2}
            }
            height_range = {
                6: {'min': 61, 'max': 71},
                12: {'min': 71, 'max': 81},
                24: {'min': 81, 'max': 91}
            }
        
        # Find closest age
        closest_age = min(weight_range.keys(), key=lambda x: abs(x - age_months))
        
        return {
            'weight': weight_range.get(closest_age, {'min': 0, 'max': 0}),
            'height': height_range.get(closest_age, {'min': 0, 'max': 0})
        }

# Initialize calculator
calculator = ChildNutritionCalculator()

@app.route('/')
def index():
    """Homepage with feature showcase"""
    return render_template('index.html')

@app.route('/calculator')
def calculator_page():
    """WHO calculator page"""
    return render_template('calculator.html')

@app.route('/easy-mode')
def easy_mode():
    """Easy mode for quick reference"""
    return render_template('easy_mode.html')

@app.route('/growth-velocity')
def growth_velocity_page():
    """Halaman Kecepatan Pertumbuhan"""
    # Pastikan Anda membuat file template growth_velocity.html nanti
    return render_template('growth_velocity.html')

@app.route('/kpsp')
def kpsp_page():
    """KPSP screening page"""
    return render_template('kpsp.html')

@app.route('/library')
def library_page():
    """Enhanced library with English mode"""
    return render_template('library.html')

@app.route('/videos')
def videos_page():
    """Video library page"""
    return render_template('videos.html')

@app.route('/reports')
def reports_page():
    """Reports and analytics page"""
    return render_template('reports.html')

@app.route('/premium')
def premium_page():
    """Premium packages page"""
    return render_template('premium.html')

@app.route('/about')
def about_page():
    """About and support page"""
    return render_template('about.html')

@app.route('/api/calculate-all', methods=['POST'])
def calculate_all():
    """Calculate all WHO indices"""
    try:
        data = request.json
        
        # Extract data
        weight = float(data.get('weight', 0))
        height = float(data.get('height', 0))
        age_months = int(data.get('age_months', 0))
        gender = data.get('gender', 'L')
        head_circumference = data.get('head_circumference')
        if head_circumference:
            head_circumference = float(head_circumference)
        
        # Calculate all indices
        results = calculator.calculate_all_indices(weight, height, age_months, gender, head_circumference)
        
        # Add additional info
        results['age_months'] = age_months
        results['weight'] = weight
        results['height'] = height
        results['gender'] = gender
        results['head_circumference'] = head_circumference
        
        # Generate chart data
        chart_data = generate_growth_chart(weight, height, age_months, gender)
        results['chart_data'] = chart_data
        
        return jsonify({
            'success': True,
            'results': results,
            'message': 'Perhitungan berhasil dilakukan'
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'message': 'Terjadi kesalahan dalam perhitungan'
        })

@app.route('/api/easy-mode', methods=['POST'])
def easy_mode_calculation():
    """Easy mode calculation"""
    try:
        data = request.json
        age_months = int(data.get('age_months', 0))
        gender = data.get('gender', 'L')
        
        # Get normal ranges
        ranges = calculator.get_normal_ranges(age_months, gender)
        
        # Calculate age in days
        if data.get('birth_date') and data.get('measurement_date'):
            age_days = calculator.calculate_age_in_days(
                data['birth_date'], 
                data['measurement_date']
            )
        else:
            age_days = age_months * 30
        
        return jsonify({
            'success': True,
            'ranges': ranges,
            'age_days': age_days,
            'age_months': age_months,
            'gender': gender
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })

@app.route('/api/kpsp-calculate', methods=['POST'])
def calculate_kpsp():
    """Calculate KPSP results"""
    try:
        data = request.json
        age = int(data.get('age', 0))
        answers = data.get('answers', {})
        
        # Calculate score
        total_questions = len(answers)
        correct_answers = sum(1 for answer in answers.values() if answer == 'ya')
        score = correct_answers
        percentage = (score / total_questions) * 100 if total_questions > 0 else 0
        
        # Determine interpretation
        if percentage >= 80:
            status = 'normal'
            interpretation = 'Perkembangan Normal'
            recommendations = [
                'Lanjutkan stimulasi rutin di rumah',
                'Ikuti jadwal KMS sesuai usia',
                'Berikan nutrisi yang seimbang'
            ]
        elif percentage >= 60:
            status = 'meragukan'
            interpretation = 'Perkembangan Meragukan'
            recommendations = [
                'Konsultasikan dengan tenaga kesehatan',
                'Lakukan stimulasi perkembangan secara intensif',
                'Lakukan pemeriksaan ulang dalam 1-2 bulan'
            ]
        else:
            status = 'terlambat'
            interpretation = 'Perkembangan Terlambat'
            recommendations = [
                'Segera konsultasi dengan dokter anak',
                'Rujuk ke layanan intervensi dini',
                'Lakukan pemeriksaan menyeluruh'
            ]
        
        return jsonify({
            'success': True,
            'score': score,
            'total_questions': total_questions,
            'percentage': percentage,
            'status': status,
            'interpretation': interpretation,
            'recommendations': recommendations
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })

@app.route('/api/growth-velocity', methods=['POST'])
def calculate_growth_velocity():
    """Calculate growth velocity"""
    try:
        data = request.json
        measurements = data.get('measurements', [])
        
        if len(measurements) < 2:
            return jsonify({
                'success': False,
                'message': 'Minimal 2 pengukuran diperlukan'
            })
        
        # Calculate velocity
        velocities = []
        for i in range(1, len(measurements)):
            prev = measurements[i-1]
            curr = measurements[i]
            
            time_diff = (curr['age_months'] - prev['age_months']) / 12  # in years
            
            if time_diff > 0:
                weight_velocity = (curr['weight'] - prev['weight']) / time_diff
                height_velocity = (curr['height'] - prev['height']) / time_diff
                
                velocities.append({
                    'period': f"{prev['age_months']}-{curr['age_months']} bulan",
                    'weight_velocity': round(weight_velocity, 2),
                    'height_velocity': round(height_velocity, 2),
                    'time_diff': round(time_diff, 2)
                })
        
        return jsonify({
            'success': True,
            'velocities': velocities,
            'message': 'Perhitungan kecepatan pertumbuhan berhasil'
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })

def generate_growth_chart(weight, height, age_months, gender):
    """Generate growth chart data"""
    # Mock WHO reference data
    ages = list(range(0, 61, 3))
    
    if gender == 'L':
        who_weight_p50 = [3.3, 5.6, 7.0, 8.2, 9.2, 10.1, 10.9, 11.5, 12.0, 12.5, 12.9, 13.3, 13.6, 13.9, 14.2, 14.5, 14.7, 14.9, 15.1, 15.3, 15.5]
        who_height_p50 = [50, 58, 63, 67, 71, 74, 77, 79, 81, 83, 85, 87, 89, 90, 92, 93, 94, 95, 96, 97, 98]
    else:
        who_weight_p50 = [3.2, 5.1, 6.4, 7.5, 8.4, 9.2, 9.9, 10.5, 11.0, 11.5, 11.9, 12.3, 12.7, 13.0, 13.3, 13.6, 13.9, 14.1, 14.3, 14.5, 14.7]
        who_height_p50 = [49, 57, 61, 65, 69, 72, 75, 77, 79, 81, 83, 85, 87, 88, 90, 91, 92, 93, 94, 95, 96]
    
    # Create chart data
    chart_data = {
        'weight_chart': {
            'ages': ages,
            'who_reference': who_weight_p50,
            'child_data': [{'x': age_months, 'y': weight}],
            'title': 'Grafik Berat Badan Menurut Usia'
        },
        'height_chart': {
            'ages': ages,
            'who_reference': who_height_p50,
            'child_data': [{'x': age_months, 'y': height}],
            'title': 'Grafik Tinggi Badan Menurut Usia'
        }
    }
    
    return chart_data

@app.route('/api/export-data', methods=['POST'])
def export_data():
    """Export data to various formats"""
    try:
        data = request.json
        format_type = data.get('format', 'pdf')
        
        # Create DataFrame from data
        df = pd.DataFrame(data.get('data', []))
        
        if format_type == 'excel':
            output = 'export.xlsx'
            df.to_excel(output, index=False)
        elif format_type == 'csv':
            output = 'export.csv'
            df.to_csv(output, index=False)
        else:
            return jsonify({
                'success': False,
                'message': 'Format tidak didukung'
            })
        
        return jsonify({
            'success': True,
            'message': f'Data berhasil diexport sebagai {format_type}',
            'filename': output
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })

@app.route('/api/save-calculation', methods=['POST'])
def save_calculation():
    """Save calculation results"""
    try:
        data = request.json
        
        # Add timestamp
        data['timestamp'] = datetime.now().isoformat()
        data['id'] = len(demo_children) + 1
        
        # Save to demo storage
        demo_children.append(data)
        
        return jsonify({
            'success': True,
            'message': 'Data berhasil disimpan',
            'id': data['id']
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })

@app.route('/api/get-motivational-message')
def get_motivational_message():
    """Get random motivational message"""
    messages = [
        "Setiap anak adalah bakat istimewa yang sedang berkembang ✨",
        "Gizi yang baik hari ini adalah investasi masa depan 💪",
        "Perkembangan anak adalah perjalanan, bukan perlombaan 🌱",
        "Konsistensi dalam gizi memberikan hasil terbaik 🎯",
        "Setiap langkah kecil menuju kesehatan sangat berarti 💖",
        "Anak yang sehat adalah anak yang bahagia 😊",
        "Pertumbuhan optimal membutuhkan cinta, nutrisi, dan perhatian ❤️",
        "Anda melakukan pekerjaan luar biasa sebagai orang tua 👏",
        "Gizi seimbang kunci tumbuh kembang cerdas 🧠",
        "Hari ini adalah hari yang tepat untuk memulai kebiasaan baik 🌟"
    ]
    
    return jsonify({
        'message': random.choice(messages)
    })

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html'), 500

# Context processors
@app.context_processor
# Di app.py
@app.context_processor
def inject_globals():
    return {
        'app_name': 'anthroGizi v4.0.0',
        'app_version': '4.0.0',
        'author': 'Habib Arsy and TIM',
        'current_year': datetime.now().year,
        'contact_wa': '628123456789'  # <--- TAMBAHKAN BARIS INI (Ganti dengan nomor Anda)
        'motivational_message': '' # Tambahkan ini juga agar aman
    }

if __name__ == '__main__':
    # Create necessary directories
    os.makedirs('flask_session', exist_ok=True)
    os.makedirs('uploads', exist_ok=True)
    os.makedirs('data', exist_ok=True)
    
    # Run the application
    app.run(
        host='0.0.0.0',
        port=int(os.environ.get('PORT', 5000)),
        debug=app.config.get('DEBUG', True),
        threaded=True
    )
