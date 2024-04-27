import time
import random
from threading import Thread
import speech_recognition as sr
import pyaudio
import pickle
import streamlit as st
import soundfile as sf
import sounddevice as sd
import numpy as np
from streamlit_option_menu import option_menu
import pymysql
import base64
import os

connection = pymysql.connect(
    host="sql6.freesqldatabase.com",
    user="sql6701908",
    password="xl5jGPFC2Q",
    database="sql6701908"
)
def show_content():
    diab_diagnosis = ''
    heart_diagnosis = ''

    # Function to monitor health parameters in real-time
    def monitor_health():
        while True:
            # Simulate retrieval of health parameters (replace with actual data retrieval)
            glucose_level = random.randint(80, 180)  # Random glucose level between 80 and 180 mg/dl
            blood_pressure = random.randint(90, 140)  # Random blood pressure between 90 and 140 mmHg
            heart_rate = random.randint(60, 100)  # Random heart rate between 60 and 100 bpm

            # Example threshold values for health parameters
            glucose_threshold = 140  # Threshold for high glucose level (mg/dl)
            systolic_threshold = 120  # Threshold for high systolic blood pressure (mmHg)
            heart_rate_threshold = 90  # Threshold for high heart rate (bpm)

            # Check if any health parameter exceeds the threshold and trigger alerts
            if glucose_level > glucose_threshold:
                # Your code to trigger an alert for high glucose level (e.g., send notification)
                print("Alert: High glucose level detected!")
            
            if blood_pressure > systolic_threshold:
                # Your code to trigger an alert for high blood pressure (e.g., send notification)
                print("Alert: High blood pressure detected!")
            
            if heart_rate > heart_rate_threshold:
                # Your code to trigger an alert for high heart rate (e.g., send notification)
                print("Alert: High heart rate detected!")

            time.sleep(60)  # Sleep for 60 seconds before checking again

    # Start monitoring health parameters in the background
    monitor_thread = Thread(target=monitor_health)
    monitor_thread.daemon = True  # Set daemon to True to terminate thread when main program exits
    monitor_thread.start()
    st.markdown('<h1 style="color: orange;font-family: DyeLine; text-align: center;">Personal Health Monitoring and Prediction System</h1>', unsafe_allow_html=True)


    # Load the saved models
    diabetes_model = pickle.load(open('C:/myproject/Saved models/diabetes_model.sav', 'rb'))
    heart_disease_model = pickle.load(open('C:/myproject/Saved models/diabetes_model.sav', 'rb'))

    # Load the audio files
    diabetic_audio_path = "C:/myproject/Audio/Diabetic.wav"
    diabetic_sound, _ = sf.read(diabetic_audio_path)

    non_diabetic_audio_path = "C:/myproject/Audio/Non_Diabetic.wav"
    non_diabetic_sound, _ = sf.read(non_diabetic_audio_path)

    heart_disease_audio_path = "C:/myproject/Audio/HeartDisease.wav"
    heart_disease_sound, _ = sf.read(heart_disease_audio_path)

    non_heart_disease_audio_path = "C:/myproject/Audio/Not_HeartDisease.wav"
    non_heart_disease_sound, _ = sf.read(non_heart_disease_audio_path)

    Invalid_details_audio_path = "C:/myproject/Audio/Invalid_details.wav"
    Invalid_details, _ = sf.read(Invalid_details_audio_path)

    # Sidebar for navigation
    with st.sidebar:
        selected = option_menu('Health Monitoring and Prediction System',
                            ['Predict Diseases by Symptoms','Diabetes Prediction', 'Heart Disease Prediction', 'Medicine Recommendations','Find Healthcare Providers'],
                            menu_icon='hospital-fill',
                            icons=['activity', 'heart', 'person'],
                            default_index=0)
        

    def voice_input():
        r = sr.Recognizer()
        with sr.Microphone() as source:
            st.write("Listening for voice input...")
            audio = r.listen(source)
        
        try:
            text = r.recognize_google(audio)
            return text
        except sr.UnknownValueError:
            st.write("Sorry, I could not understand what you said.")
            return ""
        except sr.RequestError as e:
            st.write(f"Could not request results from Google Speech Recognition service; {e}")
            return ""
    # Enable voice input checkbox
    voice_input_enabled = st.checkbox("Enable Voice Input")

    # If voice input is enabled, listen for voice input and display the recognized text
    if voice_input_enabled:
        voice_input_text = voice_input()
        st.write("Voice Input Text:", voice_input_text)
        
        
        

    # If "Predict Diseases by Symptoms" is selected
    if selected == 'Predict Diseases by Symptoms':
        # Page title
        st.markdown('<h2 style="color: green;">Predict Diseases by Symptoms</h2>', unsafe_allow_html=True)
        
        # Get symptoms input from the user
        symptoms = st.text_input('Enter your symptoms (comma-separated)', help='e.g., fever, cough, headache')
        
        # Code for predicting diseases based on symptoms
        if st.button('Predict'):
            # Process the symptoms input and predict diseases
            
            # Example: Processing symptoms input
            symptom_list = symptoms.split(',')
            
            # Example: Predicting diseases based on symptoms
            predicted_diseases = []
            
            # Add code here to predict diseases based on symptoms
            
            # Example: Display predicted diseases
            if predicted_diseases:
                st.subheader('Predicted Diseases:')
                for disease in predicted_diseases:
                    st.write(disease)
            else:
                st.write('No diseases predicted based on the provided symptoms.')



    # Diabetes Prediction Page
    if selected == 'Diabetes Prediction':
        # Page title
        st.markdown('<h2 style="color: green;">Diabetes Prediction using ML</h2>', unsafe_allow_html=True)

        # Getting the input data from the user
        col1, col2, col3 = st.columns(3)

        with col1:
            Pregnancies = st.text_input('Number of Pregnancies')

        with col2:
            Glucose = st.text_input('Glucose Level')

        with col3:
            BloodPressure = st.text_input('Blood Pressure value')

        with col1:
            SkinThickness = st.text_input('Skin Thickness value')

        with col2:
            Insulin = st.text_input('Insulin Level')

        with col3:
            BMI = st.text_input('BMI value')

        with col1:
            DiabetesPedigreeFunction = st.text_input('Diabetes Pedigree Function value')

        with col2:
            Age = st.text_input('Age of the Person')

        # Code for Prediction
        

        # Creating a button for Prediction
        if st.button('Diabetes Test Result'):
            if all(input_value.strip() for input_value in [Pregnancies, Glucose, BloodPressure, SkinThickness, Insulin, BMI, DiabetesPedigreeFunction, Age]):
                user_input = [float(Pregnancies), float(Glucose), float(BloodPressure), float(SkinThickness), float(Insulin), float(BMI), float(DiabetesPedigreeFunction), float(Age)]
                diab_prediction = diabetes_model.predict([user_input])

                if diab_prediction[0] == 1:
                    diab_diagnosis = 'The person is diabetic'
                    sd.play(np.array(diabetic_sound))  # Play diabetic sound effect
                else:
                    diab_diagnosis = 'The person is not diabetic'
                    sd.play(np.array(non_diabetic_sound))  # Play non-diabetic sound effect
            else:
                diab_diagnosis = 'Please enter valid details'
                sd.play(np.array(Invalid_details))  # Play an empty sound effect

        st.success(diab_diagnosis)
        if diab_diagnosis.startswith('The person is diabetic'):
            # Display common risk factors and symptoms of diabetes
            st.subheader('Common Risk Factors and Symptoms of Diabetes')
        if st.button('Patient Record'):
                st.subheader('Input Features:')
                st.write("Number of Pregnancies:", Pregnancies)
                st.write("Glucose Level:", Glucose)
                st.write("Blood Pressure value:", BloodPressure)
                st.write("Skin Thickness value:", SkinThickness)
                st.write("Insulin Level:", Insulin)
                st.write("BMI value:", BMI)
                st.write("Diabetes Pedigree Function value:", DiabetesPedigreeFunction)
                st.write("Age of the Person:", Age)
        
        # Add relevant text or bullet points with information about risk factors and symptoms

        # Display preventive measures and treatment options for diabetes
        st.subheader('Preventive Measures and Treatment Options for Diabetes')
        # Add relevant text or bullet points with information about lifestyle changes, medication, etc.

        # Display support resources and educational materials for diabetes
        st.subheader('Support Resources and Educational Materials for Diabetes')
        # Add links or resources to relevant websites, articles, or support groups
        # Display input features upon clicking the "Patient Records" button
        # Display buttons horizontally for "Patient Records" and "Disease Description"
        col1, col2, col3, col4 = st.columns([2,2,3,1])
        with col1:
            if st.button('Patient Records'):
                st.subheader('Input Features:')
                st.write("Number of Pregnancies:", Pregnancies)
                st.write("Glucose Level:", Glucose)
                st.write("Blood Pressure value:", BloodPressure)
                st.write("Skin Thickness value:", SkinThickness)
                st.write("Insulin Level:", Insulin)
                st.write("BMI value:", BMI)
                st.write("Diabetes Pedigree Function value:", DiabetesPedigreeFunction)
                st.write("Age of the Person:", Age)
        
        with col2:
            if st.button('Disease Description'):
                st.write("Diabetes is a chronic condition characterized by high levels of sugar (glucose) in the blood. It can lead to various complications such as heart disease, kidney failure, and blindness if not properly managed. Common symptoms include frequent urination, increased thirst, and unexplained weight loss. Treatment often involves lifestyle changes, medication, and regular monitoring of blood sugar levels.")
        with col3:
            if st.button('Educational Resources'):
                with st.expander("Videos"):
                    st.video("https://www.youtube.com/watch?v=XfyGv-xwjlI")
                    st.video("https://www.youtube.com/watch?v=69Kv9W62CSk")
                    st.write("Videos on diabetes or heart disease")
            
                # Option 2: Articles
                with st.expander("Articles"):
                    st.write("Articles on diabetes or heart disease")
        with col4:
            if st.button('articles'):
                st.write("Diabetes is a chronic condition characterized by high levels of sugar (glucose) in the blood. It can lead to various complications such as heart disease, kidney failure, and blindness if not properly managed. Common symptoms include frequent urination, increased thirst, and unexplained weight loss. Treatment often involves lifestyle changes, medication, and regular monitoring of blood sugar levels.")

            
    # Heart Disease Prediction Page
    if selected == 'Heart Disease Prediction':
        # Page title
        st.markdown('<h2 style="color: green;">Heart Disease Prediction using ML</h2>', unsafe_allow_html=True)

        col1, col2, col3 = st.columns(3)

        with col1:
            age = st.text_input('Age')

        with col2:
            sex = st.text_input('Sex')

        with col3:
            cp = st.text_input('Chest Pain types')

        with col1:
            trestbps = st.text_input('Resting Blood Pressure')

        with col2:
            chol = st.text_input('Serum Cholestoral in mg/dl')

        with col3:
            fbs = st.text_input('Fasting Blood Sugar > 120 mg/dl')

        with col1:
            restecg = st.text_input('Resting Electrocardiographic results')

        with col2:
            thalach = st.text_input('Maximum Heart Rate achieved')

        with col3:
            exang = st.text_input('Exercise Induced Angina')

        with col1:
            oldpeak = st.text_input('ST depression induced by exercise')

        with col2:
            slope = st.text_input('Slope of the peak exercise ST segment')

        with col3:
            ca = st.text_input('Major vessels colored by flourosopy')

        with col1:
            thal = st.text_input('thal: 0 = normal; 1 = fixed defect; 2 = reversable defect')

        # Code for Prediction
        heart_diagnosis = ''

        # Creating a button for Prediction
        if st.button('Heart Disease Test Result'):
            if all(input_value.strip() for input_value in [age, sex, cp, trestbps, chol, fbs, restecg, thalach, exang, oldpeak, slope, ca, thal]):
                user_input = [float(age), float(sex), float(cp), float(trestbps), float(chol), float(fbs), float(restecg), float(thalach), float(exang), float(oldpeak), float(slope), float(ca), float(thal)]
                heart_prediction = heart_disease_model.predict([user_input[:8]])

                if heart_prediction[0] == 1:
                    heart_diagnosis = 'The person is having heart disease'
                    sd.play(np.array(heart_disease_sound))  # Play heart disease sound effect
                else:
                    heart_diagnosis = 'The person does not have any heart disease'
                    sd.play(np.array(non_heart_disease_sound))  # Play non-heart disease sound effect
            else:
                heart_diagnosis = 'Please enter valid details'
                sd.play(np.array(Invalid_details))  # Play an empty sound effect

        st.success(heart_diagnosis)
        
    # Medicine Recommendation Page
    if selected == 'Medicine Recommendations':
        # Page title
        st.markdown('<h2 style="color: green;">Medicine Recommendations</h2>', unsafe_allow_html=True)

        # Check the selected disease prediction
        if diab_diagnosis.startswith('The person is diabetic'):
            # If diabetes is predicted, display recommended medicines for diabetes
            st.subheader('Recommended Medicines for Diabetes')
            st.write("1. Metformin")
            st.write("2. Insulin (if required)")
            st.write("3. Sulfonylureas (e.g., Glipizide)")
            st.write("4. DPP-4 inhibitors (e.g., Sitagliptin)")

        elif heart_diagnosis.startswith('The person is having heart disease'):
            # If heart disease is predicted, display recommended medicines for heart disease
            st.subheader('Recommended Medicines for Heart Disease')
            st.write("1. Aspirin")
            st.write("2. Beta-blockers (e.g., Metoprolol)")
            st.write("3. ACE inhibitors (e.g., Lisinopril)")
            st.write("4. Statins (e.g., Atorvastatin)")

        else:
            # If no specific disease is predicted, provide general information or prompt the user to enter more details
            st.write("Please select a disease prediction to see recommended medicines.")


    # Button for finding healthcare providers
    if selected == 'Find Healthcare Providers':
        # Add functionality to find and display nearby healthcare providers
        # This could include querying a database or using an API to fetch relevant information
        # Display the results in a user-friendly format, such as a list or interactive map
        st.header("Find Healthcare Providers Near You")
        
        # Add code here to fetch and display healthcare provider information
        
        # Example: Display a list of nearby hospitals and medical centers
        st.subheader("Hospitals and Medical Centers")
        st.write("1. Hospital ABC - 1.2 miles away")
        st.write("2. Medical Center XYZ - 2.5 miles away")
        
        # Example: Display a list of nearby doctors
        st.subheader("Doctors")
        st.write("1. Dr. Smith - Cardiologist")
        st.write("2. Dr. Johnson - Endocrinologist")

        # You can further enhance this functionality by adding filters, sorting options, or integrating with location-based services.

def css():
    st.markdown("""
    <style>
    .intro{
        text-align: justify;
    }
    </style>
    """, unsafe_allow_html=True)



def app():
    css()
    st.title(":orange[Brain Tumor] Detection Portal")
    c1, c2 = st.columns([2.5, 2], gap="small")
def show_login_page():
    app()
    st.sidebar.title("Login")
    email = st.sidebar.text_input("Email")
    password = st.sidebar.text_input("Password", type="password")
    if st.sidebar.button("Login"):
        if check_credentials(email, password):
            st.session_state.logged_in = True
            st.experimental_rerun()
        else:
            st.sidebar.error("Invalid Username/Password.")

def check_credentials(email, password):
    cursor=connection.cursor()
    query="SELECT * FROM users where email=%s AND password=%s"
    data=(email,password)
    cursor.execute(query,data)
    result=cursor.fetchone()
    cursor.close()
    if result:
        return True
    else:
        return False

if __name__ == "__main__":

    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False

    if st.session_state.logged_in:
        show_content()
        # Add logout button to sidebar
        if st.sidebar.button("Logout"):
            st.session_state.logged_in = False
    else:
        show_login_page()