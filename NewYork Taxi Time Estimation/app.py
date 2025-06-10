from flask import Flask, request, render_template
import pandas as pd

app = Flask(__name__)

# Load your dataset
filtered_data = pd.read_csv("filtered_taxi_data.csv")

@app.route("/", methods=["GET", "POST"])
def index():
    estimated_time = None

    if request.method == "POST":
        pickup_id = request.form.get("pickup")
        dropoff_id = request.form.get("dropoff")

        # Try converting to float
        try:
            pickup_id = float(pickup_id)
            dropoff_id = float(dropoff_id)
        except ValueError:
            estimated_time = None
            with open("results.txt", "a") as f:
                f.write("Invalid input: not a number\n")
            return render_template("index.html", estimated_time=None)

        # Match rows
        mask = (
            (filtered_data["pulocationid"] == pickup_id) &
            (filtered_data["dolocationid"] == dropoff_id)
        )

        matching_data = filtered_data.loc[mask, "trip_duration_minutes"]

        if not matching_data.empty:
            estimated_time = round(matching_data.mean(), 2)
            result = f"Pickup: {pickup_id}, Dropoff: {dropoff_id}, Estimated Time: {estimated_time} minutes\n"
        else:
            result = f"Pickup: {pickup_id}, Dropoff: {dropoff_id}, No match found\n"

        # Write result to file
        with open("results.txt", "a") as f:
            f.write(result)

    return render_template("index.html", estimated_time=estimated_time)

if __name__ == "__main__":
    app.run(debug=True)




