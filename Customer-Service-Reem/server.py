import os
from flask import Flask, request
import google.generativeai as genai
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)

# إعداد مفتاح API
GEMINI_KEY = os.environ.get("GEMINI_API_KEY")
if GEMINI_KEY:
    genai.configure(api_key=GEMINI_KEY)

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
        # قراءة النص القادم من الواتساب
        incoming_msg = request.values.get('Body', '').strip()
        print(f"Message received: {incoming_msg}")

        if not incoming_msg:
            resp = MessagingResponse()
            resp.message("أهلاً بك! كيف يمكنني مساعدتك اليوم؟")
            return str(resp)

        # استدعاء موديل gemini-1.5-flash-latest مع التعليمات النظامية للحفاظ على هوية ريم
        model = genai.GenerativeModel('gemini-1.5-flash-latest', system_instruction=SYSTEM_PROMPT)
        response = model.generate_content(incoming_msg)
        
        reply_text = response.text if response and hasattr(response, 'text') else "تم استلام رسالتك بنجاح."

        # تجهيز رد Twilio
        resp = MessagingResponse()
        resp.message(reply_text)
        return str(resp)

    except Exception as e:
        print(f"Error in webhook execution: {str(e)}")
        resp = MessagingResponse()
        resp.message("مرحباً بك! استلمت رسالتك وجاري معالجتها.")
        return str(resp)

@app.route('/', methods=['GET'])
def index():
    return "Reem Customer Service Bot is Running!", 200

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)

