import os
from flask import Flask, request, jsonify
import google.generativeai as genai
from datetime import datetime

app = Flask(__name__)

# تهيئة إعدادات Gemini API بأمان من متغيرات البيئة
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

model = genai.GenerativeModel('gemini-1.5-flash')

# النظام التوجيهي لـ "ريم" (هوية مؤسسة الذيباني)
SYSTEM_PROMPT = """
أنت "ريم"، مساعدة ذكاء اصطناعي ذكية ومرحبة لمؤسسة الذيباني لخدمات التجزئة والخدمات الرقمية.
مهمتك: الرد على العملاء خارج أوقات العمل، تقديم معلومات وعروض أسعار تقريبية لبضائع المتجر، كروت الإنترنت، شحن الألعاب، والخدمات الرقمية، وجمع بيانات التواصل لخدمتهم لاحقاً.

🎯 أهدافك المحددة:
1. الترحيب بالعميل بأسلوب راقٍ ومحترم وبلهجة عربية مهذبة ومرحبة تعكس هوية المؤسسة.
2. فهم طبيعة طلبه (استفسار عن بضائع، أسعار كروت إنترنت، شحن ألعاب، أو خدمات رقمية).
3. تقديم سعر أو رد تقريبي ومرن مع توضيح أن السعر النهائي يتم اعتماده من الإدارة.
4. طلب اسم العميل ورقم جواله بلطف لتوثيق الطلب في النظام.
5. إبلاغ العميل بأن فريق الدعم الفني البشري سيقوم بالتواصل معه وتأكيد طلبه فور بدء ساعات العمل الرسمية.

📌 القواعد الصارمة:
- تحدث بوضوح وموثوقية عالية.
- لا تعطي وعوداً نهائية أو خصومات كبرى دون مراجعة الإدارة.
- حافظ على سرية البيانات ولا تطلب معلومات حساسة مثل كلمات مرور أو تفاصيل حسابات.
"""

@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        data = request.get_json() or {}
        message = data.get('message')
        sender = data.get('sender', 'عميل')
        
        if not message:
            return jsonify({'status': 'error', 'reply': 'المحتوى فارغ، يرجى كتابة رسالة.'}), 400

        full_prompt = f"{SYSTEM_PROMPT}\n\nالعميل ({sender}): {message}"
        response = model.generate_content(full_prompt)
        reply = response.text
        
        return jsonify({
            'reply': reply,
            'status': 'success',
            'timestamp': datetime.utcnow().isoformat()
        })
    except Exception as e:
        return jsonify({'reply': 'عذراً، واجهت ريم مشكلة تقنية مؤقتة.', 'error': str(e)}), 500

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'healthy', 'service': 'Al-Dhibani Reem Agent (Flask)'})

@app.route('/', methods=['GET'])
def index():
    return "<h1>🤖 وكيل ريم لخدمة العملاء (Flask) يعمل بنجاح!</h1>"

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 3000))
    app.run(host='0.0.0.0', port=port)
