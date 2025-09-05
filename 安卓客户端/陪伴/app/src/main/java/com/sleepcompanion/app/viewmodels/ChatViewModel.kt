package com.sleepcompanion.app.viewmodels

import androidx.lifecycle.LiveData
import androidx.lifecycle.MutableLiveData
import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.sleepcompanion.app.SleepCompanionApp
import com.sleepcompanion.app.data.entity.ChatMessage
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.launch
import java.util.UUID

class ChatViewModel : ViewModel() {
    
    private val chatMessageDao = SleepCompanionApp.database.chatMessageDao()
    
    val messages: LiveData<List<ChatMessage>> = MutableLiveData()
    
    private val _messageSent = MutableLiveData<Boolean>()
    val messageSent: LiveData<Boolean> = _messageSent
    
    fun loadMessages(userId: String, companionId: String) {
        viewModelScope.launch {
            messages = chatMessageDao.getConversation(userId, companionId)
        }
    }
    
    fun sendMessage(senderId: String, receiverId: String, content: String) {
        viewModelScope.launch(Dispatchers.IO) {
            val message = ChatMessage(
                id = UUID.randomUUID().toString(),
                senderId = senderId,
                receiverId = receiverId,
                content = content,
                timestamp = System.currentTimeMillis(),
                isRead = false
            )
            
            chatMessageDao.insertMessage(message)
            _messageSent.postValue(true)
        }
    }
    
    fun receiveMessage(senderId: String, receiverId: String, content: String) {
        viewModelScope.launch(Dispatchers.IO) {
            val message = ChatMessage(
                id = UUID.randomUUID().toString(),
                senderId = senderId,
                receiverId = receiverId,
                content = content,
                timestamp = System.currentTimeMillis(),
                isRead = true
            )
            
            chatMessageDao.insertMessage(message)
        }
    }
    
    fun markMessagesAsRead(userId: String) {
        viewModelScope.launch(Dispatchers.IO) {
            chatMessageDao.markAllMessagesAsRead(userId)
        }
    }
}