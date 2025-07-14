from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import requests
import base64
import os
import tempfile
import zipfile
import io

app = Flask(__name__, static_folder='static')
CORS(app)

DEEPL_API_KEY = "c01a5e0d-9a88-4b92-8bd5-c33c7bf965d1"
DEEPL_API_URL = "https://api.deepl.com/v2/translate"

def translate_text(text, target_lang ):
    """Translate text using DeepL API"""
    if not text or not text.strip():
        return text
    
    headers = {
        'Authorization': f'DeepL-Auth-Key {DEEPL_API_KEY}',
        'Content-Type': 'application/x-www-form-urlencoded',
    }
    
    data = {
        'text': text,
        'target_lang': target_lang,
        'source_lang': 'DE'
    }
    
    try:
        response = requests.post(DEEPL_API_URL, headers=headers, data=data)
        if response.status_code == 200:
            result = response.json()
            return result['translations'][0]['text']
        else:
            print(f"DeepL API Error: {response.status_code} - {response.text}")
            return text
    except Exception as e:
        print(f"Translation error: {e}")
        return text

@app.route('/')
def index():
    return send_from_directory('static', 'index.html')

@app.route('/translate-document-ultimate', methods=['POST'])
def translate_document_ultimate():
    try:
        data = request.get_json()
        
        if not data or 'filename' not in data or 'content' not in data:
            return jsonify({'success': False, 'error': 'Missing filename or content'}), 400
        
        filename = data['filename']
        base64_content = data['content']
        target_lang = data.get('target_lang', 'EN')
        
        # Create response filename
        base_name = os.path.splitext(filename)[0]
        extension = os.path.splitext(filename)[1].lower()
        lang_suffix = target_lang.lower()
        response_filename = f"{base_name}_{lang_suffix}{extension}"
        
        try:
            file_content = base64.b64decode(base64_content)
            
            # For DOCX files - extract and translate text
            if extension == '.docx':
                translated_content = translate_docx_content(file_content, target_lang)
            # For PPTX files - extract and translate text  
            elif extension == '.pptx':
                translated_content = translate_pptx_content(file_content, target_lang)
            else:
                # For other files, return original with translated filename
                translated_content = file_content
            
            # Return translated file
            response_base64 = base64.b64encode(translated_content).decode('utf-8')
            
            return jsonify({
                'success': True,
                'data': {
                    'filename': response_filename,
                    'content': response_base64
                }
            })
            
        except Exception as e:
            return jsonify({'success': False, 'error': f'Processing error: {str(e)}'}), 400
        
    except Exception as e:
        print(f"Translation endpoint error: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

def translate_docx_content(file_content, target_lang):
    """Translate DOCX content using simple text extraction and replacement"""
    try:
        # Create a temporary file
        with tempfile.NamedTemporaryFile(suffix='.docx', delete=False) as temp_file:
            temp_file.write(file_content)
            temp_file_path = temp_file.name
        
        # Read as ZIP and extract text
        with zipfile.ZipFile(temp_file_path, 'r') as zip_ref:
            # Read document.xml which contains the main text
            if 'word/document.xml' in zip_ref.namelist():
                document_xml = zip_ref.read('word/document.xml').decode('utf-8')
                
                # Simple text extraction (basic approach)
                import re
                text_pattern = r'<w:t[^>]*>([^<]+)</w:t>'
                texts = re.findall(text_pattern, document_xml)
                
                # Translate each text segment
                for original_text in texts:
                    if original_text.strip():
                        translated_text = translate_text(original_text, target_lang)
                        document_xml = document_xml.replace(f'>{original_text}<', f'>{translated_text}<')
                
                # Create new ZIP with translated content
                output_buffer = io.BytesIO()
                with zipfile.ZipFile(output_buffer, 'w', zipfile.ZIP_DEFLATED) as new_zip:
                    for item in zip_ref.namelist():
                        if item == 'word/document.xml':
                            new_zip.writestr(item, document_xml.encode('utf-8'))
                        else:
                            new_zip.writestr(item, zip_ref.read(item))
                
                os.unlink(temp_file_path)
                return output_buffer.getvalue()
        
        os.unlink(temp_file_path)
        return file_content
        
    except Exception as e:
        print(f"DOCX translation error: {e}")
        return file_content

def translate_pptx_content(file_content, target_lang):
    """Translate PPTX content using simple text extraction and replacement"""
    try:
        # Create a temporary file
        with tempfile.NamedTemporaryFile(suffix='.pptx', delete=False) as temp_file:
            temp_file.write(file_content)
            temp_file_path = temp_file.name
        
        # Read as ZIP and extract text from slides
        with zipfile.ZipFile(temp_file_path, 'r') as zip_ref:
            output_buffer = io.BytesIO()
            
            with zipfile.ZipFile(output_buffer, 'w', zipfile.ZIP_DEFLATED) as new_zip:
                for item in zip_ref.namelist():
                    if item.startswith('ppt/slides/slide') and item.endswith('.xml'):
                        # Process slide XML
                        slide_xml = zip_ref.read(item).decode('utf-8')
                        
                        # Simple text extraction for slides
                        import re
                        text_pattern = r'<a:t[^>]*>([^<]+)</a:t>'
                        texts = re.findall(text_pattern, slide_xml)
                        
                        # Translate each text segment
                        for original_text in texts:
                            if original_text.strip():
                                translated_text = translate_text(original_text, target_lang)
                                slide_xml = slide_xml.replace(f'>{original_text}<', f'>{translated_text}<')
                        
                        new_zip.writestr(item, slide_xml.encode('utf-8'))
                    else:
                        new_zip.writestr(item, zip_ref.read(item))
            
            os.unlink(temp_file_path)
            return output_buffer.getvalue()
        
    except Exception as e:
        print(f"PPTX translation error: {e}")
        os.unlink(temp_file_path)
        return file_content

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
