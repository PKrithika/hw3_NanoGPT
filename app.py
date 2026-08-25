from flask import Flask, jsonify, send_from_directory, request
import subprocess

app = Flask(__name__)


@app.route('/')
def index():
    return send_from_directory('.', 'index.html')


@app.route('/generate', methods=['POST'])
def generate_text():
    data = request.get_json()
    dataset = data.get('dataset', 'twitter')  # 'twitter' or 'shakespeare'

    out_dir = f'out-{dataset}-char'

    result = subprocess.run(
        ["python", "sample.py", f"--out_dir={out_dir}", "--device=cpu"],
        capture_output=True,
        text=True
    )

    output = result.stdout

    # sample.py prints setup logs before the actual generated text,
    # and separates multiple samples with a line of dashes.
    # We only want the first generated sample, cleanly.
    parts = output.split('---------------')
    generated = parts[0] if parts else output

    lines = generated.splitlines()
    clean_lines = [l for l in lines if not l.lower().startswith('overriding')
                   and 'number of parameters' not in l.lower()]
    clean_text = '\n'.join(clean_lines).strip()

    return jsonify({"output": clean_text})


if __name__ == '__main__':
    app.run(debug=True, port=5000)