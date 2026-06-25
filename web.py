from flask import Flask,render_template,request
from openai import OpenAI
import pypdf
app = Flask(__name__)
client = OpenAI(
    base_url="https://router.huggingface.co/v1",
    api_key="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"
)
@app.route('/',methods=['GET','POST'])
def home():
    output=""
    reply=""
    if request.method=='POST':
        user=request.form['user']
        file = request.files['file']
        pdf_reader = pypdf.PdfReader(file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()
        output=text
        completion = client.chat.completions.create(
          model="deepseek-ai/DeepSeek-R1",
         messages=[
         {
             "role": "user",
             "content":f"document informsation: {output},user query: {user}"
          }
        ],
        )
        reply = completion.choices[0].message
    return render_template('index.html',output=reply)

if __name__=="__main__":
    app.run(host="0.0.0.0")
