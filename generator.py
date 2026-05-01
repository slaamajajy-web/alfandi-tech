from jinja2 import Template

# القالب الأساسي للهوية البصرية (Dark & Gold Theme)
HTML_TEMPLATE = """
<!DOCTYPE html>
<html dir="rtl" lang="ar">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        body { background-color: #020617; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
        .alfandi-card { border: 1px solid #ca8a04; background: #0f172a; box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.5); }
    </style>
</head>
<body class="text-gray-200 p-6 flex items-center justify-center min-h-screen">
    <div class="alfandi-card rounded-2xl p-8 max-w-lg w-full text-center">
        <h1 class="text-3xl font-extrabold text-yellow-600 mb-4">الفندي TechHunter التقنية</h1>
        <div class="h-1 w-20 bg-yellow-600 mx-auto mb-6"></div>
        <div class="text-right leading-relaxed">
            {{ content }}
        </div>
        <div class="mt-8 pt-6 border-t border-gray-700 text-sm text-gray-500 italic">
            جميع الحقوق محفوظة - إمبراطورية الفندي 2026
        </div>
    </div>
</body>
</html>
"""

def render_html(content_text):
    """دالة تقوم بحقن المحتوى داخل القالب السيادي"""
    return Template(HTML_TEMPLATE).render(content=content_text)
