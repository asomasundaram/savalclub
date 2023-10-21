from flask import Flask, render_template, request
import pickle 
import requests
import urllib3
import time

app = Flask(__name__)
model = pickle.load(open('expense_model.pkl','rb')) #read mode
@app.route("/")
def home():
    return render_template('index.html')
@app.route("/predict", methods=['GET','POST'])
def predict():
    if request.method == 'POST':
        #access the data from form
        ## Age
        age = int(request.form["age"])
        bmi = int(request.form["bmi"])
        children = int(request.form["children"])
        Sex = int(request.form["Sex"])
        Smoker = int(request.form["Smoker"])
        Region = int(request.form["Region"])
        #get prediction
        input_cols = [[age, bmi, children, Sex, Smoker, Region]]
        prediction = model.predict(input_cols)
        output = round(prediction[0], 2)
        return render_template("index.html", prediction_text='Your predicted annual Healthcare Expense is $ {}'.format(output))

@app.route("/exchange_token", methods=['GET','POST'])
def exchange_token():
    if request.method == 'GET':
        #access the data from form
        ## Age
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

        code = request.args.get('code')
        #return render_template("index.html", prediction_text='Your code is {}'.format(token))
        auth_url = "https://www.strava.com/oauth/token"

        payload = {
        'client_id': "115482",
        'client_secret': 'a8ba6d54854b7f6896290b38aad90032817fbe98',
        'code': code,
        'grant_type': "authorization_code",
        'f': 'json'
        }

        payload_refresh = {
        'client_id': "115482",
        'client_secret': 'a8ba6d54854b7f6896290b38aad90032817fbe98',
        'refresh_token': '719596c8c97b31901fa942e28eee175fb4ba92c3',
        'grant_type': "refresh_token",
        'f': 'json'
    }

        res = requests.post(auth_url, data=payload, verify=False)

        a_token = res.json()['access_token']
        r_token = res.json()['refresh_token']
        name = res.json()['athlete']['username']

        activites_url = "https://www.strava.com/api/v3/athlete/activities"
        ep = round(int(time.time()))
        header = {'Authorization': 'Bearer ' + a_token}
        param = {'before':ep, 'page': 1, 'per_page': 1}
        act_dataset = requests.get(activites_url, headers=header, params=param).json()

        return render_template("index.html", access_token='Your access token is {}'.format(a_token), 
        refresh_token='Your refresh token is {}'.format(r_token),
        username='Your user name is {}'.format(name),
        activity_name='Your recent activitiy is {}'.format(act_dataset[0]['name']+ ' at ' + act_dataset[0]['start_date']))




if __name__ == "__main__":
    app.run(debug=True)