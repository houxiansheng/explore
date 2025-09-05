package com.sleepcompanion.app.data.entity

import androidx.room.Entity
import androidx.room.PrimaryKey

@Entity(tableName = "chat_messages")
data class ChatMessage(
    @PrimaryKey val id: String,
    val senderId: String,
    val receiverId: String,
    val content: String,
    val timestamp: Long,
    val isRead: Boolean = false,
    val type: Int = TYPE_TEXT
) {
    companion object {
        const val TYPE_TEXT = 0
        const val TYPE_IMAGE = 1
        const val TYPE_VOICE = 2
    }
}