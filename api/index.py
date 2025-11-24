import io
import os
from flask import Flask, render_template, request, send_file, Response, url_for
from PIL import Image

# 初始化 Flask，指定模板文件夹位置
app = Flask(__name__, template_folder='../templates')
app.secret_key = os.environ.get('SECRET_KEY', 'fast_ico_maker_secret')
app.config['MAX_CONTENT_LENGTH'] = 4.5 * 1024 * 1024  # 限制 4.5MB

# ===========================
# 核心功能路由
# ===========================

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate_ico():
    if 'file' not in request.files:
        return "未上传文件", 400

    file = request.files['file']

    if file.filename == '':
        return "未选择文件", 400

    try:
        size_str = request.form.get('size', '32')
        size = int(size_str)

        # 图像处理核心逻辑
        img = Image.open(file.stream)
        img = img.convert("RGBA") # 强制转为 RGBA 以保留透明度

        # 使用高质量重采样算法
        img = img.resize((size, size), Image.Resampling.LANCZOS)

        # 写入内存流
        img_io = io.BytesIO()
        img.save(img_io, format='ICO', sizes=[(size, size)])
        img_io.seek(0)

        return send_file(
            img_io,
            mimetype='image/x-icon',
            as_attachment=True,
            download_name='favicon.ico'
        )

    except Exception as e:
        return f"转换失败，请检查图片格式。错误信息: {str(e)}", 500

# ===========================
# SEO 专用路由
# ===========================

@app.route('/robots.txt')
def robots():
    """告诉搜索引擎允许抓取"""
    lines = [
        "User-agent: *",
        "Allow: /",
        f"Sitemap: {request.url_root}sitemap.xml"
    ]
    return Response("\n".join(lines), mimetype="text/plain")

@app.route('/sitemap.xml')
def sitemap():
    """生成站点地图，帮助收录"""
    # 获取当前部署后的域名
    base_url = request.url_root.rstrip('/')
    xml = f"""<?xml version="1.0" encoding="UTF-8"?>
    <urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
        <url>
            <loc>{base_url}/</loc>
            <lastmod>2023-10-01</lastmod>
            <changefreq>monthly</changefreq>
            <priority>1.0</priority>
        </url>
    </urlset>"""
    return Response(xml, mimetype="application/xml")
