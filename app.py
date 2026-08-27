import sys
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
        [sys.executable, "sample.py", f"--out_dir={out_dir}", "--device=cpu"],
        capture_output=True,
        text=True
    )

    # If something went wrong, send the actual error back so we can see it
    if result.returncode != 0:
        return jsonify({"output": f"ERROR:\n{result.stderr}"})

    output = result.stdout

    parts = output.split('---------------')
    generated = parts[0] if parts else output

    lines = generated.splitlines()
    clean_lines = [l for l in lines if not l.lower().startswith('overriding')
                   and 'number of parameters' not in l.lower()
                   and not l.lower().startswith('loading meta')]
    clean_text = '\n'.join(clean_lines).strip()

    if not clean_text:
        clean_text = f"(No output generated)\n\nSTDOUT:\n{output}\n\nSTDERR:\n{result.stderr}"

    return jsonify({"output": clean_text})


if __name__ == '__main__':
    app.run(debug=True, port=5000)