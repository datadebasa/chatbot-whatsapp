from flask import Flask, jsonify, request
import requests, markdown
app = Flask(__name__)

class FonteSetup():
    def __init__(self):
        self._token = ''

    def set_token(self, token):
        self._token = token
        
    def send_message(self, data):  
        endpoint = 'https://api.fonnte.com/send'      
        headers = {
            "Authorization":self._token
        }

        payload = {
            'target':data.get('target'),
            'message':data.get('message'),
        }
        response = requests.post(endpoint, headers=headers, data=payload)
        pass

class chatBootSetup():
    def __init__(self):
        self._endpoint = 'https://chat-boot-wa.vercel.app/generate'

    def get_message(self, prompt):
        enpoint = f'{self._endpoint}?promt={prompt}'
        response = requests.get(enpoint)
        if response.status_code == 200:
            return response.json().get('payload').get('response')
        else:
            return None
# boot_contig = chatBootSetup()
# response = boot_contig.get_message('aku putus sama cewek aku?')            
# print(response)

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.is_json:
        data = request.get_json()
        sender = data.get("sender")
        message = data.get("message")
        if message.startswith('ai:'):
            token = request.args.get('token')
            fonte_setup = FonteSetup()
            boot_contig = chatBootSetup()
            response = boot_contig.get_message(message)
            

            data = {
                'message':response,
                'target':sender,
            }
            fonte_setup.set_token('o1AY55mzsCxZtHcUbbut')

            fonte_setup.send_message(data)
            return jsonify({"status": "success", "message": "Message sent"})
    else:
        return jsonify({"status": "error", "message": "Invalid request format"})
                    

@app.route('/about')
def about():
    return 'About'

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)