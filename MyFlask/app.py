import pickle
mdl_gender = pickle.load(open("final_model_gender.pkl","rb"))
mdl_age_group = pickle.load(open("final_model_age_group.pkl","rb"))
test_data_gender = pickle.load(open("test_data_gender.pkl","rb"))
test_data_age_group = pickle.load(open("test_data_age_group.pkl","rb"))

test_data_gender.columns = ["DeviceID", "Gender", "AgeGroup", "TravellerType", "HighLevelCategory", "Cluster", "EventCount", "MobilePhoneBrand", "DeviceModel", "TrainTestFlag"]

test_data_age_group.columns = ['DeviceID', 'Gender', 'AgeGroup', 'TravellerType', 'HighLevelCategory',
    'Cluster', 'EventCount', 'MobilePhoneBrand', 'DeviceModel',
    'TrainTestFlag']

import numpy as np
from flask import Flask,request,render_template


app =Flask(__name__)


@app.route("/")
def homepage():
    device_ids = test_data_gender["DeviceID"].values
    return render_template('index.html', device_ids=device_ids)
	
	####################################################################

@app.route("/recommend_campaign",methods=['POST'])
def predict():
    def select_campaign(gender,age_group):
        campaign={
            "Female":[("Campaign 1","Specific personalized fashion-related campaigns targeting female customers."),
                      ("Campaign 2","Specific cashback offers on special days [for example, International Women’s Day] targeting female customers.")],
            "Male":[
                      ("Campaign 3","Personalized call and data packs targeting male customers.")],
            
            "0-24":
                      [("Campaign 4","Bundled smartphone offers for the age group 0–24 years.")],
                     "25-32" : [("Campaign 5","Special offers for payment wallet offers - those in the age group of 25–32 years.")],
                     "33-45":[ ("Campaign 6","Special cashback offers for Privilege Membership 33-45 years.")],
                     "46+":[ ("Campaign 6","Special cashback offers for Older Customers [46+] years.")]
                      
                     
                 }
        final=""
        for cmp in campaign[gender]:
            final = final + cmp[0] + " - " + cmp[1] + "\n"
        for cmp in campaign[age_group]:
            final = final + cmp[0] + " - " + cmp[1] + "\n"
        return final
        

    device_id=[int(x) for x in request.form.values()][0]
    
    
    X_gender=test_data_gender[test_data_gender["DeviceID"]==device_id].drop(["DeviceID","Gender","AgeGroup","TrainTestFlag"],axis=1).iloc[0,:]
    X_age_group=test_data_age_group[test_data_age_group["DeviceID"]==device_id].drop(["DeviceID","Gender","AgeGroup","TrainTestFlag"],axis=1).iloc[0,:]
    gender="Female" if mdl_gender.predict(X_gender.values.reshape(1, -1))[0] == 0 else "Male"

    age_group_predicted=mdl_age_group.predict(X_age_group.values.reshape(1, -1))[0]
    age_group = "0-24" if age_group_predicted == 0 else "25-32" if age_group_predicted == 1 else "33-45" if age_group_predicted == 2 else "46+"

    campaign=select_campaign(gender,age_group)
    result_var = [device_id, gender, age_group, campaign]
    
    return render_template("index.html", prediction_text = result_var)
#    return render_template("index.html",prediction_text = "Prediction for Device: " + str(device_id) + " -> " + "\n Gender is "+ gender + ",\n" + "\nAge Group is " + str(age_group) + ",\n" + "\nCampaigns are - \n" + campaign)

    
    
    
    
if __name__=="__main__":
    app.run(host="0.0.0.0",port=5000,debug=True)