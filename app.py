from flask import Flask, render_template, request
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
import numpy as np
import pandas as pd
import os

app = Flask(__name__)

def get_sleep_quality():
    quality = request.form['sleep_quality']
    if quality in ['0', '1', '2']:
        return quality
    else:
        return "ข้อมูลผิด, กรุณาใส่คำว่า สนิท = 0 , สนิทปานกลาง = 1 , ไม่สนิท = 2"

def calculate_bmi(weight, height):
    bmi = weight / (height/100)**2
    if bmi < 18.5:
        category = "น้ำหนักน้อย/ผอม"
    elif bmi < 23:
        category = "ปกติ (สุขภาพดี)"
    elif bmi < 25:
        category = "ท้วม / โรคอ้วนระดับ 1"
    else:
        category = "อ้วน / โรคอ้วนระดับ 2"
    return bmi, category

def check_sleep_duration(duration):
    if duration >= 7 and duration <= 9:
        return "เพียงพอ"
    else:
        return "ไม่เพียงพอ"
    

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/program')
def program():
    return render_template('program.html')

@app.route('/process_input', methods=['POST'])
def process_input():
    weight = float(request.form['weight'])
    height = float(request.form['height'])
    sleep_duration = float(request.form['sleep_duration'])
    sleep_quality = get_sleep_quality()

    bmi, category = calculate_bmi(weight, height)
    sleep_status = check_sleep_duration(sleep_duration)

    data = [
        "น้ำหนัก : "+str(int(weight)), 
        "ส่วนสูง : "+str(int(height)), 
        "นอนกี่ชั่วโมง : "+str(int(sleep_duration)), 
        "คุณภาพการนอนหลับ : "+sleep_quality+" = "+sleep_status, 
        "BMI : "+str("%.2f"%bmi), 
        "ประเมินว่า : "+category
    ]
    
    def save_data_to_file(data):
        with open('uploaded_files/database_pscp.txt', 'a', encoding='utf-8') as file:
            file.write("User\n")
            for item in data:
                file.write("%s\n" % item)
            file.write("\n")
    save_data_to_file(data)
    return render_template('program.html', data = data)

@app.route('/process_plot')
def plot_process():
    with open('uploaded_files/database_pscp.txt', 'r', encoding='utf-8') as file:
        data = file.read()
        
    users_data = data.split('\n\nUser\n')[1:]
    weights = []
    heights = []
    hours_slept = []
    quality_of_sleep = []
    
    for user_data in users_data:
        lines = user_data.strip().split('\n')
        weights.append(float(lines[0].split(': ')[1]))
        heights.append(float(lines[1].split(': ')[1]))
        hours_slept.append(float(lines[2].split(': ')[1]))
        quality_of_sleep.append(float(lines[3].split(': ')[1].split(' = ')[0]))
  
    average_weight = np.mean(weights)
    average_height = np.mean(heights)
    average_hours_slept = np.mean(hours_slept)
    average_quality_of_sleep = np.mean(quality_of_sleep)

    
    labels = ['Weight', 'Height', 'Hours Slept', 'Quality of Sleep']
    values = [average_weight, average_height, average_hours_slept, average_quality_of_sleep]

    plt.figure(figsize=(10, 5))
    plt.bar(labels, values)
    plt.title('Average User Data')
    plt.xlabel('Categories')
    plt.ylabel('Average Value')
    plt.savefig('static/images/bar_plot.png')
    plt.close()

   
    categories = ['Weight', 'Height', 'Hours Slept', 'Quality of Sleep']
    average_values = [average_weight, average_height, average_hours_slept, average_quality_of_sleep]

    plt.figure(figsize=(10, 5))
    plt.plot(categories, average_values, marker='o')
    plt.title('Average User Data')
    plt.xlabel('Categories')
    plt.ylabel('Average Value')
    plt.savefig('static/images/line_plot.png')
    plt.close()
    
    return render_template('program_plot.html')

if __name__ == '__main__':
    app.run(debug=True)
