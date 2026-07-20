print("Python يعمل بشكل صحيح")
try:
    import flask
    print("✅ Flask مثبت")
except:
    print("❌ Flask غير مثبت")

try:
    import google.generativeai as genai
    print("✅ Google Generative AI مثبت")
except:
    print("❌ Google Generative AI غير مثبت")

print("جميع الاختبارات اكتملت")
