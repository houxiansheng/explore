package com.sleepcompanion.app.data

import androidx.room.Database
import androidx.room.RoomDatabase
import com.sleepcompanion.app.data.dao.ChatMessageDao
import com.sleepcompanion.app.data.dao.UserDao
import com.sleepcompanion.app.data.entity.ChatMessage
import com.sleepcompanion.app.data.entity.User

@Database(entities = [User::class, ChatMessage::class], version = 1)
abstract class AppDatabase : RoomDatabase() {
    abstract fun userDao(): UserDao
    abstract fun chatMessageDao(): ChatMessageDao
}