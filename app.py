import os
import io
import json
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, flash, send_file, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
from fitparse import FitFile
from fpdf import FPDF
import matplotlib.pyplot as plt
import pandas as pd

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key_here'
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///local.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'uploads'

db = SQLAlchemy(app)

# --- Database Models ---

class Marker(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    unit = db.Column(db.String(20))
    min_norm = db.Column(db.Float)
    max_norm = db.Column(db.Float)

    def to_dict(self):
        return {'id': self.id, 'name': self.name, 'unit': self.unit or '', 'min_norm': self.min_norm or '', 'max_norm': self.max_norm or ''}

class LabValue(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    value = db.Column(db.Float, nullable=False)
    unit = db.Column(db.String(20))
    min_norm = db.Column(db.Float)
    max_norm = db.Column(db.Float)

    def to_dict(self):
        return {
            'id': self.id, 'type': 'lab',
            'date': self.date.strftime('%Y-%m-%d'),
            'name': self.name, 'value': self.value, 'unit': self.unit or '',
            'min_norm': self.min_norm or '', 'max_norm': self.max_norm or ''
        }

class VitalValue(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False)
    type = db.Column(db.String(50)) 
    value_sys = db.Column(db.Integer) 
    value_dia = db.Column(db.Integer) 
    value_pulse = db.Column(db.Integer) 
    
    def to_dict(self):
        return {
            'id': self.id, 'type': 'vital',
            'date': self.date.strftime('%Y-%m-%d'),
            'time': self.date.strftime('%H:%M'),
            'sys': self.value_sys, 'dia': self.value_dia, 'pulse': self.value_pulse
        }

class WeightEntry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False)
    weight = db.Column(db.Float, nullable=False)
    fat_percentage = db.Column(db.Float)
    bmi = db.Column(db.Float)
    skeletal_muscle = db.Column(db.Float)
    muscle_mass = db.Column(db.Float)
    protein = db.Column(db.Float)
    bmr = db.Column(db.Float)
    fat_free_mass = db.Column(db.Float)
    subcutaneous_fat = db.Column(db.Float)
    visceral_fat = db.Column(db.Float)
    body_water = db.Column(db.Float)
    bone_mass = db.Column(db.Float)
    
    def to_dict(self):
        return {
            'id': self.id, 
            'type': 'weight', 
            'date': self.date.strftime('%Y-%m-%d'), 
            'weight': self.weight,
            'fat_percentage': self.fat_percentage,
            'bmi': self.bmi,
            'skeletal_muscle': self.skeletal_muscle,
            'muscle_mass': self.muscle_mass,
            'protein': self.protein,
            'bmr': self.bmr,
            'fat_free_mass': self.fat_free_mass,
            'subcutaneous_fat': self.subcutaneous_fat,
            'visceral_fat': self.visceral_fat,
            'body_water': self.body_water,
            'bone_mass': self.bone_mass
        }

class Steps(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False, unique=True) 
    count = db.Column(db.Integer, nullable=False)

    def to_dict(self):
        return {'id': self.id, 'type': 'steps', 'date': self.date.strftime('%Y-%m-%d'), 'count': self.count}

class FoodEntry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False)
    description = db.Column(db.String(200))
    calories = db.Column(db.Integer)
    protein = db.Column(db.Float, default=0)
    carbs = db.Column(db.Float, default=0)
    fat = db.Column(db.Float, default=0)

    def to_dict(self):
        return {
            'id': self.id, 'type': 'food',
            'date': self.date.strftime('%Y-%m-%d'),
            'description': self.description, 'calories': self.calories or 0,
            'protein': self.protein or 0, 'carbs': self.carbs or 0, 'fat': self.fat or 0
        }

class Activity(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False)
    type = db.Column(db.String(50))
    duration_min = db.Column(db.Integer)
    distance_km = db.Column(db.Float)
    source = db.Column(db.String(20)) 
    garmin_id = db.Column(db.String(100), unique=True) 

    def to_dict(self):
        return {
            'id': self.id, 'type': 'activity', 'act_type': self.type,
            'date': self.date.strftime('%Y-%m-%d'),
            'time': self.date.strftime('%H:%M'),
            'duration': self.duration_min, 'distance': self.distance_km or '', 'source': self.source
        }

class Profile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    height_cm = db.Column(db.Float)
    birthdate = db.Column(db.Date)

class Medication(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    unit = db.Column(db.String(50)) # e.g. "Tabletten", "Tropfen"
    common_dose = db.Column(db.String(100)) # e.g. "1, 2, 0.5"

    def to_dict(self):
        return {'id': self.id, 'name': self.name, 'unit': self.unit or '', 'common_dose': self.common_dose or ''}

class MedicationEntry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False)
    medication_id = db.Column(db.Integer, db.ForeignKey('medication.id'), nullable=False)
    amount = db.Column(db.String(50), nullable=False) # Store as string to allow "1 Tablette" or "50"
    medication = db.relationship('Medication')

    def to_dict(self):
        return {
            'id': self.id, 'name': self.medication.name,
            'amount': self.amount, 'unit': self.medication.unit,
            'date': self.date.strftime('%Y-%m-%d')
        }

class MoodEntry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False)
    mood_score = db.Column(db.Integer) 
    energy_score = db.Column(db.Integer) 
    notes = db.Column(db.Text)

    def to_dict(self):
        return {
            'id': self.id, 'date': self.date.strftime('%Y-%m-%d'),
            'mood': self.mood_score, 'energy': self.energy_score, 'notes': self.notes
        }

class WaterEntry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False) 
    amount_ml = db.Column(db.Integer, nullable=False)

class SleepEntry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False) 
    duration_hours = db.Column(db.Float, nullable=False)
    quality = db.Column(db.Integer) 

    def to_dict(self):
        return {
            'id': self.id, 'date': self.date.strftime('%Y-%m-%d'),
            'duration': self.duration_hours, 'quality': self.quality
        }

# --- Helper Functions ---

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'fit'}

def safe_float(val, default=None):
    try: return float(val)
    except: return default

def safe_int(val, default=None):
    try: return int(val)
    except: return default

def parse_date_str(date_str):
    return datetime.strptime(date_str, '%Y-%m-%d')

def parse_datetime_str(date_str, time_str):
    return datetime.strptime(f"{date_str} {time_str}", '%Y-%m-%d %H:%M')

# --- Routes ---

@app.route('/', methods=['GET'])
def index():
    sort_order = request.args.get('sort', 'desc')
    sort_dir = sort_order
    def get_sort(model): return model.date.asc() if sort_dir == 'asc' else model.date.desc()

    lab_values = LabValue.query.order_by(get_sort(LabValue)).all()
    markers = Marker.query.order_by(Marker.name).all()
    vitals = VitalValue.query.order_by(get_sort(VitalValue)).all()
    weights = WeightEntry.query.order_by(get_sort(WeightEntry)).all()
    foods = FoodEntry.query.order_by(get_sort(FoodEntry)).all()
    activities = Activity.query.order_by(get_sort(Activity)).all()
    steps = Steps.query.order_by(get_sort(Steps)).all()
    meds_def = Medication.query.all()
    meds_log = MedicationEntry.query.order_by(get_sort(MedicationEntry)).all()
    moods = MoodEntry.query.order_by(get_sort(MoodEntry)).all()
    sleeps = SleepEntry.query.order_by(SleepEntry.date.desc() if sort_dir == 'desc' else SleepEntry.date.asc()).all()
    water_today = db.session.query(db.func.sum(WaterEntry.amount_ml)).filter(WaterEntry.date == datetime.now().date()).scalar() or 0
    
    recent_history = []
    for i in range(3):
        d = (datetime.now() - pd.Timedelta(days=i)).date()
        d_start = datetime.combine(d, datetime.min.time()); d_end = datetime.combine(d, datetime.max.time())
        day_steps = Steps.query.filter(Steps.date == d_start).first()
        day_weight = WeightEntry.query.filter(WeightEntry.date >= d_start, WeightEntry.date <= d_end).first()
        day_sleep = SleepEntry.query.filter(SleepEntry.date == d).first()
        day_foods = FoodEntry.query.filter(FoodEntry.date >= d_start, FoodEntry.date <= d_end).all()
        macros = {'kcal': 0, 'p': 0, 'c': 0, 'f': 0}
        for f in day_foods:
            macros['kcal'] += (f.calories or 0); macros['p'] += (f.protein or 0); macros['c'] += (f.carbs or 0); macros['f'] += (f.fat or 0)
        recent_history.append({'date': d, 'steps': day_steps.count if day_steps else None, 'weight': day_weight.weight if day_weight else None, 'sleep': day_sleep.duration_hours if day_sleep else None, 'macros': macros})

    profile = Profile.query.first()
    return render_template('index.html', labs=lab_values, markers=markers, vitals=vitals, weights=weights, foods=foods, activities=activities, steps=steps, meds_def=meds_def, meds_log=meds_log, moods=moods, profile=profile, sleeps=sleeps, water_today=water_today, recent_history=recent_history, sort_order=sort_order, now=datetime.now()) 

# --- CRUD Routes ---

@app.route('/save_profile', methods=['POST'])
def save_profile():
    p = Profile.query.first() or Profile()
    if not p.id: db.session.add(p)
    p.height_cm = safe_float(request.form.get('height')); bd = request.form.get('birthdate')
    if bd: p.birthdate = parse_date_str(bd)
    db.session.commit(); return redirect(url_for('index'))

@app.route('/add_water', methods=['POST'])
def add_water():
    amount = safe_int(request.form.get('amount'))
    if amount: db.session.add(WaterEntry(date=datetime.now().date(), amount_ml=amount)); db.session.commit()
    return redirect(url_for('index'))

@app.route('/reset_water', methods=['POST'])
def reset_water():
    WaterEntry.query.filter_by(date=datetime.now().date()).delete(); db.session.commit(); return redirect(url_for('index'))

@app.route('/add_sleep', methods=['POST'])
def add_sleep():
    date = parse_date_str(request.form.get('date')).date()
    duration = safe_float(request.form.get('duration')); quality = safe_int(request.form.get('quality'))
    existing = SleepEntry.query.filter_by(date=date).first()
    if existing: existing.duration_hours = duration; existing.quality = quality
    else: db.session.add(SleepEntry(date=date, duration_hours=duration, quality=quality))
    db.session.commit(); return redirect(url_for('index'))

@app.route('/add_medication_def', methods=['POST'])
def add_medication_def():
    name = request.form.get('name'); unit = request.form.get('unit'); doses = request.form.get('common_dose')
    if name: db.session.add(Medication(name=name, unit=unit, common_dose=doses)); db.session.commit()
    return redirect(url_for('index'))

@app.route('/add_medication_entry', methods=['POST'])
def add_medication_entry():
    date = parse_date_str(request.form.get('date')); med_id = request.form.get('med_id')
    amount = request.form.get('amount_custom') or request.form.get('amount_select')
    if med_id and amount: db.session.add(MedicationEntry(date=date, medication_id=med_id, amount=amount)); db.session.commit()
    return redirect(url_for('index'))

@app.route('/add_mood', methods=['POST'])
def add_mood():
    db.session.add(MoodEntry(date=parse_date_str(request.form.get('date')), mood_score=safe_int(request.form.get('mood')), energy_score=safe_int(request.form.get('energy')), notes=request.form.get('notes')))
    db.session.commit(); return redirect(url_for('index'))

@app.route('/add_lab', methods=['POST'])
def add_lab():
    db.session.add(LabValue(date=parse_date_str(request.form['date']), name=request.form['name'], value=safe_float(request.form['value']), unit=request.form.get('unit'), min_norm=safe_float(request.form.get('min_norm')), max_norm=safe_float(request.form.get('max_norm'))))
    db.session.commit(); return redirect(url_for('index'))

@app.route('/add_vital', methods=['POST'])
def add_vital():
    db.session.add(VitalValue(date=parse_datetime_str(request.form['date'], request.form['time']), type='Blutdruck/Puls', value_sys=safe_int(request.form['sys']), value_dia=safe_int(request.form['dia']), value_pulse=safe_int(request.form['pulse'])))
    db.session.commit(); return redirect(url_for('index'))

@app.route('/add_weight', methods=['POST'])
def add_weight():
    db.session.add(WeightEntry(
        date=parse_datetime_str(request.form['weight_date'], request.form.get('weight_time', '00:00')), 
        weight=safe_float(request.form['weight_val']),
        fat_percentage=safe_float(request.form.get('fat_percentage')),
        bmi=safe_float(request.form.get('bmi')),
        skeletal_muscle=safe_float(request.form.get('skeletal_muscle')),
        muscle_mass=safe_float(request.form.get('muscle_mass')),
        protein=safe_float(request.form.get('weight_protein')),
        bmr=safe_float(request.form.get('bmr')),
        fat_free_mass=safe_float(request.form.get('fat_free_mass')),
        subcutaneous_fat=safe_float(request.form.get('subcutaneous_fat')),
        visceral_fat=safe_float(request.form.get('visceral_fat')),
        body_water=safe_float(request.form.get('body_water')),
        bone_mass=safe_float(request.form.get('bone_mass'))
    ))
    db.session.commit(); return redirect(url_for('index'))

@app.route('/add_steps', methods=['POST'])
def add_steps():
    dt = parse_date_str(request.form['steps_date']); existing = Steps.query.filter(Steps.date == dt).first()
    if existing: existing.count = safe_int(request.form['steps_count'])
    else: db.session.add(Steps(date=dt, count=safe_int(request.form['steps_count'])))
    db.session.commit(); return redirect(url_for('index'))

@app.route('/add_food', methods=['POST'])
def add_food():
    db.session.add(FoodEntry(date=parse_date_str(request.form['food_date']), description=request.form['food_desc'], calories=safe_int(request.form.get('food_cal')), protein=safe_float(request.form.get('food_pro')), carbs=safe_float(request.form.get('food_carb')), fat=safe_float(request.form.get('food_fat'))))
    db.session.commit(); return redirect(url_for('index'))

@app.route('/add_activity', methods=['POST'])
def add_activity():
    db.session.add(Activity(date=parse_datetime_str(request.form['date'], request.form['time']), type=request.form['act_type'], duration_min=safe_int(request.form['act_duration']), distance_km=safe_float(request.form.get('act_distance')), source='manual'))
    db.session.commit(); return redirect(url_for('index'))

@app.route('/get_entry/<string:model_type>/<int:id>')
def get_entry(model_type, id):
    model_map = {
        'lab': LabValue, 'vital': VitalValue, 'weight': WeightEntry, 
        'steps': Steps, 'food': FoodEntry, 'activity': Activity, 
        'medication': MedicationEntry, 'sleep': SleepEntry, 'mood': MoodEntry,
        'marker': Marker, 'med_def': Medication
    }
    Model = model_map.get(model_type)
    if not Model: return jsonify({'error': 'Invalid type'}), 400
    obj = Model.query.get_or_404(id)
    return jsonify(obj.to_dict())

@app.route('/edit_entry/<string:model_type>/<int:id>', methods=['POST'])
def edit_entry(model_type, id):
    model_map = {
        'lab': LabValue, 'vital': VitalValue, 'weight': WeightEntry, 
        'steps': Steps, 'food': FoodEntry, 'activity': Activity, 
        'medication': MedicationEntry, 'sleep': SleepEntry, 'mood': MoodEntry,
        'marker': Marker, 'med_def': Medication
    }
    Model = model_map.get(model_type)
    if not Model: return redirect(url_for('index'))
    obj = Model.query.get_or_404(id)
    
    if model_type == 'lab':
        obj.date = parse_date_str(request.form['date'])
        obj.name = request.form['name']; obj.value = safe_float(request.form['value']); obj.unit = request.form.get('unit')
        obj.min_norm = safe_float(request.form.get('min_norm')); obj.max_norm = safe_float(request.form.get('max_norm'))
    elif model_type == 'marker':
        obj.name = request.form['name']; obj.unit = request.form.get('unit')
        obj.min_norm = safe_float(request.form.get('min_norm')); obj.max_norm = safe_float(request.form.get('max_norm'))
    elif model_type == 'med_def':
        obj.name = request.form['name']; obj.unit = request.form.get('unit'); obj.common_dose = request.form.get('common_dose')
    elif model_type == 'vital':
        obj.date = parse_datetime_str(request.form['date'], request.form['time'])
        obj.value_sys = safe_int(request.form['sys']); obj.value_dia = safe_int(request.form['dia']); obj.value_pulse = safe_int(request.form['pulse'])
    elif model_type == 'weight':
        obj.date = parse_datetime_str(request.form['weight_date'], request.form.get('weight_time', '00:00'))
        obj.weight = safe_float(request.form['weight_val']); obj.fat_percentage = safe_float(request.form.get('fat_percentage'))
        obj.bmi = safe_float(request.form.get('bmi')); obj.skeletal_muscle = safe_float(request.form.get('skeletal_muscle'))
        obj.muscle_mass = safe_float(request.form.get('muscle_mass')); obj.protein = safe_float(request.form.get('weight_protein'))
        obj.bmr = safe_float(request.form.get('bmr')); obj.fat_free_mass = safe_float(request.form.get('fat_free_mass'))
        obj.subcutaneous_fat = safe_float(request.form.get('subcutaneous_fat')); obj.visceral_fat = safe_float(request.form.get('visceral_fat'))
        obj.body_water = safe_float(request.form.get('body_water')); obj.bone_mass = safe_float(request.form.get('bone_mass'))
    elif model_type == 'steps':
        obj.date = parse_date_str(request.form['steps_date']); obj.count = safe_int(request.form['steps_count'])
    elif model_type == 'food':
        obj.date = parse_date_str(request.form['food_date']); obj.description = request.form['food_desc']
        obj.calories = safe_int(request.form.get('food_cal')); obj.protein = safe_float(request.form.get('food_pro'))
        obj.carbs = safe_float(request.form.get('food_carb')); obj.fat = safe_float(request.form.get('food_fat'))
    elif model_type == 'activity':
        obj.date = parse_datetime_str(request.form['date'], request.form['time']); obj.type = request.form['act_type']
        obj.duration_min = safe_int(request.form['act_duration']); obj.distance_km = safe_float(request.form.get('act_distance'))
    elif model_type == 'sleep':
        obj.date = parse_date_str(request.form['date']).date()
        obj.duration_hours = safe_float(request.form['duration']); obj.quality = safe_int(request.form['quality'])
    elif model_type == 'mood':
        obj.date = parse_date_str(request.form['date'])
        obj.mood_score = safe_int(request.form['mood']); obj.energy_score = safe_int(request.form['energy']); obj.notes = request.form['notes']
    elif model_type == 'medication':
        obj.date = parse_date_str(request.form['date'])
        obj.amount = request.form.get('amount_custom') or request.form.get('amount_select')

    db.session.commit(); return redirect(url_for('index'))

@app.route('/delete_entry/<string:model_type>/<int:id>', methods=['POST'])
def delete_entry(model_type, id):
    model_map = {
        'lab': LabValue, 'vital': VitalValue, 'weight': WeightEntry, 
        'steps': Steps, 'food': FoodEntry, 'activity': Activity, 
        'marker': Marker, 'medication': MedicationEntry, 'sleep': SleepEntry, 
        'mood': MoodEntry, 'med_def': Medication
    }
    Model = model_map.get(model_type)
    if Model: db.session.delete(Model.query.get_or_404(id)); db.session.commit()
    return redirect(url_for('index'))

@app.route('/daily_summary/<string:target_date>')
def daily_summary(target_date):
    try:
        dt = datetime.strptime(target_date, '%Y-%m-%d'); start = datetime.combine(dt, datetime.min.time()); end = datetime.combine(dt, datetime.max.time())
        weights = WeightEntry.query.filter(WeightEntry.date >= start, WeightEntry.date <= end).all()
        steps = Steps.query.filter(Steps.date >= start, Steps.date <= end).all()
        foods = FoodEntry.query.filter(FoodEntry.date >= start, FoodEntry.date <= end).all()
        vitals = VitalValue.query.filter(VitalValue.date >= start, VitalValue.date <= end).all()
        activities = Activity.query.filter(Activity.date >= start, Activity.date <= end).all()
        moods = MoodEntry.query.filter(MoodEntry.date >= start, MoodEntry.date <= end).all()
        meds = MedicationEntry.query.filter(MedicationEntry.date >= start, MedicationEntry.date <= end).all()
        labs = LabValue.query.filter(LabValue.date >= start, LabValue.date <= end).all()
        sleep = SleepEntry.query.filter(SleepEntry.date == dt.date()).first()
        water_sum = db.session.query(db.func.sum(WaterEntry.amount_ml)).filter(WaterEntry.date == dt.date()).scalar() or 0
        nutrition = {'calories': 0, 'protein': 0, 'carbs': 0, 'fat': 0}
        for f in foods:
            nutrition['calories'] += (f.calories or 0); nutrition['protein'] += (f.protein or 0); nutrition['carbs'] += (f.carbs or 0); nutrition['fat'] += (f.fat or 0)
        return jsonify({
            'weights': [w.to_dict() for w in weights], 'steps': [s.to_dict() for s in steps],
            'nutrition_summary': nutrition, 'vitals': [v.to_dict() for v in vitals],
            'activities': [a.to_dict() for a in activities], 'moods': [m.to_dict() for m in moods],
            'meds': [m.to_dict() for m in meds], 'sleep': sleep.to_dict() if sleep else None, 
            'water': water_sum, 'lab_values': [l.to_dict() for l in labs], 'foods': [f.to_dict() for f in foods]
        })
    except Exception as e: return jsonify({'error': str(e)}), 400

@app.route('/chart_data')
def chart_data():
    weights = WeightEntry.query.order_by(WeightEntry.date).all()
    steps = Steps.query.order_by(Steps.date).all()
    vitals = VitalValue.query.order_by(VitalValue.date).all()
    return jsonify({
        'weights': [{'date': w.date.strftime('%Y-%m-%d'), 'weight': w.weight} for w in weights],
        'steps': [{'date': s.date.strftime('%Y-%m-%d'), 'count': s.count} for s in steps],
        'vitals': [{'date': v.date.strftime('%Y-%m-%d %H:%M'), 'sys': v.value_sys, 'dia': v.value_dia, 'pulse': v.value_pulse} for v in vitals]
    })

@app.route('/export')
def export_data():
    data = {
        'lab_values': [{'date': l.date.strftime('%Y-%m-%d'), 'name': l.name, 'value': l.value, 'unit': l.unit} for l in LabValue.query.all()],
        'weights': [{'date': w.date.strftime('%Y-%m-%d'), 'weight': w.weight} for w in WeightEntry.query.all()],
        'steps': [{'date': s.date.strftime('%Y-%m-%d'), 'count': s.count} for s in Steps.query.all()]
    }
    res = jsonify(data); res.headers['Content-Disposition'] = 'attachment; filename=health_export.json'; return res

@app.route('/pdf')
def generate_pdf():
    try:
        pdf = FPDF(); pdf.set_margins(10, 10, 10); pdf.add_page(); pdf.set_auto_page_break(auto=True, margin=15); w = 190
        def clean(s): return str(s).encode('latin-1', 'replace').decode('latin-1') if s else ""
        pdf.set_font("Arial", 'B', 20); pdf.cell(w, 15, txt=clean("Gesundheitsbericht"), ln=1, align='C')
        data_by_date = {}
        def add(d_obj, text, cat):
            d_str = d_obj.strftime('%Y-%m-%d'); 
            if d_str not in data_by_date: data_by_date[d_str] = []
            data_by_date[d_str].append({'text': clean(text), 'time': d_obj.strftime('%H:%M') if hasattr(d_obj, 'strftime') else "00:00"})
        for x in LabValue.query.all(): add(x.date, f"Labor: {x.name}={x.value}{x.unit}", "L")
        for x in VitalValue.query.all(): add(x.date, f"Vital: {x.value_sys}/{x.value_dia} Puls:{x.value_pulse}", "V")
        for x in WeightEntry.query.all(): 
            details = [f"Gewicht: {x.weight}kg"]
            if x.fat_percentage: details.append(f"Fett: {x.fat_percentage}%")
            if x.bmi: details.append(f"BMI: {x.bmi}")
            if x.skeletal_muscle: details.append(f"Skelettmuskeln: {x.skeletal_muscle}%")
            if x.muscle_mass: details.append(f"Muskelmasse: {x.muscle_mass}kg")
            if x.protein: details.append(f"Protein: {x.protein}%")
            if x.bmr: details.append(f"Grundumsatz: {x.bmr}kcal")
            if x.fat_free_mass: details.append(f"Fettfreie Masse: {x.fat_free_mass}kg")
            if x.subcutaneous_fat: details.append(f"Subkutanes Fett: {x.subcutaneous_fat}%")
            if x.visceral_fat: details.append(f"Viszerales Fett: {x.visceral_fat}")
            if x.body_water: details.append(f"Körperwasser: {x.body_water}%")
            if x.bone_mass: details.append(f"Knochenmasse: {x.bone_mass}kg")
            add(x.date, " | ".join(details), "W")
        for x in Steps.query.all(): add(x.date, f"Schritte: {x.count}", "S")
        for x in MoodEntry.query.all(): add(x.date, f"Mood: {x.mood_score}/10", "M")
        for x in SleepEntry.query.all(): add(datetime.combine(x.date, datetime.min.time()), f"Schlaf: {x.duration_hours}h", "SL")
        for d_str in sorted(data_by_date.keys(), reverse=True):
            pdf.set_fill_color(230, 230, 230); pdf.set_font("Arial", 'B', 12); pdf.cell(w, 10, txt=clean(d_str), ln=1, fill=True); pdf.set_font("Arial", '', 10)
            for e in sorted(data_by_date[d_str], key=lambda x: x['time']): pdf.multi_cell(w, 6, txt=f"[{e['time']}] {e['text']}")
        pdf_output = pdf.output(dest='S')
        if isinstance(pdf_output, str): pdf_output = pdf_output.encode('latin-1')
        return send_file(io.BytesIO(pdf_output), mimetype='application/pdf', as_attachment=True, download_name='report.pdf')
    except Exception as e: return str(e), 500

with app.app_context():
    db.create_all()
    # Simple migration hack for existing installations
    try:
        cols = [
            ("fat_percentage", "FLOAT"), ("bmi", "FLOAT"), ("skeletal_muscle", "FLOAT"),
            ("muscle_mass", "FLOAT"), ("protein", "FLOAT"), ("bmr", "FLOAT"),
            ("fat_free_mass", "FLOAT"), ("subcutaneous_fat", "FLOAT"), ("visceral_fat", "FLOAT"),
            ("body_water", "FLOAT"), ("bone_mass", "FLOAT")
        ]
        for col_name, col_type in cols:
            try:
                db.session.execute(db.text(f"ALTER TABLE weight_entry ADD COLUMN {col_name} {col_type}"))
            except Exception:
                pass # Column likely already exists
        
        db.session.execute(db.text("ALTER TABLE medication ADD COLUMN IF NOT EXISTS unit VARCHAR(50)"))
        db.session.execute(db.text("ALTER TABLE medication ADD COLUMN IF NOT EXISTS common_dose VARCHAR(100)"))
        db.session.commit()
    except Exception as e:
        print(f"Migration check: {e}")
        db.session.rollback()
    
    if not os.path.exists(app.config['UPLOAD_FOLDER']): os.makedirs(app.config['UPLOAD_FOLDER'])

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
