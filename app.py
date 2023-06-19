from flask import Flask, render_template,request
import pickle
import os
from jinja2 import TemplateNotFound

app = Flask(__name__, static_folder='static')


def load_model(model_path):
    full_path = os.path.join(os.path.dirname(__file__), model_path)
    model = pickle.load(open(full_path, 'rb'))
    return model

def create_app():
    app.config['ENV'] = 'production'
    # Load ML models
    model1 = load_model('model/modelM.pkl')
    model2 = load_model('model/modelF.pkl')
    model3 = load_model('model/modelD.pkl')
  
    # Load the scaler used for scaling the training data
    scaler1 = pickle.load(open('model/scalerM.pkl', 'rb'))
    scaler2 = pickle.load(open('model/scalerF.pkl', 'rb'))
  

    # Add the loaded models and scaler to the app context
    app.config['MODEL1'] = model1
    app.config['MODEL2'] = model2
    app.config['MODEL3'] = model3
    app.config['SCALER1'] = scaler1
    app.config['SCALER2'] = scaler2
    

    return app
# Helper - Extract current page name from request
def get_segment(request):
    try:
        segment = request.path.split('/')[-1]

        if segment == '':
            segment = 'index'

        return segment

    except:
        return None


@app.route('/')
def index():
    return render_template('home/index.html')


@app.route('/predictF')
def predictF():
    return render_template('home/predictF.html')

@app.route('/predictM')
def predictM():
    return render_template('home/predictM.html')

@app.route('/predictD')
def predictD():
    return render_template('home/diabetes.html')

@app.route('/resource')
def resource():
    return render_template('home/resource.html')

@app.route('/calc')
def calc():
    return render_template('home/pregCalc.html')

@app.route('/help')
def help():
    return render_template('home/helpline.html')



@app.route('/<template>')
def route_template(template):

    try:

        if not template.endswith('.html'):
            template += '.html'

        # Detect the current page
        segment = get_segment(request)

        # Serve the file (if exists) from app/templates/home/FILE.html
        return render_template("home/",template, segment=segment)

    except TemplateNotFound:
        return render_template('home/page-404.html'), 404

    except:
        return render_template('home/page-500.html'), 500


@app.route('/model1/predict', methods=['POST'])
def predict_model1():
    try:
        # Get the input values from the form
        age = float(request.form['age'])
        systolic_bp = float(request.form['systolicBP'])
        diastolic_bp = float(request.form['diastolicBP'])
        glucose = float(request.form['glucose'])
        temperature = float(request.form['temp'])
        heart_rate = float(request.form['heartRate'])

        # Create a feature vector or input array
        input_data = [[age, systolic_bp, diastolic_bp, glucose, temperature, heart_rate]]

        scaler1 = app.config['SCALER1'] 
        scaled_data = scaler1.transform(input_data)
        
        # Perform prediction using the loaded ML model for Model 1
        model1 = app.config['MODEL1']
        prediction = int(model1.predict(scaled_data))
   
        # Map the prediction to a meaningful label
        pred_mapper = {1:'Low Risk', 2:'Mid Risk', 3:'High Risk'}
        final_pred = pred_mapper.get(prediction, 'Unknown')

        return render_template('home/predictM.html', result_data={'prediction': final_pred})
    
    except Exception as e:
        error_message = f"An error occurred during prediction: {str(e)}"
        return render_template('home/page-400.html', error=error_message)


@app.route('/model2/predict', methods=['POST'])
def predict_model2():

    try:
        baseline = float(request.form['baseline'])
        accelerations = float(request.form['accelerations'])
        movement = float(request.form['movement'])
        contractions = float(request.form['contractions'])
        decelerations = float(request.form['decelerations'])
        severe = float(request.form['severe'])
        prolonged = float(request.form['prolonged'])
        abnormal = float(request.form['abnormal'])
        mean = float(request.form['mean'])
        time = float(request.form['time'])
        long = float(request.form['long'])
        width = float(request.form['width'])
        minimum = float(request.form['min'])
        maximum = float(request.form['max'])
        peaks = float(request.form['peaks'])
        zeroes = float(request.form['zero'])
        mode = float(request.form['mode'])
        hmean = float(request.form['hmean'])
        hmedian = float(request.form['hmedian'])
        variance = float(request.form['var'])
        tendency = float(request.form['tend'])
        
        input_data = [[baseline, accelerations, movement, contractions, decelerations, severe,
                                      prolonged, abnormal, mean, time, long, width, minimum, maximum, peaks,
                                      zeroes, mode, hmean, hmedian, variance, tendency]]
        
        scaler2 = app.config['SCALER2'] 
        scaled_data = scaler2.transform(input_data)
        
        # Perform prediction using the loaded ML model for Model 2
        model2 = app.config['MODEL2']
        prediction = int(model2.predict(scaled_data))

        # Map the prediction to a meaningful label
        pred_mapper = {1: 'Normal', 2: 'Suspect', 3: 'Pathological'}
        final_pred = pred_mapper.get(prediction, 'Unknown')

        # Prepare the data to pass to the result page for Model 2
        result_data = {
            'prediction': final_pred,
            'input_data': {
                'Baseline Heartrate': baseline,
                'Accelerations': accelerations,
                'Fetal Movement': movement,
                'Uterine Contractions': contractions,
                'Light Decelerations': decelerations,
                'Severe Decelerations': severe,
                'Prolonged Decelerations': prolonged,
                'Abnormal Short-term Variability': abnormal,
                'Mean Value of Short-term Variability': mean,
                'Percentage of Time with Abnormal Long-term Variability': time,
                'Mean Value of Long-term Variability': long,
                'Histogram Width': width,
                'Histogram Minimum': minimum,
                'Histogram Maximum': maximum,
                'Histogram Number of Peaks': peaks,
                'Histogram Number of Zeroes': zeroes,
                'Histogram Mode': mode,
                'Histogram Mean': hmean,
                'Histogram Median': hmedian,
                'Histogram Variance': variance,
                'Histogram Tendency': tendency
            }
        }

        return render_template('home/predictF.html', result_data=result_data)
    except Exception as e:
        error_message = f"An error occurred during prediction: {str(e)}"
        return render_template('home/page-400.html', error=error_message)



@app.route('/model3/predict', methods=['POST'])
def predict_model3():

    try:
        weight = float(request.form['weight'])
        bmi = float(request.form['BMI'])
        glucose = float(request.form['glucose'])
        fat = float(request.form['fat'])
        age = float(request.form['age'])
        
        input_data = [[weight,bmi,glucose,fat,age]]
        
     
        # Perform prediction using the loaded ML model for Model 2
        model3 = app.config['MODEL3']
        prediction = int(model3.predict(input_data))

        # Map the prediction to a meaningful label
        pred_mapper = {0: 'Low Risk', 1: 'High Risk'}
        final_pred = pred_mapper.get(prediction, 'Unknown')

        # Prepare the data to pass to the result page for Model 2
        result_data = {
            'prediction': final_pred,
            'input_data': {
                'Chlid Birth Weight(g)': weight,
                'BMI Pregestational (kg/m)': bmi,
                'First Fasting Glucose (mg/dl)': glucose,
                'Central Armellini Fat (mm)': fat,
                'Age': age
            }
        }

        return render_template('home/diabetes.html', result_data=result_data)
    except Exception as e:
        error_message = f"An error occurred during prediction: {str(e)}"
        return render_template('home/page-400.html', error=error_message)




if __name__ == "__main__":
    app = create_app()
    app.run()
