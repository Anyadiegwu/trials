# # import os
# # import json
# # import requests
# # from flask import Flask, request, render_template, session
# # from dotenv import load_dotenv

# # load_dotenv()  # Load .env for local dev

# # app = Flask(__name__)
# # app.secret_key = os.getenv('SECRET_KEY', 'your_secret_key_here')  # For sessions; set in .env or Render

# # # Your Gemini API setup (from original code)
# # class AiAssistant:
# #     def __init__(self, api_endpoint, api_key, default_model):
# #         self.api_endpoint = api_endpoint
# #         self.api_key = api_key
# #         self.default_model = default_model

# #     def call_with_prompt(self, prompt, model=None):
# #         url = f"{self.api_endpoint}?key={self.api_key}"
# #         payload = {
# #             "contents": [{"role": "user", "parts": [{"text": prompt}]}],
# #             "generationConfig": {"temperature": 0.3}
# #         }
# #         headers = {"Content-Type": "application/json"}
# #         try:
# #             response = requests.post(url, headers=headers, json=payload)
# #             response.raise_for_status()
# #             result = response.json()
# #             return result['candidates'][0]['content']['parts'][0]['text']
# #         except Exception as e:
# #             return f"Error: {e}"

# # gemini_api_url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-lite:generateContent"
# # gemini_api_key = os.getenv('GEMINI_API_KEY')
# # gemi = AiAssistant(gemini_api_url, gemini_api_key, "gemini-2.5-flash-lite")

# # # Categories (from original)
# # categories = """
# # Classify the user’s main banking need into one of these categories:
# # - Account Opening
# # - Billing Issue
# # - Account Access
# # - Transaction Inquiry
# # - Card Services
# # - Account Statement
# # - Loan Inquiry
# # - General Information
# # """

# # # Home route: Show chat interface
# # @app.route('/', methods=['GET', 'POST'])
# # def chat():
# #     if 'context_data' not in session:
# #         session['context_data'] = {}
# #         session['predicted_category'] = None
# #         session['conversation'] = ["Assistant: Hello! Welcome. I'm your secure AI banking assistant. How can I help you today?"]

# #     if request.method == 'POST':
# #         userInput = request.form['userInput'].strip()
# #         if userInput.lower() in ["exit", "quit", "stop"]:
# #             session.clear()
# #             return render_template('chat.html', conversation=["Assistant: Goodbye! Have a great day!"])

# #         # Extract details (prompt1 - no context for extraction)
# #         prompt1 = f"""You are a friendly precise requirements-extraction assistant for a bank. Always:
# # - Do NOT output JSON, code, or field names.
# # - The reply must be plain conversational text only.
# # - Prefer structured JSON output when extracting facts.
# # - If the user input is ambiguous, list ambiguous items and ask for clarification.
# # - Keep follow-up questions short (1 question at a time).
# # - Always include a human-readable one-sentence summary after the JSON.
# # - When asking follow-ups, reference the JSON keys you want filled.
# # - Respect user privacy; never store personal data unless explicitly asked.

# # User message:
# # {userInput}
# # """
# #         extracted_detail = gemi.call_with_prompt(prompt1)

# #         # Parse JSON and update context
# #         try:
# #             start = extracted_detail.find("{")
# #             end = extracted_detail.rfind("}") + 1
# #             if start != -1 and end > start:
# #                 json_str = extracted_detail[start:end]
# #                 new_data = json.loads(json_str)
# #                 if isinstance(new_data, dict):
# #                     session['context_data'].update(new_data)
# #         except:
# #             pass

# #         # Classify only if first message or not set
# #         if session['predicted_category'] is None:
# #             prompt2 = f"""You are an intent classification assistant for a banking support chatbot.

# # Select the single most relevant category that matches the user's intent.
# # Use only the categories from the provided list.
# # If no category fits, return "Unclear".

# # Categories:
# # {categories}

# # User message:
# # {userInput}
# # """
# #             session['predicted_category'] = gemi.call_with_prompt(prompt2).strip()

# #         # Controller (prompt3 with full context)
# #         prompt3 = f"""You are the controller assistant that manages outputs from two other banking AI components.

# # You will be given:
# # 1. The FULL extracted details so far (cumulative context).
# # 2. The predicted category.

# # Your task:
# # - Do NOT output JSON, code, or field names.
# # - The reply must be plain conversational text only.
# # - Identify if any important fields are missing or ambiguous for the category: {session['predicted_category']}
# # - Decide the next system action:
# #     - "ask follow up" if key fields are missing or ambiguous
# #     - "route to handler" if data is sufficient for the selected category
# #     - "unclear" if intent is still uncertain
# # - If asking follow-up, make it ONE short, natural question referencing the missing field.
# # - Do NOT invent details.

# # Cumulative Extracted Context:
# # {json.dumps(session['context_data'], indent=2)}

# # Current User Message:
# # {userInput}

# # Category: {session['predicted_category']}
# # """
# #         response = gemi.call_with_prompt(prompt3)

# #         # Append to conversation
# #         session['conversation'].append(f"You: {userInput}")
# #         session['conversation'].append(f"Assistant: {response}")

# #     return render_template('chat.html', conversation=session['conversation'])

# # if __name__ == '__main__':
# #     app.run(debug=True)

# import re
# import json
# import requests
# import os
# from flask import Flask, request, render_template, session
# from dotenv import load_dotenv

# load_dotenv()  # Load .env for local dev

# app = Flask(__name__)
# app.secret_key = os.getenv('SECRET_KEY', 'your_secret_key_here') 

# class AiAssitant:
#       def __init__(self, api_endpoint, api_key, default_model):
#           self.api_endpoint = api_endpoint
#           self.api_key = api_key
#           self.default_model = default_model

#       def call_with_prompt(self, prompt, model=None):
#           url = f"{self.api_endpoint}?key={self.api_key}"

#           payload = {
#               "contents": [
#                   {
#                       "role": "user",
#                       "parts": [{"text": prompt}]
#                   }
#               ],
#               "generationConfig": {
#                   "temperature": 0.3
#               }
#           }

#           headers = {
#               "Content-Type": "application/json"
#           }

#           try:
#               response = requests.post(url, headers=headers, json=payload)
#               response.raise_for_status()
#               result = response.json()
#               return result['candidates'][0]['content']['parts'][0]['text']
#           except requests.exceptions.RequestException as e:
#               print(f"Error: {e}")
#               return None
#           except (KeyError, IndexError):
#               print("Unexpected response format:", response.text)
#               return None




# gemini_api_url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-lite:generateContent"
# gemini_api_key = os.getenv('GEMINI_API_KEY')
# gemi = AiAssitant(gemini_api_url, gemini_api_key, "gemini-2.5-flash-lite")



# categories = """
#     Classify the user’s main banking need into one of these categories:
#     - Account Opening
#     - Billing Issue
#     - Account Access
#     - Transaction Inquiry
#     - Card Services
#     - Account Statement
#     - Loan Inquiry
#     - General Information
#   """

# @app.route('/',methods=['GET', 'POST'])
# def run_prompt_chain():
#     if 'context_data' not in session:
#         session['context_data'] = {}
#         session['predicted_category'] = None
#         session['conversation'] = ["Assistant: Hello! Welcome. I'm your secure AI banking assistant. How can I help you today?"]
# #   print("Bank Assistant initialized. Type 'exit' anytime to quit.\n")

#     if request.method == 'POST':
#         userInput = request.form['userInput'].strip()
#         if userInput.lower() in ["exit", "quit", "stop"]:
#             session.clear()
#             return render_template('chat.html', conversation=["Assistant: Goodbye! Have a great day!"])

#         prompt1 = f"""
#         You are a friendly precise requirements-extraction assistant for a bank. Always:
#       - Do NOT output JSON, code, or field names.
#       - The reply must be plain conversational text only.
#       - Prefer structured JSON output when extracting facts.
#       - If the user input is ambiguous, list ambiguous items and ask for clarification.
#       - Keep follow-up questions short (1 question at a time).
#       - Always include a human-readable one-sentence summary after the JSON.
#       - When asking follow-ups, reference the JSON keys you want filled.
#       - Respect user privacy; never store personal data unless explicitly asked.

#       User message:
#       {userInput}
#       """

#         extracted_detail = gemi.call_with_prompt(prompt1)

#         try:
#             # new_data = json.loads(json_text)
#             start = extracted_detail.find("{")
#             end = extracted_detail.rfind("}") + 1
#             if start != -1 and end > start:
#                 json_str = extracted_detail[start:end]
#                 new_data = json.loads(json_str)
#                 if isinstance(new_data, dict):
#                     session['context_data'].update(new_data)
#             # if isinstance(new_data, dict):
#             #     context_data.update(new_data)
#         except:
#             pass
#         if session['predicted_category'] is None:
#             prompt2 = f"""
#       You are an intent classification assistant for a banking support chatbot.

#       You will be given:
#       1. A list of possible categories (in plain text)
#       2. A user message.

#       Your job is to:
#       - Select the single most relevant category that matches the user’s intent.
#       - Use only the categories from the provided list.
#       - If no category fits, return "Unclear".
#       - Never output explanations, reasoning, or JSON fields not requested.
#       ```
#       {categories}
#       ```
#       ```
#       {userInput}
#       ```
#       """
#             session['predicted_category'] = gemi.call_with_prompt(prompt2).strip()
#         prompt3 = f"""
#     You are the controller assistant that manages outputs from two other banking AI components.

#     You will be given:
#     1. User's latest message.
#     2. The predicted category (from the classification assistant).
#     3. The previous conversation context.

#     Your task:
#     - Do NOT output JSON, code, or field names.
#     - The reply must be plain conversational text only.
#     - Review the predicted category and previous context.
#     - Identify if any important fields are missing or ambiguous.
#     - Ask ONLY for fields that are still missing or empty in the context.
#     - If all required info is collected, confirm and route to handler.
#     - Decide the next system action:
#         - "ask follow up" → if key fields are missing or ambiguous
#         - "route to handler" → if data is sufficient for the selected category
#         - "unclear" → if both extraction and classification are uncertain
#     - Do NOT invent details not found in the inputs.

#     Previous conversation context:
#     {json.dumps(session["context_data"], indent=2)}


#     Predicted category:
#     {session['predicted_category']}

#     User's latest message:
#     {userInput}

#     """
#         controller_response = gemi.call_with_prompt(prompt3)
#         # print(controller_response)
#         session['conversation'].append(f"You: {userInput}")
#         session['conversation'].append(f"Assistant: {controller_response}")
#         # controller_data = {}
#     return render_template('chat.html', conversation=session['conversation'])

# if __name__ == '__main__':
#     app.run(debug=True)

   
import os
import re
import json
import requests
from flask import Flask, request, jsonify, render_template_string
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

class AiAssistant:
    def __init__(self, api_endpoint, api_key, default_model):
        self.api_endpoint = api_endpoint
        self.api_key = api_key
        self.default_model = default_model

    def call_with_prompt(self, prompt, model=None):
        url = f"{self.api_endpoint}?key={self.api_key}"
        payload = {
            "contents": [{"role": "user", "parts": [{"text": prompt}]}],
            "generationConfig": {"temperature": 0.3}
        }
        headers = {"Content-Type": "application/json"}
        
        try:
            response = requests.post(url, headers=headers, json=payload)
            response.raise_for_status()
            result = response.json()
            return result['candidates'][0]['content']['parts'][0]['text']
        except Exception as e:
            print(f"Error: {e}")
            return None

# Initialize AI Assistant
gemini_api_url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-lite:generateContent"
gemini_api_key = os.getenv('GEMINI_API_KEY')
gemi = AiAssistant(gemini_api_url, gemini_api_key, "gemini-2.5-flash-lite")

categories = """
- Account Opening
- Billing Issue
- Account Access
- Transaction Inquiry
- Card Services
- Account Statement
- Loan Inquiry
- General Information
"""

# Store sessions (in production, use Redis or database)
sessions = {}

@app.route('/')
def home():
    html = '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Bank AI Assistant</title>
        <style>
            body { font-family: Arial, sans-serif; max-width: 800px; margin: 50px auto; padding: 20px; }
            #chat-box { border: 1px solid #ccc; height: 400px; overflow-y: auto; padding: 15px; margin-bottom: 20px; background: #f9f9f9; }
            .message { margin: 10px 0; padding: 10px; border-radius: 5px; }
            .user { background: #007bff; color: white; text-align: right; }
            .bot { background: #e9ecef; }
            #user-input { width: 80%; padding: 10px; }
            #send-btn { width: 18%; padding: 10px; background: #007bff; color: white; border: none; cursor: pointer; }
            #send-btn:hover { background: #0056b3; }
        </style>
    </head>
    <body>
        <h1>🏦 Bank AI Assistant</h1>
        <div id="chat-box"></div>
        <input type="text" id="user-input" placeholder="Type your message..." />
        <button id="send-btn" onclick="sendMessage()">Send</button>

        <script>
            let sessionId = Math.random().toString(36).substring(7);
            
            window.onload = function() {
                addBotMessage("Hello! Welcome. I'm your secure AI banking assistant. How can I help you today?");
            };

            function addBotMessage(message) {
                const chatBox = document.getElementById('chat-box');
                chatBox.innerHTML += '<div class="message bot"><strong>Bot:</strong> ' + message + '</div>';
                chatBox.scrollTop = chatBox.scrollHeight;
            }

            function addUserMessage(message) {
                const chatBox = document.getElementById('chat-box');
                chatBox.innerHTML += '<div class="message user"><strong>You:</strong> ' + message + '</div>';
                chatBox.scrollTop = chatBox.scrollHeight;
            }

            async function sendMessage() {
                const input = document.getElementById('user-input');
                const message = input.value.trim();
                
                if (!message) return;
                
                addUserMessage(message);
                input.value = '';

                try {
                    const response = await fetch('/chat', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ message: message, session_id: sessionId })
                    });
                    
                    const data = await response.json();
                    addBotMessage(data.response);
                } catch (error) {
                    addBotMessage('Sorry, an error occurred. Please try again.');
                }
            }

            document.getElementById('user-input').addEventListener('keypress', function(e) {
                if (e.key === 'Enter') sendMessage();
            });
        </script>
    </body>
    </html>
    '''
    return render_template_string(html)

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_input = data.get('message', '')
    session_id = data.get('session_id', 'default')
    
    # Initialize session if new
    if session_id not in sessions:
        sessions[session_id] = {
            'context_data': {},
            'predicted_category': None,
            'conversation_history': []
        }
    
    session = sessions[session_id]
    
    # Extract details
    prompt1 = f"""
    You are a precise requirements-extraction assistant for a bank.
    Extract key information from the user's message as a JSON object.
    
    Current context: {json.dumps(session['context_data'], indent=2)}
    User message: {user_input}
    
    Output ONLY a JSON object.
    """
    
    extracted_detail = gemi.call_with_prompt(prompt1)
    new_data = {}
    match = re.search(r'(\{.*\})', extracted_detail, re.DOTALL)
    if match:
        try:
            new_data = json.loads(match.group())
            for key, value in new_data.items():
                if value:
                    session['context_data'][key] = value
        except:
            pass
    
    # Classify category
    if session['predicted_category'] is None:
        prompt2 = f"""
        Classify this banking request into one category:
        {categories}
        
        User message: {user_input}
        Return ONLY the category name.
        """
        session['predicted_category'] = gemi.call_with_prompt(prompt2).strip()
    
    # Controller
    prompt3 = f"""
    You are a banking conversation controller.
    
    Category: {session['predicted_category']}
    Collected info: {json.dumps(session['context_data'], indent=2)}
    User message: {user_input}
    
    Required for Account Opening: full_name, date_of_birth, address, account_type
    
    - Do NOT ask for information already collected
    - Ask for ONE missing field at a time
    - If all info collected, say "All information collected. Routing to handler."
    
    Already collected: {', '.join(session['context_data'].keys())}
    """
    
    controller_response = gemi.call_with_prompt(prompt3)
    
    session['conversation_history'].append({
        'user_input': user_input,
        'response': controller_response
    })
    
    return jsonify({'response': controller_response})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)