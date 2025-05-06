import datetime
from flask import Flask, render_template, request, session

app = Flask(__name__)
app.secret_key = "your-secret-key"  # Replace with a secure, random key

def tier1(input_text):
    # Example processing logic — replace with your actual logic
    return f"Processed: {input_text.upper()} ahmed.hossam1"

def get_client_ip():
    if request.headers.getlist("X-Forwarded-For"):
        return request.headers.getlist("X-Forwarded-For")[0].split(',')[0].strip()
    return request.remote_addr

# @app.route("/", methods=["GET", "POST"])
# def home():
#     result = ""
#     name = session.get("username")
#
#     if request.method == "POST":
#         # Save username if not already in session
#         if not name:
#             name = request.form.get("username")
#             if name:
#                 session["username"] = name
#
#         user_input = request.form["user_input"]
#         ip = get_client_ip()
#         user_agent = request.headers.get('User-Agent')
#         timestamp = datetime.datetime.now().isoformat()
#
#         # Save all data to a file
#         with open("user_inputs.txt", "a", encoding="utf-8") as f:
#             f.write(f"{timestamp}\t{name}\t{ip}\t{user_agent}\t{user_input}\n")
#
#         result = tier1(user_input)
#
#     return render_template("index.html", result=result, name=name)

@app.route("/", methods=["GET", "POST"])
def home():
    result = ""
    name = session.get("username")

    if request.method == "POST":
        if not name:
            name = request.form.get("username")
            if name:
                session["username"] = name

        user_input = request.form["user_input"]
        ip = get_client_ip()
        user_agent = request.headers.get('User-Agent')
        timestamp = datetime.datetime.now().isoformat()

        # Save input
        with open("user_inputs.txt", "a", encoding="utf-8") as f:
            f.write(f"{timestamp}\t{name}\t{ip}\t{user_agent}\t{user_input}\n")

        result = tier1(user_input)

    # Read all previous messages
    messages = []
    try:
        with open("user_inputs.txt", "r", encoding="utf-8") as f:
            for line in f:
                parts = line.rstrip('\n').split('\t', 4)
                if len(parts) == 5:
                    _, _, _, _, message = parts
                    # Replace literal \n with actual newline + indent
                    indent = "\n" + " " * 11
                    unescaped_msg = message.replace("\\n", indent)

                    # Ignore if message is only newlines or whitespace
                    if unescaped_msg.strip():
                        formatted_msg = (
                            "<div style='white-space: pre-wrap;'>"
                            "<span style='color:blue;'>Anonymous:</span> "
                            f"{unescaped_msg}</div>"
                        )
                        messages.append(formatted_msg)
        messages.reverse()
    except FileNotFoundError:
        messages = []

    return render_template("index.html", result=result, name=name, all_messages="<br>".join(messages))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
