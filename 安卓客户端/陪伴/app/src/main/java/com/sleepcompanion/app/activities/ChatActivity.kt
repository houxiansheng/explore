package com.sleepcompanion.app.activities

import android.Manifest
import android.content.Intent
import android.content.pm.PackageManager
import android.os.Bundle
import android.speech.RecognitionListener
import android.speech.RecognizerIntent
import android.speech.SpeechRecognizer
import android.view.MenuItem
import android.widget.Toast
import androidx.appcompat.app.AppCompatActivity
import androidx.core.app.ActivityCompat
import androidx.core.content.ContextCompat
import androidx.lifecycle.ViewModelProvider
import androidx.recyclerview.widget.LinearLayoutManager
import com.sleepcompanion.app.adapters.ChatAdapter
import com.sleepcompanion.app.databinding.ActivityChatBinding
import com.sleepcompanion.app.utils.PreferenceManager
import com.sleepcompanion.app.utils.TextToSpeechManager
import com.sleepcompanion.app.viewmodels.ChatViewModel
import java.util.Locale

class ChatActivity : AppCompatActivity() {
    
    private lateinit var binding: ActivityChatBinding
    private lateinit var viewModel: ChatViewModel
    private lateinit var chatAdapter: ChatAdapter
    private lateinit var prefManager: PreferenceManager
    private lateinit var speechRecognizer: SpeechRecognizer
    private lateinit var textToSpeechManager: TextToSpeechManager
    
    // 陪伴机器人ID（在实际应用中，这应该从服务器获取）
    private val companionId = "companion_bot_001"
    
    // 语音识别请求码
    private val RECORD_AUDIO_REQUEST_CODE = 101
    
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        binding = ActivityChatBinding.inflate(layoutInflater)
        setContentView(binding.root)
        
        prefManager = PreferenceManager(this)
        viewModel = ViewModelProvider(this).get(ChatViewModel::class.java)
        textToSpeechManager = TextToSpeechManager(this)
        
        setupActionBar()
        setupRecyclerView()
        setupSpeechRecognizer()
        setupListeners()
        observeViewModel()
        
        // 加载聊天记录
        viewModel.loadMessages(prefManager.getUserId(), companionId)
    }
    
    private fun setupActionBar() {
        setSupportActionBar(binding.toolbar)
        supportActionBar?.apply {
            setDisplayHomeAsUpEnabled(true)
            setDisplayShowHomeEnabled(true)
            title = "夜间陪伴"
            subtitle = "在线"
        }
    }
    
    private fun setupRecyclerView() {
        chatAdapter = ChatAdapter(prefManager.getUserId())
        binding.recyclerView.apply {
            layoutManager = LinearLayoutManager(this@ChatActivity).apply {
                stackFromEnd = true // 从底部开始显示
            }
            adapter = chatAdapter
        }
    }
    
    private fun setupSpeechRecognizer() {
        if (SpeechRecognizer.isRecognitionAvailable(this)) {
            speechRecognizer = SpeechRecognizer.createSpeechRecognizer(this)
            speechRecognizer.setRecognitionListener(object : RecognitionListener {
                override fun onReadyForSpeech(params: Bundle?) {}
                override fun onBeginningOfSpeech() {}
                override fun onRmsChanged(rmsdB: Float) {}
                override fun onBufferReceived(buffer: ByteArray?) {}
                override fun onEndOfSpeech() {}
                override fun onError(error: Int) {
                    val errorMessage = when (error) {
                        SpeechRecognizer.ERROR_AUDIO -> "音频错误"
                        SpeechRecognizer.ERROR_CLIENT -> "客户端错误"
                        SpeechRecognizer.ERROR_INSUFFICIENT_PERMISSIONS -> "权限不足"
                        SpeechRecognizer.ERROR_NETWORK -> "网络错误"
                        SpeechRecognizer.ERROR_NETWORK_TIMEOUT -> "网络超时"
                        SpeechRecognizer.ERROR_NO_MATCH -> "没有匹配的结果"
                        SpeechRecognizer.ERROR_RECOGNIZER_BUSY -> "识别器忙"
                        SpeechRecognizer.ERROR_SERVER -> "服务器错误"
                        SpeechRecognizer.ERROR_SPEECH_TIMEOUT -> "语音超时"
                        else -> "未知错误"
                    }
                    Toast.makeText(this@ChatActivity, "语音识别错误: $errorMessage", Toast.LENGTH_SHORT).show()
                }
                
                override fun onResults(results: Bundle?) {
                    val matches = results?.getStringArrayList(SpeechRecognizer.RESULTS_RECOGNITION)
                    if (!matches.isNullOrEmpty()) {
                        val recognizedText = matches[0]
                        binding.etMessage.setText(recognizedText)
                        // 自动发送识别到的消息
                        sendMessage(recognizedText)
                    }
                }
                
                override fun onPartialResults(partialResults: Bundle?) {}
                override fun onEvent(eventType: Int, params: Bundle?) {}
            })
        } else {
            Toast.makeText(this, "您的设备不支持语音识别", Toast.LENGTH_SHORT).show()
            binding.btnVoice.isEnabled = false
        }
    }
    
    private fun setupListeners() {
        binding.btnSend.setOnClickListener {
            val message = binding.etMessage.text.toString().trim()
            if (message.isNotEmpty()) {
                // 发送消息
                sendMessage(message)
            }
        }
        
        binding.btnVoice.setOnClickListener {
            if (ContextCompat.checkSelfPermission(this, Manifest.permission.RECORD_AUDIO) != PackageManager.PERMISSION_GRANTED) {
                ActivityCompat.requestPermissions(this, arrayOf(Manifest.permission.RECORD_AUDIO), RECORD_AUDIO_REQUEST_CODE)
            } else {
                startSpeechRecognition()
            }
        }
    }
    
    private fun sendMessage(message: String) {
        val userId = prefManager.getUserId()
        viewModel.sendMessage(userId, companionId, message)
        
        // 清空输入框
        binding.etMessage.text.clear()
    }
    
    private fun startSpeechRecognition() {
        val intent = Intent(RecognizerIntent.ACTION_RECOGNIZE_SPEECH).apply {
            putExtra(RecognizerIntent.EXTRA_LANGUAGE_MODEL, RecognizerIntent.LANGUAGE_MODEL_FREE_FORM)
            putExtra(RecognizerIntent.EXTRA_LANGUAGE, Locale.CHINESE.toString())
            putExtra(RecognizerIntent.EXTRA_MAX_RESULTS, 1)
            putExtra(RecognizerIntent.EXTRA_PROMPT, "请说话...")
        }
        
        try {
            speechRecognizer.startListening(intent)
            Toast.makeText(this, "正在聆听...", Toast.LENGTH_SHORT).show()
        } catch (e: Exception) {
            Toast.makeText(this, "语音识别启动失败: ${e.message}", Toast.LENGTH_SHORT).show()
        }
    }
    
    private fun observeViewModel() {
        viewModel.messages.observe(this) { messages ->
            chatAdapter.submitList(messages)
            if (messages.isNotEmpty()) {
                binding.recyclerView.smoothScrollToPosition(messages.size - 1)
            }
        }
        
        viewModel.messageSent.observe(this) { sent ->
            if (sent) {
                // 模拟机器人回复
                simulateCompanionReply()
            }
        }
    }
    
    private fun simulateCompanionReply() {
        // 在实际应用中，这里应该调用API获取回复
        // 这里为了演示，我们模拟一个简单的回复
        val replies = listOf(
            "你好呀，睡不着吗？",
            "我一直都在这里陪着你。",
            "要不要听一个睡前故事？",
            "深呼吸，放松一下，慢慢地会睡着的。",
            "今天过得怎么样？想聊聊吗？",
            "你知道吗？保持规律的作息时间对睡眠很有帮助。",
            "试着闭上眼睛，想象一个平静的地方。",
            "有什么心事想分享吗？",
            "我可以为你播放一些轻柔的音乐帮助你入睡。",
            "记得睡前不要看手机哦，蓝光会影响睡眠质量。"
        )
        
        val randomReply = replies.random()
        
        // 延迟一下，模拟打字时间
        binding.root.postDelayed({
            viewModel.receiveMessage(companionId, prefManager.getUserId(), randomReply)
            
            // 使用文字转语音朗读回复
            textToSpeechManager.speak(randomReply)
        }, 1000)
    }
    
    override fun onRequestPermissionsResult(requestCode: Int, permissions: Array<out String>, grantResults: IntArray) {
        super.onRequestPermissionsResult(requestCode, permissions, grantResults)
        if (requestCode == RECORD_AUDIO_REQUEST_CODE && grantResults.isNotEmpty()) {
            if (grantResults[0] == PackageManager.PERMISSION_GRANTED) {
                startSpeechRecognition()
            } else {
                Toast.makeText(this, "需要麦克风权限才能使用语音功能", Toast.LENGTH_SHORT).show()
            }
        }
    }
    
    override fun onOptionsItemSelected(item: MenuItem): Boolean {
        if (item.itemId == android.R.id.home) {
            finish()
            return true
        }
        return super.onOptionsItemSelected(item)
    }
    
    override fun onDestroy() {
        super.onDestroy()
        if (::speechRecognizer.isInitialized) {
            speechRecognizer.destroy()
        }
        if (::textToSpeechManager.isInitialized) {
            textToSpeechManager.shutdown()
        }
    }
}