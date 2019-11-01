from flask import Flask, render_template, request
from werkzeug import secure_filename
import os, json, requests

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = '/tmp/'


# set to your own subscription key value
subscription_key = os.getenv('face_key')
assert subscription_key

# replace <My Endpoint String> with the string from your endpoint URL
face_api_url = 'https://westeurope.api.cognitive.microsoft.com/face/v1.0/detect'

image_url = 'https://upload.wikimedia.org/wikipedia/commons/3/37/Dagestani_man_and_woman.jpg'

headers = {'Ocp-Apim-Subscription-Key': subscription_key}

params = {
    'returnFaceId': 'true',
    'returnFaceLandmarks': 'false',
    'returnFaceAttributes': 'age,gender,headPose,smile,facialHair,glasses,emotion,hair,makeup,occlusion,accessories,blur,exposure,noise',
}



@app.route('/')
def upload_f():
   return render_template('upload.html')

@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file():
   if request.method == 'POST':
      f = request.files['file']
      f.save(os.path.join(app.config['UPLOAD_FOLDER'],secure_filename(f.filename)))
      response = requests.post(face_api_url, params=params,
                         headers=headers, json={"url": image_url})
      return json.dumps(response.json())

# if __name__ == '__main__':
app.run(debug = True)
