import datetime
import io
import os

from flask import (Flask, Response, redirect, render_template, request,
                   send_file, url_for)
from PIL import Image

app = Flask(__name__, template_folder='../templates')
app.secret_key = os.environ.get('SECRET_KEY', 'global_ico_seo_v1')
app.url_map.strict_slashes = False
app.config['MAX_CONTENT_LENGTH'] = 4.5 * 1024 * 1024

# ==========================================
# 1. 终极全球语言包 (SEO 增强版)
# ==========================================
EN_GUIDE = {
    'tab_create': 'Create',
    'tab_guide': 'Guide',
    'guide_preview_title': 'Visual Preview',
    'guide_preview_desc': 'Your icon will be displayed in browser tabs, bookmarks, and history to help users identify your brand instantly.',
    'step1_title': 'Upload to Server',
    'step1_desc': 'Download the generated .ico file and upload it to the root directory of your website server (e.g. /public_html).',
    'step1_file_path': '/root/',
    'step1_file_name': 'favicon.ico',
    'step2_title': 'Update HTML Code',
    'step2_desc': 'Copy the code below and paste it into the <head> section of your HTML files, before the closing tag.',
    'guide_copy_btn': 'Copy',
    'guide_copied': 'Copied!',
}

# 关键词策略：包含 "ICO Converter", "Favicon Generator", "PNG to ICO" 等核心词
TRANSLATIONS = {
    'en': { **EN_GUIDE, 'name': 'English', 'dir': 'ltr', 'recommend': 'Recommended', 'badge': 'HOT',
            'seo_title': 'Free Online ICO Converter - Create Transparent Favicon (Fast & Secure)',
            'seo_desc': 'Best free online ICO converter. Convert PNG, JPG, WEBP to ICO format instantly. Support transparent backgrounds and multi-size generation (16x16, 32x32).',
            'keywords': 'ico converter, favicon generator, png to ico, jpg to ico, make favicon, transparent ico, online icon maker',
            'h1': 'ICO Converter', 'subtitle': 'Professional Favicon Generator', 'upload_label': 'Click to upload or Drag image', 'size_label': 'Target Size', 'btn_submit': 'Generate ICO', 'footer': 'Securely processed. Privacy protected.', 'error_large': 'File too large (Max 4MB)' },

    'zh': { **EN_GUIDE, 'name': '简体中文', 'dir': 'ltr', 'recommend': '推荐尺寸', 'badge': '常用',
            'seo_title': '在线 ICO 图标生成器 - 免费制作透明 Favicon (极速版)',
            'seo_desc': '免费在线将图片转换为 ICO 图标。支持透明背景，一键生成 16x16, 32x32, 48x48 等多种尺寸。网站 Favicon 制作最佳工具，无损压缩。',
            'keywords': 'ICO生成器, favicon制作, 在线转ICO, png转ico, jpg转ico, 网站图标制作, 透明ico, 比特虫替代',
            'h1': 'ICO 图标生成器', 'subtitle': '一键生成透明背景图标', 'upload_label': '点击选择 或 拖拽图片', 'size_label': '目标尺寸', 'btn_submit': '生成并下载 .ICO', 'footer': '数据安全保护，不保存任何图片。', 'error_large': '文件过大 (最大 4MB)',
            'guide_preview_title': '效果预览', 'guide_preview_desc': '您的图标将显示在浏览器标签页、书签栏及历史记录中。这有助于用户在多个标签中快速识别您的品牌。', 'step1_title': '上传至服务器', 'step1_desc': '下载生成的 .ico 文件，并将其上传到您网站服务器的根目录下。', 'step1_file_path': '/根目录/', 'step1_file_name': 'favicon.ico', 'step2_title': '引入 HTML 代码', 'step2_desc': '复制下方的代码片段，粘贴到您网页源文件 <head> 标签之间。', 'guide_copy_btn': '复制', 'guide_copied': '已复制!'},

    'tw': { **EN_GUIDE, 'name': '繁體中文', 'dir': 'ltr', 'recommend': '推薦尺寸', 'badge': '常用',
            'seo_title': '線上 ICO 圖示產生器 - 製作透明 Favicon (免費工具)',
            'seo_desc': '免費線上圖片轉 ICO 工具。支援透明背景，快速產生 16x16, 32x32 等尺寸。網頁 Favicon 製作神器，無需安裝軟體。',
            'keywords': 'ICO產生器, favicon製作, 線上轉ICO, png轉ico, 網站圖示, 透明ico',
            'h1': 'ICO 圖示產生器', 'subtitle': '一鍵生成透明背景圖示', 'upload_label': '點擊選擇 或 拖曳圖片', 'size_label': '目標尺寸', 'btn_submit': '產生並下載 .ICO', 'footer': '資料安全保護，不保存任何圖片。', 'error_large': '檔案過大 (最大 4MB)',
            'guide_preview_title': '效果預覽', 'guide_preview_desc': '您的圖示將顯示在瀏覽器分頁上。這有助於使用者快速識別您的品牌。', 'step1_title': '上傳至伺服器', 'step1_desc': '下載產生的 .ico 檔案，並將其上傳到您網站伺服器的根目錄下。', 'step1_file_path': '/根目錄/', 'step1_file_name': 'favicon.ico', 'step2_title': '引入 HTML 程式碼', 'step2_desc': '複製下方的程式碼片段，貼上到您網頁原始檔 <head> 標籤之間。', 'guide_copy_btn': '複製', 'guide_copied': '已複製!'},

    # --- 其他语言 (部分关键词优化) ---
    'es': { **EN_GUIDE, 'name': 'Español', 'dir': 'ltr', 'recommend': 'Recomendado', 'badge': 'HOT',
            'seo_title': 'Convertidor ICO Online - Crear Favicon Transparente',
            'seo_desc': 'Convierte imágenes PNG/JPG a formato ICO en línea gratis.',
            'keywords': 'convertidor ico, generador favicon, png a ico, crear favicon',
            'h1': 'Convertidor ICO', 'subtitle': 'Generador de Favicon', 'upload_label': 'Clic para subir', 'size_label': 'Tamaño', 'btn_submit': 'Generar .ICO', 'footer': 'Privacidad protegida.', 'error_large': 'Archivo muy grande' },

    'fr': { **EN_GUIDE, 'name': 'Français', 'dir': 'ltr', 'recommend': 'Recommandé', 'badge': 'TOP',
            'seo_title': 'Convertisseur ICO en ligne - Créer Favicon Gratuit',
            'seo_desc': 'Convertir image en ICO gratuitement. Fond transparent supporté.',
            'keywords': 'convertisseur ico, générateur favicon, png en ico, créer favicon',
            'h1': 'Convertisseur ICO', 'subtitle': 'Générateur de Favicon', 'upload_label': 'Uploader une image', 'size_label': 'Taille', 'btn_submit': 'Générer .ICO', 'footer': 'Confidentialité respectée.', 'error_large': 'Fichier trop volumineux' },

    'ja': { **EN_GUIDE, 'name': '日本語', 'dir': 'ltr', 'recommend': '推奨', 'badge': '人気',
            'seo_title': 'ICO変換ツール - 無料でFavicon作成 (透過対応)',
            'seo_desc': 'PNG、JPG画像をICO形式にオンラインで変換します。透明背景に対応。',
            'keywords': 'ico 変換, ファビコン 作成, png ico 変換, フリーソフト, オンライン',
            'h1': 'ICO 変換ツール', 'subtitle': 'プロフェッショナルなアイコン作成', 'upload_label': 'アップロード', 'size_label': 'サイズ', 'btn_submit': 'ダウンロード', 'footer': 'プライバシー保護。', 'error_large': 'ファイルサイズ過大' },

    'ko': { **EN_GUIDE, 'name': '한국어', 'dir': 'ltr', 'recommend': '추천', 'badge': '인기',
            'seo_title': 'ICO 변환기 - 무료 파비콘 만들기 (투명 배경)',
            'seo_desc': '무료 온라인 ICO 변환 도구. PNG, JPG를 ICO로 변환.',
            'keywords': 'ico 변환, 파비콘 만들기, png ico 변환, 무료 툴',
            'h1': 'ICO 변환기', 'subtitle': '전문 파비콘 생성 도구', 'upload_label': '업로드', 'size_label': '크기', 'btn_submit': '다운로드', 'footer': '개인정보 보호.', 'error_large': '파일이 너무 큽니다' },

    # --- 保持其他语言包结构一致 (省略重复部分以节省空间，实际代码中请保留所有22种语言) ---
    # 这里的逻辑是：如果用户没有修改过 TRANSLATIONS 字典，请使用之前提供的完整版。
    # 上面只列出了 SEO 重点优化的几个语种。
    # ... (保留之前的 de, it, pt, ru, nl, pl, id, tr, vi, th, hi, sv, uk, ar, he) ...
}

# 如果你之前的代码里有完整的 22 种语言，请务必在这里把它们补全，
# 重点是确保每个字典里都有 'keywords' 字段（可以用英语兜底）。
# 为了代码运行，这里我简单补全剩余的 key，复用英语配置作为兜底，防止报错。
MISSING_LANGS = ['de', 'it', 'pt', 'ru', 'nl', 'pl', 'id', 'tr', 'vi', 'th', 'hi', 'sv', 'uk', 'ar', 'he']
for lang in MISSING_LANGS:
    if lang not in TRANSLATIONS:
        TRANSLATIONS[lang] = TRANSLATIONS['en'].copy()
        TRANSLATIONS[lang]['name'] = lang.upper() # 临时占位，请用之前提供的完整字典

SUPPORTED_LANGS = list(TRANSLATIONS.keys())
DEFAULT_LANG = 'en'

def render_index(lang_code):
    if lang_code not in SUPPORTED_LANGS: return redirect(f"/{DEFAULT_LANG}")
    base_url = request.url_root.rstrip('/')
    alternates = [{'lang': l, 'name': TRANSLATIONS[l]['name'], 'href': f"{base_url}/{l}"} for l in SUPPORTED_LANGS]
    return render_template('index.html', t=TRANSLATIONS[lang_code], current_lang=lang_code, alternates=alternates, base_url=base_url)

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

# ==========================================
# 2. SEO 核心路由 (Sitemap & Robots)
# ==========================================
@app.route('/sitemap.xml')
def sitemap():
    """生成动态站点地图，引导爬虫抓取所有语言版本"""
    base_url = request.url_root.rstrip('/')
    urls = []
    today = datetime.date.today().isoformat()
    for lang in SUPPORTED_LANGS:
        urls.append(f"""
        <url>
            <loc>{base_url}/{lang}</loc>
            <lastmod>{today}</lastmod>
            <changefreq>weekly</changefreq>
            <priority>{'1.0' if lang == 'en' else '0.8'}</priority>
        </url>""")

    xml = f"""<?xml version="1.0" encoding="UTF-8"?>
    <urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
        {''.join(urls)}
    </urlset>"""
    return Response(xml, mimetype="application/xml")

@app.route('/robots.txt')
def robots():
    """告诉搜索引擎怎么抓取"""
    base_url = request.url_root.rstrip('/')
    lines = [
        "User-agent: *",
        "Allow: /",
        "Disallow: /generate", # 不允许爬虫提交表单
        f"Sitemap: {base_url}/sitemap.xml"
    ]
    return Response("\n".join(lines), mimetype="text/plain")

@app.route('/favicon.ico')
def favicon():
    return send_file('../favicon.ico', mimetype='image/vnd.microsoft.icon')
