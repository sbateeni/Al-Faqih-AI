from weasyprint import HTML, CSS
from weasyprint.text.fonts import FontConfiguration
import tempfile
import os

class PDFHelper:
    @staticmethod
    def generate_pdf(content, title="نتائج البحث"):
        """توليد ملف PDF من المحتوى"""
        try:
            # تحضير CSS للتصميم
            css = CSS(string='''
                @font-face {
                    font-family: 'Traditional Arabic';
                    src: url('/static/fonts/traditional-arabic.ttf');
                }
                body {
                    font-family: 'Traditional Arabic', Arial, sans-serif;
                    direction: rtl;
                    padding: 2rem;
                }
                h1 {
                    color: #198754;
                    text-align: center;
                    margin-bottom: 2rem;
                }
                .content {
                    line-height: 1.6;
                }
                .references {
                    margin-top: 2rem;
                    padding-top: 1rem;
                    border-top: 1px solid #dee2e6;
                    font-size: 0.9rem;
                    color: #6c757d;
                }
            ''')

            # تحضير HTML
            html_content = f"""
            <html dir="rtl" lang="ar">
            <head>
                <meta charset="UTF-8">
                <title>{title}</title>
            </head>
            <body>
                <h1>{title}</h1>
                <div class="content">
                    {content}
                </div>
            </body>
            </html>
            """

            # إنشاء ملف مؤقت
            with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as tmp:
                # توليد PDF
                font_config = FontConfiguration()
                HTML(string=html_content).write_pdf(
                    tmp.name,
                    stylesheets=[css],
                    font_config=font_config
                )
                return tmp.name

        except Exception as e:
            print(f"خطأ في توليد PDF: {str(e)}")
            return None

    @staticmethod
    def cleanup_temp_file(file_path):
        """حذف الملف المؤقت"""
        try:
            if file_path and os.path.exists(file_path):
                os.unlink(file_path)
        except Exception as e:
            print(f"خطأ في حذف الملف المؤقت: {str(e)}") 