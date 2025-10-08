from flask import Flask, render_template
import pandas as pd

app = Flask(__name__)

def load_pieces():
    df = pd.read_excel("data/bricklink_pieces.xlsx")
    df["Price"] = 0.0  # Placeholder for future price column
    pieces = df.to_dict(orient="records")
    return pieces

@app.route("/")
def index():
    pieces = load_pieces()
    return render_template("index.html", pieces=pieces)

if __name__ == "__main__":
    app.run(debug=True)
