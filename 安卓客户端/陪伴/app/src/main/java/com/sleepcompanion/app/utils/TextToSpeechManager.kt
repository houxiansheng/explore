package com.sleepcompanion.app.utils

import android.content.Context
import android.speech.tts.TextToSpeech
import android.util.Log
import java.util.Locale

class TextToSpeechManager(context: Context) {
    
    private var textToSpeech: TextToSpeech? = null
    private var isInitialized = false
    
    init {
        textToSpeech = TextToSpeech(context) { status ->
            if (status == TextToSpeech.SUCCESS) {
                val result = textToSpeech?.setLanguage(Locale.CHINESE)
                if (result == TextToSpeech.LANG_MISSING_DATA || result == TextToSpeech.LANG_NOT_SUPPORTED) {
                    Log.e("TTS", "中文语言不支持")
                } else {
                    isInitialized = true
                }
            } else {
                Log.e("TTS", "初始化失败")
            }
        }
    }
    
    fun speak(text: String) {
        if (isInitialized) {
            textToSpeech?.speak(text, TextToSpeech.QUEUE_FLUSH, null, null)
        }
    }
    
    fun shutdown() {
        textToSpeech?.stop()
        textToSpeech?.shutdown()
    }
}