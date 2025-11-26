import io
import os

from flask import (Flask, Response, redirect, render_template, request,
                   send_file)
from PIL import Image

app = Flask(__name__, template_folder='../templates')
app.secret_key = os.environ.get('SECRET_KEY', 'global_ico_guide_rich_v1')
app.url_map.strict_slashes = False
app.config['MAX_CONTENT_LENGTH'] = 4.5 * 1024 * 1024

# ==========================================
# 1. 终极全球语言包 (文案增强版)
# ==========================================
EN_GUIDE = {
    'tab_create': 'Create',
    'tab_guide': 'Guide',
    # 预览区
    'guide_preview_title': 'Visual Preview',
    'guide_preview_desc': 'This is how your icon will appear in browser tabs. It helps users instantly recognize your website.',
    # 步骤 1
    'step1_title': 'Upload to Server',
    'step1_desc': 'Download the .ico file and upload it to the root directory of your website (e.g., public_html).',
    'step1_file_path': '/root/',
    'step1_file_name': 'favicon.ico',
    # 步骤 2
    'step2_title': 'Update HTML Code',
    'step2_desc': 'Copy the following code snippet and paste it inside the <head> section of your webpages.',
    'guide_copy_btn': 'Copy',
    'guide_copied': 'Copied!',
}

TRANSLATIONS = {
    'en': { **EN_GUIDE, 'name': 'English', 'dir': 'ltr', 'recommend': 'Recommended', 'badge': 'HOT', 'seo_title': 'Free Online ICO Converter', 'seo_desc': 'Convert PNG/JPG to ICO. Professional tool.', 'h1': 'ICO Converter', 'subtitle': 'Professional Favicon Generator', 'upload_label': 'Click to upload or Drag image', 'size_label': 'Target Size', 'btn_submit': 'Generate ICO', 'footer': 'Securely processed. Privacy protected.', 'error_large': 'File too large (Max 4MB)' },

    'zh': {
        'name': '简体中文', 'dir': 'ltr', 'recommend': '推荐尺寸', 'badge': '常用',
        'seo_title': '在线 ICO 图标生成器', 'seo_desc': '免费在线图片转 ICO 工具。支持透明背景。',
        'h1': 'ICO 图标生成器', 'subtitle': '一键生成透明背景图标', 'upload_label': '点击选择 或 拖拽图片', 'size_label': '目标尺寸', 'btn_submit': '生成并下载 .ICO', 'footer': '数据安全保护，不保存任何图片。', 'error_large': '文件过大 (最大 4MB)',
        'tab_create': '制作图标',
        'tab_guide': '使用指南',
        'guide_preview_title': '效果预览',
        'guide_preview_desc': '您的图标将显示在浏览器标签页上（如下图所示）。这有助于用户在多个标签中快速识别您的品牌。',
        'step1_title': '上传至服务器',
        'step1_desc': '下载生成的 .ico 文件，并将其上传到您网站服务器的根目录下。',
        'step1_file_path': '/根目录/',
        'step1_file_name': 'favicon.ico',
        'step2_title': '引入 HTML 代码',
        'step2_desc': '复制下方的代码片段，粘贴到您网页源文件 <head> 标签之间。',
        'guide_copy_btn': '复制',
        'guide_copied': '已复制!',
    },

    'tw': {
        'name': '繁體中文', 'dir': 'ltr', 'recommend': '推薦尺寸', 'badge': '常用',
        'seo_title': '線上 ICO 圖示產生器', 'seo_desc': '免費線上圖片轉 ICO 工具。',
        'h1': 'ICO 圖示產生器', 'subtitle': '一鍵生成透明背景圖示', 'upload_label': '點擊選擇 或 拖曳圖片', 'size_label': '目標尺寸', 'btn_submit': '產生並下載 .ICO', 'footer': '資料安全保護，不保存任何圖片。', 'error_large': '檔案過大 (最大 4MB)',
        'tab_create': '製作圖示',
        'tab_guide': '使用指南',
        'guide_preview_title': '效果預覽',
        'guide_preview_desc': '您的圖示將顯示在瀏覽器分頁上。這有助於使用者快速識別您的品牌。',
        'step1_title': '上傳至伺服器',
        'step1_desc': '下載產生的 .ico 檔案，並將其上傳到您網站伺服器的根目錄下。',
        'step1_file_path': '/根目錄/',
        'step1_file_name': 'favicon.ico',
        'step2_title': '引入 HTML 程式碼',
        'step2_desc': '複製下方的程式碼片段，貼上到您網頁原始檔 <head> 標籤之間。',
        'guide_copy_btn': '複製',
        'guide_copied': '已複製!',
    },

    # --- 其他语言 (使用 EN_GUIDE 填充) ---
    'es': { **EN_GUIDE, 'name': 'Español', 'dir': 'ltr', 'recommend': 'Recomendado', 'badge': 'HOT', 'seo_title': 'Convertidor ICO Online', 'seo_desc': 'Convierte imágenes a ICO.', 'h1': 'Convertidor ICO', 'subtitle': 'Generador de Favicon', 'upload_label': 'Clic para subir', 'size_label': 'Tamaño', 'btn_submit': 'Generar .ICO', 'footer': 'Privacidad protegida.', 'error_large': 'Archivo muy grande' },
    'fr': { **EN_GUIDE, 'name': 'Français', 'dir': 'ltr', 'recommend': 'Recommandé', 'badge': 'TOP', 'seo_title': 'Convertisseur ICO', 'seo_desc': 'Convertir en ICO.', 'h1': 'Convertisseur ICO', 'subtitle': 'Générateur de Favicon', 'upload_label': 'Uploader une image', 'size_label': 'Taille', 'btn_submit': 'Générer .ICO', 'footer': 'Confidentialité respectée.', 'error_large': 'Fichier trop volumineux' },
    'de': { **EN_GUIDE, 'name': 'Deutsch', 'dir': 'ltr', 'recommend': 'Empfohlen', 'badge': 'TOP', 'seo_title': 'ICO Konverter', 'seo_desc': 'In ICO umwandeln.', 'h1': 'ICO Konverter', 'subtitle': 'Favicon-Generator', 'upload_label': 'Bild hochladen', 'size_label': 'Größe', 'btn_submit': '.ICO Herunterladen', 'footer': 'Datenschutz.', 'error_large': 'Datei zu groß' },
    'it': { **EN_GUIDE, 'name': 'Italiano', 'dir': 'ltr', 'recommend': 'Consigliato', 'badge': 'TOP', 'seo_title': 'Convertitore ICO', 'seo_desc': 'Converti in ICO.', 'h1': 'Convertitore ICO', 'subtitle': 'Generatore di Favicon', 'upload_label': 'Clicca per caricare', 'size_label': 'Dimensione', 'btn_submit': 'Scarica .ICO', 'footer': 'Privacy protetta.', 'error_large': 'File troppo grande' },
    'pt': { **EN_GUIDE, 'name': 'Português', 'dir': 'ltr', 'recommend': 'Recomendado', 'badge': 'HOT', 'seo_title': 'Conversor ICO', 'seo_desc': 'Converta para ICO.', 'h1': 'Conversor de ICO', 'subtitle': 'Gerador de Favicon', 'upload_label': 'Clique para subir', 'size_label': 'Tamanho', 'btn_submit': 'Baixar .ICO', 'footer': 'Privacidade protegida.', 'error_large': 'Arquivo muito grande' },
    'ru': { **EN_GUIDE, 'name': 'Русский', 'dir': 'ltr', 'recommend': 'Стандарт', 'badge': 'ХИТ', 'seo_title': 'Конвертер ICO', 'seo_desc': 'Конвертировать в ICO.', 'h1': 'Конвертер ICO', 'subtitle': 'Генератор иконок', 'upload_label': 'Загрузить файл', 'size_label': 'Размер', 'btn_submit': 'Скачать .ICO', 'footer': 'Конфиденциальность.', 'error_large': 'Файл слишком большой' },
    'nl': { **EN_GUIDE, 'name': 'Nederlands', 'dir': 'ltr', 'recommend': 'Aanbevolen', 'badge': 'TOP', 'seo_title': 'ICO Converter', 'seo_desc': 'Naar ICO converteren.', 'h1': 'ICO Converter', 'subtitle': 'Favicon Generator', 'upload_label': 'Klik om te uploaden', 'size_label': 'Grootte', 'btn_submit': 'Downloaden', 'footer': 'Privacy beschermd.', 'error_large': 'Bestand te groot' },
    'pl': { **EN_GUIDE, 'name': 'Polski', 'dir': 'ltr', 'recommend': 'Zalecane', 'badge': 'HIT', 'seo_title': 'Konwerter ICO', 'seo_desc': 'Konwertuj na ICO.', 'h1': 'Konwerter ICO', 'subtitle': 'Generator Favicon', 'upload_label': 'Prześlij plik', 'size_label': 'Rozmiar', 'btn_submit': 'Pobierz .ICO', 'footer': 'Ochrona prywatności.', 'error_large': 'Plik zbyt duży' },
    'ja': { **EN_GUIDE, 'name': '日本語', 'dir': 'ltr', 'recommend': '推奨サイズ', 'badge': '人気', 'seo_title': 'ICO変換ツール', 'seo_desc': 'ICO形式に変換。', 'h1': 'ICO 変換ツール', 'subtitle': 'プロフェッショナルなアイコン作成', 'upload_label': 'アップロード', 'size_label': 'サイズ', 'btn_submit': 'ダウンロード', 'footer': 'プライバシー保護。', 'error_large': 'ファイルサイズ過大' },
    'ko': { **EN_GUIDE, 'name': '한국어', 'dir': 'ltr', 'recommend': '추천 크기', 'badge': '인기', 'seo_title': 'ICO 변환기', 'seo_desc': 'ICO 변환 도구.', 'h1': 'ICO 변환기', 'subtitle': '전문 파비콘 생성 도구', 'upload_label': '업로드', 'size_label': '크기', 'btn_submit': '다운로드', 'footer': '개인정보 보호.', 'error_large': '파일이 너무 큽니다' },
    'id': { **EN_GUIDE, 'name': 'Bahasa Indonesia', 'dir': 'ltr', 'recommend': 'Disarankan', 'badge': 'HOT', 'seo_title': 'Konverter ICO', 'seo_desc': 'Ubah ke ICO.', 'h1': 'Konverter ICO', 'subtitle': 'Pembuat Favicon', 'upload_label': 'Unggah gambar', 'size_label': 'Ukuran', 'btn_submit': 'Unduh .ICO', 'footer': 'Privasi dilindungi.', 'error_large': 'File terlalu besar' },
    'tr': { **EN_GUIDE, 'name': 'Türkçe', 'dir': 'ltr', 'recommend': 'Önerilen', 'badge': 'POP', 'seo_title': 'ICO Dönüştürücü', 'seo_desc': 'ICO\'ya çevir.', 'h1': 'ICO Dönüştürücü', 'subtitle': 'Favicon Oluşturucu', 'upload_label': 'Dosya yükle', 'size_label': 'Boyut', 'btn_submit': 'İndir', 'footer': 'Gizlilik korumalı.', 'error_large': 'Dosya çok büyük' },
    'vi': { **EN_GUIDE, 'name': 'Tiếng Việt', 'dir': 'ltr', 'recommend': 'Đề xuất', 'badge': 'HOT', 'seo_title': 'Chuyển đổi ICO', 'seo_desc': 'Sang định dạng ICO.', 'h1': 'Chuyển đổi ICO', 'subtitle': 'Tạo Favicon', 'upload_label': 'Tải lên', 'size_label': 'Kích thước', 'btn_submit': 'Tải xuống', 'footer': 'Bảo mật riêng tư.', 'error_large': 'Tệp quá lớn' },
    'th': { **EN_GUIDE, 'name': 'ไทย', 'dir': 'ltr', 'recommend': 'แนะนำ', 'badge': 'ฮิต', 'seo_title': 'ตัวแปลง ICO', 'seo_desc': 'แปลงเป็น ICO', 'h1': 'ตัวแปลง ICO', 'subtitle': 'สร้าง Favicon', 'upload_label': 'อัปโหลด', 'size_label': 'ขนาด', 'btn_submit': 'ดาวน์โหลด', 'footer': 'ความเป็นส่วนตัว', 'error_large': 'ไฟล์ใหญ่เกินไป' },
    'hi': { **EN_GUIDE, 'name': 'हिन्दी', 'dir': 'ltr', 'recommend': 'अनुशंसित', 'badge': 'आम', 'seo_title': 'ICO कन्वर्टर', 'seo_desc': 'ICO में बदलें', 'h1': 'ICO कन्वर्टर', 'subtitle': 'Favicon जनरेटर', 'upload_label': 'अपलोड करें', 'size_label': 'आकार', 'btn_submit': 'डाउनलोड करें', 'footer': 'गोपनीयता', 'error_large': 'फ़ाइल बहुत बड़ी है' },
    'sv': { **EN_GUIDE, 'name': 'Svenska', 'dir': 'ltr', 'recommend': 'Standard', 'badge': 'TOP', 'seo_title': 'ICO Konverterare', 'seo_desc': 'Till ICO.', 'h1': 'ICO Konverterare', 'subtitle': 'Favicon Generator', 'upload_label': 'Ladda upp', 'size_label': 'Storlek', 'btn_submit': 'Ladda ner', 'footer': 'Integritetsskyddad.', 'error_large': 'Filen är för stor' },
    'uk': { **EN_GUIDE, 'name': 'Українська', 'dir': 'ltr', 'recommend': 'Стандарт', 'badge': 'ХІТ', 'seo_title': 'Конвертер ICO', 'seo_desc': 'В ICO.', 'h1': 'Конвертер ICO', 'subtitle': 'Генератор іконок', 'upload_label': 'Завантажити', 'size_label': 'Розмір', 'btn_submit': 'Завантажити', 'footer': 'Конфіденційність.', 'error_large': 'Файл занадто великий' },
    'ar': { **EN_GUIDE, 'name': 'العربية', 'dir': 'rtl', 'recommend': 'موصى به', 'badge': 'شائع', 'seo_title': 'محول ICO', 'seo_desc': 'تحويل إلى ICO.', 'h1': 'محول ICO', 'subtitle': 'مولد أيقونات', 'upload_label': 'رفع صورة', 'size_label': 'الحجم', 'btn_submit': 'تحميل .ICO', 'footer': 'حماية الخصوصية.', 'error_large': 'الملف كبير جداً' },
    'he': { **EN_GUIDE, 'name': 'עברית', 'dir': 'rtl', 'recommend': 'מומלץ', 'badge': 'נפוץ', 'seo_title': 'ממיר ICO', 'seo_desc': 'להמיר ל-ICO.', 'h1': 'ממיר ICO', 'subtitle': 'יוצר אייקונים', 'upload_label': 'העלאת תמונה', 'size_label': 'גודל', 'btn_submit': 'הורד .ICO', 'footer': 'פרטיות מוגנת.', 'error_large': 'קובץ גדול מדי' }
}

SUPPORTED_LANGS = list(TRANSLATIONS.keys())
DEFAULT_LANG = 'en'

def render_index(lang_code):
    if lang_code not in SUPPORTED_LANGS: return redirect(f"/{DEFAULT_LANG}")
    base_url = request.url_root.rstrip('/')
    alternates = [{'lang': l, 'name': TRANSLATIONS[l]['name'], 'href': f"{base_url}/{l}"} for l in SUPPORTED_LANGS]
    return render_template('index.html', t=TRANSLATIONS[lang_code], current_lang=lang_code, alternates=alternates)

for lang in SUPPORTED_LANGS:
    app.add_url_rule(f'/{lang}', endpoint=f'view_{lang}', view_func=render_index, defaults={'lang_code': lang})

@app.errorhandler(404)
def page_not_found(e): return redirect(f"/{DEFAULT_LANG}")

@app.route('/')
def root():
    accept_lang = request.headers.get('Accept-Language', '')
    target = DEFAULT_LANG
    if 'zh-CN' in accept_lang: target = 'zh'
    elif 'zh-TW' in accept_lang: target = 'tw'
    else:
        for lang in SUPPORTED_LANGS:
            if lang in accept_lang:
                target = lang
                break
    return redirect(f"/{target}")

@app.route('/generate', methods=['POST'])
def generate_ico():
    if 'file' not in request.files: return "Error", 400
    file = request.files['file']
    if file.filename == '': return "Error", 400
    try:
        size = int(request.form.get('size', '32'))
        file_bytes = file.read()
        if len(file_bytes) == 0: return "Error: Empty file", 400
        input_stream = io.BytesIO(file_bytes)
        img = Image.open(input_stream)
        if img.mode != "RGBA": img = img.convert("RGBA")
        img = img.resize((size, size), Image.Resampling.LANCZOS)
        output_stream = io.BytesIO()
        img.save(output_stream, format='ICO', sizes=[(size, size)])
        output_stream.seek(0)
        return send_file(output_stream, mimetype='image/x-icon', as_attachment=True, download_name='favicon.ico')
    except Exception as e:
        print(f"Error: {str(e)}")
        return "Invalid image file", 500

@app.route('/sitemap.xml')
def sitemap():
    base_url = request.url_root.rstrip('/')
    urls = []
    for lang in SUPPORTED_LANGS:
        urls.append(f"<url><loc>{base_url}/{lang}</loc><changefreq>weekly</changefreq></url>")
    xml = f"""<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{''.join(urls)}</urlset>"""
    return Response(xml, mimetype="application/xml")

@app.route('/favicon.ico')
def favicon():
    return send_file('../favicon.ico', mimetype='image/vnd.microsoft.icon')
