from flask import Flask, render_template, request, redirect
from dotenv import load_dotenv
import requests
import os

load_dotenv()

app = Flask(__name__)

username=os.getenv("HUE_USERNAME")
bridge_ip=os.getenv("HUE_BRIDGE_IP")

#use to get new username, have to press button on bridge
#payload = {"devicetype": "hue-dashboard"}
#response = requests.post(f"http://{bridge_ip}/api", json=payload)
#print(response.json())

def get_lights():
  url = f"http://{bridge_ip}/api/{username}/lights"
  response = requests.get(url)
  return response.json()

def update_light(light_id, data):
  url = f"http://{bridge_ip}/api/{username}/lights/{light_id}/state"
  requests.put(url, json=data)
  print(f"Light {light_id} updated with {data}")

def flip_light(light_id):
  url = f"http://{bridge_ip}/api/{username}/lights/{light_id}"
  response = requests.get(url)
  light_data = response.json()
  current_state = light_data["state"]["on"]
  new_state = not current_state
  toggle_url = f"http://{bridge_ip}/api/{username}/lights/{light_id}/state"
  requests.put(toggle_url, json={"on": new_state})

  print(f"Light {light_id} toggled to {'on' if new_state else 'off'}.")

@app.route("/")
def index():
  lights = get_lights()
  return render_template("index.html", lights=lights)

@app.route("/toggle/<light_id>")
def toggle_light(light_id):
  flip_light(light_id)
  return redirect("/")

@app.route("/brightness/<light_id>", methods=["POST"])
def set_brightness(light_id):
  brightness = int(request.form["brightness"])
  update_light(light_id, {"bri": brightness})
  return redirect("/")

if __name__ == "__main__":
  app.run(debug=True)