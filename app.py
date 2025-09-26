from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from flask import Flask, render_template, request, send_file
from bs4 import BeautifulSoup
import requests
import io
import time

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    urls = request.form.get('urls', '').splitlines()
    urls = [url.strip() for url in urls if url]
    
    if not urls:
        return "Please enter at least one URL", 400
    
    session = requests.Session()
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Connection": "keep-alive"
    }
    session.headers.update(headers)
    
    # A4 page setup
    A4 = (210, 297)  # Standard A4 size (mm)
    pdf_buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        pdf_buffer,
        pagesize=A4,
        rightMargin=18,
        leftMargin=18,
        topMargin=18,
        bottomMargin=18
    )

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        name='Title',
        fontSize=11,
        leading=18,
        alignment=1,
        textColor=(0, 0, 0),
        fontName='Helvetica-Bold'
    )

    body_style = ParagraphStyle(
        name='Body',
        fontSize=4,
        leading=5,
        alignment=0,
        textColor=(0, 0, 0)
    )

    bullet_style = ParagraphStyle(
        name='BulletIndented',
        leftIndent=10,
        fontSize=4,
        leading=5,
        alignment=0,
        textColor=(0, 0, 0)
    )

    bold_style = ParagraphStyle(
        name='Bold',
        fontSize=4,
        leading=5,
        alignment=0,
        textColor=(0, 0, 0),
        fontName='Helvetica-Bold'
    )

    link_style = ParagraphStyle(
        name='Link',
        fontSize=4,
        leading=5,
        alignment=0,
        textColor=(0, 0, 0),
        linkUnderline=0,
        fontName='Helvetica-Bold'
    )

    header2_style = ParagraphStyle(
        name='Header2',
        fontSize=7,
        leading=10,
        alignment=0,
        textColor=(0, 0, 0),
        fontName='Helvetica-Bold'
    )

    header3_style = ParagraphStyle(
        name='Header3',
        fontSize=6,
        leading=8,
        alignment=0,
        textColor=(0, 0, 0),
        fontName='Helvetica-Bold'
    )

    header4_style = ParagraphStyle(
        name='Header4',
        fontSize=5,
        leading=7,
        alignment=0,
        textColor=(0, 0, 0),
        fontName='Helvetica-Bold'
    )
    
    # Build PDF content
    story = []
    for url in urls:
        try:
            response = session.get(url, timeout=10)
            response.raise_for_status()
            time.sleep(1)  # Critical for avoiding rate limits
            
            soup = BeautifulSoup(response.text, 'html.parser')
            main = soup.find('main')

            target_div = main.find('div', {'id': 'import_and_publish_news_modal'})
            if target_div:
                target_div.decompose()
            
            if not main:
                continue
                
            for btn in main.find_all('button', {'data-toggle': 'collapse'}):
                h3 = soup.new_tag('h3')
                h3.string = btn.string
                btn.replace_with(h3)

            for br in main.find_all("br"):
                br.replace_with("<br/>")
            
            title = main.find('h1')
            if title:
                story.append(Paragraph(title.text, title_style))
                story.append(Spacer(0, 10))
            
            elements = main.find_all(['h2', 'h3', 'h4', 'p', 'li', 'br','strong'])
            for i, elem in enumerate(elements):
                text = elem.get_text(strip=True)
                if text.strip():
                    if elem.name == 'h2':
                        story.append(Paragraph(text, header2_style))
                    elif elem.name == 'h3':
                        story.append(Paragraph(text, header3_style))
                    elif elem.name == 'h4':
                        story.append(Paragraph(text, header4_style))
                    elif elem.name in ['strong', 'b']:
                        story.append(Paragraph(text, bold_style))
                    # to be improved
                    # elif elem.name == 'a':
                    #     story.append(Paragraph(text, link_style))
                    elif elem.name == 'li':
                        text = "• " + text  # Add bullet
                        story.append(Paragraph(text, bullet_style))
                    else:
                        story.append(Paragraph(text, body_style))
                    # Add spacer after each non-empty item (except last)
                    if i < len(elements) - 1:
                        story.append(Spacer(0, 8)) 
            story.append(PageBreak())

            
        except Exception as e:
            print(f"Error processing {url}: {str(e)}")
    
    doc.build(story)
    pdf_buffer.seek(0)
    
    return send_file(
        pdf_buffer,
        mimetype='application/pdf',
        download_name='output.pdf',
        as_attachment=True
    )

if __name__ == '__main__':
    app.run(debug=True)
