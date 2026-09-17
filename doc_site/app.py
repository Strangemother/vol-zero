from flask import Flask, render_template


app = Flask(__name__)


@app.get("/")
def home():
	return render_template("index.html")


def main():
	app.run(debug=True, host="127.0.0.1", port=9050)


if __name__ == "__main__":
	main()
