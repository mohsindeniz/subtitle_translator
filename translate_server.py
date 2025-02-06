from flask import Flask, request, jsonify
from flask_cors import CORS
from deep_translator import GoogleTranslator
from concurrent.futures import ThreadPoolExecutor, as_completed
import asyncio
import aiohttp

app = Flask(__name__)
CORS(app)

# Thread havuzunu daha fazla worker ile oluştur
executor = ThreadPoolExecutor(max_workers=10)

# Asenkron çeviri için session havuzu
session = None

def fix_translation_format(text):
    # Gereksiz satır sonlarını kaldır
    text = ' '.join(text.split())
    # Noktalama işaretlerinden sonra boşluk ekle
    text = text.replace('.','. ').replace('!','! ').replace('?','? ')
    # Fazla boşlukları temizle
    text = ' '.join(text.split())
    return text

async def init_session():
    global session
    if session is None:
        session = aiohttp.ClientSession()

async def translate_chunk_async(text, from_lang='en', to_lang='tr'):
    translator = GoogleTranslator(source=from_lang, target=to_lang)
    return translator.translate(text)

async def translate_chunks_parallel(chunks, from_lang, to_lang):
    tasks = []
    for chunk in chunks:
        if chunk.strip():  # Boş chunk'ları atla
            task = asyncio.create_task(translate_chunk_async(chunk, from_lang, to_lang))
            tasks.append(task)
    return await asyncio.gather(*tasks)

@app.route('/translate', methods=['POST'])
async def translate_text():
    try:
        await init_session()
        data = request.json
        text = data.get('text', '')
        from_lang = data.get('source', 'en')
        to_lang = data.get('target', 'tr')

        # Daha küçük parçalara böl
        MAX_LENGTH = 500  # Daha küçük chunk'lar
        chunks = [text[i:i+MAX_LENGTH] for i in range(0, len(text), MAX_LENGTH)]
        
        # Chunk'ları gruplara ayır (daha fazla paralel işlem)
        BATCH_SIZE = 10
        translated_text = []
        
        for i in range(0, len(chunks), BATCH_SIZE):
            batch = chunks[i:i+BATCH_SIZE]
            # Her batch'i paralel çevir
            batch_results = await translate_chunks_parallel(batch, from_lang, to_lang)
            translated_text.extend(batch_results)

        # Sonuçları birleştir ve temizle
        final_text = ' '.join(filter(None, translated_text))
        
        # Çeviri formatını düzelt
        final_text = fix_translation_format(final_text)
        
        return jsonify({
            'translatedText': final_text
        })
    except Exception as e:
        return jsonify({
            'error': str(e)
        }), 500

if __name__ == '__main__':
    # Asenkron sunucu başlat
    app.run(port=5000, threaded=True, debug=False) 