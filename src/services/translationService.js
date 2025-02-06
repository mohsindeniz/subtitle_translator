import translate from 'translate-google';

export async function translateText(text, targetLanguage = 'tr') {
  try {
    const translatedText = await translate(text, { to: targetLanguage });
    return translatedText;
  } catch (error) {
    throw new Error('Çeviri sırasında bir hata oluştu');
  }
} 