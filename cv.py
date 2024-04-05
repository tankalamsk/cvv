#!/usr/bin/env python
# coding: utf-8

# In[17]:


import base64
import os
import io
import google.generativeai as genai


# In[18]:


from flask import Flask, render_template, request
import fitz  # PyMuPDF
#import genai  # Assuming you have installed the GenAI library

app = Flask(__name__)

# Configure GenAI with your API key
genai.configure(api_key="AIzaSyCnuWGt-UsF21XWMeVKJH_B0NmWvOqBXas")

# Function to extract text from PDF
def extract_text_from_pdf(file_path):
    text = ""
    doc = fitz.open(file_path)
    for page in doc:
        text += page.get_text()
    return text

# Function to process CV and job description
def process_cv_and_job_description(pdf_content, input_text):
    jd_cv = input_text + pdf_content
    return jd_cv

# Function to get response from GenAI
def get_gemini_response(jd_cv, prompt):
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(prompt + jd_cv)  # Use jd_cv directly
    return response

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Handle file upload
        resume_file = request.files['resume']
        job_description = request.form['job_description']

        # Save the uploaded resume
        upload_folder = 'uploads'
        if not os.path.exists(upload_folder):
            os.makedirs(upload_folder)
        resume_file_path = os.path.join(upload_folder, resume_file.filename)
        resume_file.save(resume_file_path)

        # Extract text from PDF
        pdf_content = extract_text_from_pdf(resume_file_path)

        # Process CV and job description
        jd_cv = process_cv_and_job_description(pdf_content, job_description)

        # Get response from GenAI
        input_prompt1 = """
        I am providing the job description. Parse the job description and the CV and check whether the job description matches the CV or not.
        Check the job description that I am providing here, and lastly provide the number of skills matching and multiply by 100.
        """
        response1 = get_gemini_response(jd_cv, input_prompt1)
        response_text = response1.text

        return render_template('result.html', response=response_text)

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)


# In[ ]:



