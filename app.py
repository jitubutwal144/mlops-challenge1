from flask import Flask
from flask import render_template
from flask import request

from src.pipelines.predict_pipeline import InferenceData
from src.pipelines.predict_pipeline import PredictPipeline

application = Flask(__name__)

app = application

## Route for a home page


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/predict", methods=["GET", "POST"])
def predict_datapoint():
    if request.method == "GET":
        return render_template("home.html")
    else:
        latest_sensor_data = InferenceData()
        inference_df = latest_sensor_data.get_data_as_data_frame()

        predict_pipeline = PredictPipeline()
        results = predict_pipeline.predict(inference_df)
        print(f"predictions: {results}")
        return render_template("home.html", results=results[0])


if __name__ == "__main__":
    app.run(host="0.0.0.0")
