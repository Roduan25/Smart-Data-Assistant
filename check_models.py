import google.generativeai as genai
import sys
import io

# لدعم اللغة العربية في التيرمينال
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# ضع مفتاحك الجديد هنا (ولا تشاركه هنا في المحادثة!)
API_KEY = "AIzaSyDVb2C-iPwWq2m3dYe5y1taK_sj1KFSVVk"
genai.configure(api_key=API_KEY)

print("جاري الاتصال بجوجل لمعرفة النماذج المتاحة لك...\n")

try:
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            print(f"✅ متاح: {m.name}")
except Exception as e:
    print(f"❌ حدث خطأ أثناء الاتصال: {e}")