# AI Registration Assistant

An AI-powered conversational chatbot designed to help students with internship-related queries and guide them through the internship registration process.

**Task ID:** AI-SS-001  
**Student Code:** DAS005540

---

## Project Overview

The AI Registration Assistant is a conversational AI application developed as part of the AI & Data Science internship task.

The chatbot uses Natural Language Processing (NLP) and Machine Learning techniques to understand user messages, identify their intent, extract registration information, validate user inputs, and guide students through the registration process.

The project also includes a Streamlit-based web interface for interacting with the chatbot.

---

## Objectives

The main objectives of this project are:

- Implement NLP-based text preprocessing.
- Classify user messages into different intents.
- Extract entities such as name, email, and field of study.
- Implement conversational dialog management.
- Validate user registration information.
- Store registration data in JSON format.
- Provide answers to frequently asked questions.
- Integrate the chatbot with a web-based user interface.

---

## Features

### 1. Natural Language Processing

The chatbot preprocesses user input using NLP techniques such as:

- Text normalization
- Tokenization
- Stopword removal
- Lemmatization

NLTK is used for the NLP preprocessing pipeline.

### 2. Intent Classification

The chatbot identifies the purpose of a user's message using:

- TF-IDF Vectorization
- Logistic Regression

The system supports intents such as:

- Greeting
- Registration
- FAQ
- Help
- Goodbye

### 3. Entity Extraction

The chatbot extracts important information from user messages, including:

- Name
- Email address
- Field of study / area of interest

### 4. Registration Workflow

The chatbot guides users through a step-by-step registration process:

1. Start registration
2. Collect name
3. Collect email
4. Collect field of study
5. Validate the provided information
6. Ask for confirmation
7. Save the registration

### 5. Input Validation

The system validates user-provided information such as email addresses and handles invalid inputs by asking the user to provide the information again.

### 6. FAQ Support

The chatbot can answer basic questions related to:

- Internship overview
- Registration requirements
- Technologies used
- Available fields
- Project and chatbot functionality

Quick FAQ buttons are also available in the Streamlit interface.

### 7. JSON Data Storage

Completed registrations are stored in:

```text
registrations.json