import re
import json
import nltk

from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression


# -----------------------------------------
# 1. NLP PREPROCESSING
# -----------------------------------------

lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words("english"))


def preprocess(text):
    """
    Convert user text into a cleaner form for NLP.
    """

    text = text.lower()

    # Keep only letters and spaces
    text = re.sub(r"[^a-zA-Z\s]", "", text)

    # Tokenization
    words = text.split()

    # Remove stopwords and perform lemmatization
    words = [
        lemmatizer.lemmatize(word)
        for word in words
        if word not in stop_words
    ]

    return " ".join(words)


# -----------------------------------------
# 2. TRAINING DATA FOR INTENT CLASSIFICATION
# -----------------------------------------

training_sentences = [
    # Greeting
    "hello",
    "hi",
    "hey",
    "good morning",
    "good afternoon",

    # Registration
    "I want to register",
    "I want to join the internship",
    "how can I register",
    "I want to apply",
    "register me",

    # FAQ
    "what is this internship",
    "tell me about the internship",
    "what is AI internship",
    "what does this internship offer",
    "what is the internship about",
    "how does the internship work",
    "what is this project",
    "what technologies are used",
    "what information is required",
    "what do I need for registration",
    "what fields are available",
    "how does the chatbot work",

    # Help
    "help",
    "what can you do",
    "I need help",

    # Goodbye
    "thank you",
    "thanks",
    "bye",
    "goodbye"
]

training_labels = [
    # Greeting - 5
    "greeting",
    "greeting",
    "greeting",
    "greeting",
    "greeting",

    # Registration - 5
    "registration",
    "registration",
    "registration",
    "registration",
    "registration",

    # FAQ - 12
    "faq",
    "faq",
    "faq",
    "faq",
    "faq",
    "faq",
    "faq",
    "faq",
    "faq",
    "faq",
    "faq",
    "faq",

    # Help - 3
    "help",
    "help",
    "help",

    # Goodbye - 4
    "goodbye",
    "goodbye",
    "goodbye",
    "goodbye"
]


# -----------------------------------------
# 3. TRAIN INTENT CLASSIFICATION MODEL
# -----------------------------------------

processed_sentences = [
    preprocess(sentence)
    for sentence in training_sentences
]

vectorizer = TfidfVectorizer()

X = vectorizer.fit_transform(processed_sentences)

model = LogisticRegression(max_iter=1000)

model.fit(X, training_labels)


def predict_intent(text):
    """
    Predict the user's intent.
    """

    processed_text = preprocess(text)

    vector = vectorizer.transform([processed_text])

    prediction = model.predict(vector)[0]

    return prediction


# -----------------------------------------
# 4. ENTITY EXTRACTION
# -----------------------------------------

def extract_email(text):
    """
    Extract email address from user input.
    """

    pattern = r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}"

    match = re.search(pattern, text)

    if match:
        return match.group()

    return None


def extract_name(text):
    """
    Extract name from phrases such as:
    'my name is Rahul'
    'I am Rahul'
    """

    patterns = [
        r"my name is ([A-Za-z ]+)",
        r"i am ([A-Za-z ]+)",
        r"i'm ([A-Za-z ]+)"
    ]

    for pattern in patterns:

        match = re.search(pattern, text, re.IGNORECASE)

        if match:
            return match.group(1).strip()

    return None


def extract_field(text):
    """
    Extract a study/interest field.
    """

    fields = [
        "computer science",
        "data science",
        "artificial intelligence",
        "machine learning",
        "information technology",
        "electronics",
        "mechanical",
        "civil"
    ]

    text_lower = text.lower()

    for field in fields:

        if field in text_lower:
            return field.title()

    return None


# -----------------------------------------
# 5. VALIDATION
# -----------------------------------------

def valid_email(email):
    """
    Check whether email format is valid.
    """

    pattern = r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"

    return re.match(pattern, email) is not None


# -----------------------------------------
# 6. REGISTRATION ASSISTANT
# -----------------------------------------

class RegistrationAssistant:

    def __init__(self):

        self.student_data = {
            "name": None,
            "email": None,
            "field": None
        }

        self.registration_started = False
        self.current_step = None


    def start_registration(self):

        self.registration_started = True
        self.current_step = "name"

        return (
            "Sure! I can help you with internship registration.\n"
            "First, please tell me your name."
        )


    def handle_registration(self, user_input):

        # -------------------------
        # NAME
        # -------------------------

        if self.current_step == "name":

            name = extract_name(user_input)

            if not name:

                # If user simply types a name
                if len(user_input.split()) <= 4:
                    name = user_input.strip()

            if name:

                self.student_data["name"] = name.title()

                self.current_step = "email"

                return (
                    f"Nice to meet you, {self.student_data['name']}!\n"
                    "Please enter your email address."
                )

            return "Please enter your name."


        # -------------------------
        # EMAIL
        # -------------------------

        if self.current_step == "email":

            email = extract_email(user_input)

            if email and valid_email(email):

                self.student_data["email"] = email

                self.current_step = "field"

                return (
                    "Email saved successfully.\n"
                    "What is your field of study or area of interest?"
                )

            return (
                "That email does not look valid.\n"
                "Please enter a valid email such as student@example.com"
            )


        # -------------------------
        # FIELD
        # -------------------------

        if self.current_step == "field":

            field = extract_field(user_input)

            if field:

                self.student_data["field"] = field

                self.current_step = "confirmation"

                return (
                    f"Got it. Your field is {field}.\n\n"
                    "Please confirm your details:\n"
                    f"Name: {self.student_data['name']}\n"
                    f"Email: {self.student_data['email']}\n"
                    f"Field: {self.student_data['field']}\n\n"
                    "Type 'yes' to confirm or 'no' to restart."
                )

            return (
                "Please mention your field, for example "
                "Computer Science, Data Science, or AI."
            )


        # -------------------------
        # CONFIRMATION
        # -------------------------

        if self.current_step == "confirmation":

            answer = user_input.lower().strip()

            if answer in ["yes", "y", "confirm", "confirmed"]:

                self.save_registration()

                self.registration_started = False
                self.current_step = None

                return (
                    "Registration successful!\n"
                    "Your information has been saved.\n"
                    "Thank you for registering."
                )

            if answer in ["no", "n"]:

                self.student_data = {
                    "name": None,
                    "email": None,
                    "field": None
                }

                self.current_step = "name"

                return "No problem. Let's start again. What is your name?"

            return "Please type 'yes' to confirm or 'no' to restart."


    # -----------------------------------------
    # SAVE DATA TO JSON
    # -----------------------------------------

    def save_registration(self):

        try:

            with open("registrations.json", "r") as file:
                registrations = json.load(file)

        except (FileNotFoundError, json.JSONDecodeError):

            registrations = []

        registrations.append(self.student_data)

        with open("registrations.json", "w") as file:

            json.dump(
                registrations,
                file,
                indent=4
            )


# -----------------------------------------
# 7. CHATBOT
# -----------------------------------------

assistant = RegistrationAssistant()


def chatbot_response(user_input):

    # If registration is currently active,
    # continue registration flow.

    if assistant.registration_started:

        return assistant.handle_registration(user_input)


    intent = predict_intent(user_input)


    if intent == "greeting":

        return (
            "Hello! I am the AI Registration Assistant.\n"
            "I can help you register for the internship."
        )


    if intent == "registration":

        return assistant.start_registration()


    if intent == "faq":
        text = user_input.lower()

        if "technology" in text or "technologies" in text:
            return (
                "This project uses Python, NLTK, Scikit-learn, "
                "TF-IDF vectorization, Logistic Regression, "
                "Streamlit, and JSON for data storage."
            )

        if "information" in text or "required" in text:
            return (
                "For registration, I need three basic details:\n"
                "• Name\n"
                "• Email address\n"
                "• Field of study or area of interest"
            )

        if "field" in text:
            return (
                "Currently supported fields include:\n"
                "• Computer Science\n"
                "• Data Science\n"
                "• Artificial Intelligence\n"
                "• Machine Learning\n"
                "• Information Technology\n"
                "• Electronics\n"
                "• Mechanical\n"
                "• Civil"
            )

        if "chatbot" in text or "project" in text:
            return (
                "This AI Registration Assistant uses NLP to understand "
                "user messages, classify their intent, extract registration "
                "details, and guide students through the registration process."
            )

        return (
            "This internship project focuses on an AI Registration Assistant "
            "that helps students with basic queries and guides them through "
            "the internship registration process.\n\n"
            "You can ask about the internship, required information, "
            "technologies, available fields, or start registration."
        )    


    if intent == "help":

        return (
            "I can help you with internship registration.\n"
            "You can say 'I want to register' to begin."
        )


    if intent == "goodbye":

        return "Goodbye! Best of luck with your internship."


    return (
        "Sorry, I didn't understand that.\n"
        "Try saying 'I want to register' or 'help'."
    )


# -----------------------------------------
# 8. RUN CHATBOT
# -----------------------------------------

print("=" * 50)
print("       AI REGISTRATION ASSISTANT")
print("=" * 50)

print("Type 'bye' to exit.\n")


if __name__ == "__main__":
    while True:
        user_input = input("You: ")

        if user_input.lower().strip() == "bye":
            print("Bot:", chatbot_response("bye"))
            break

        response = chatbot_response(user_input)
        print("Bot:", response)