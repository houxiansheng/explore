package com.sleepcompanion.app.data.dao

import androidx.lifecycle.LiveData
import androidx.room.*
import com.sleepcompanion.app.data.entity.ChatMessage

@Dao
interface ChatMessageDao {
    @Query("SELECT * FROM chat_messages WHERE (senderId = :userId AND receiverId = :companionId) OR (senderId = :companionId AND receiverId = :userId) ORDER BY timestamp ASC")
    fun getConversation(userId: String, companionId: String): LiveData<List<ChatMessage>>
    
    @Query("SELECT * FROM chat_messages WHERE id = :messageId")
    fun getMessageById(messageId: String): LiveData<ChatMessage>
    
    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insertMessage(message: ChatMessage)
    
    @Update
    suspend fun updateMessage(message: ChatMessage)
    
    @Delete
    suspend fun deleteMessage(message: ChatMessage)
    
    @Query("UPDATE chat_messages SET isRead = 1 WHERE receiverId = :userId AND isRead = 0")
    suspend fun markAllMessagesAsRead(userId: String)
    
    @Query("SELECT COUNT(*) FROM chat_messages WHERE receiverId = :userId AND isRead = 0")
    fun getUnreadMessageCount(userId: String): LiveData<Int>
}