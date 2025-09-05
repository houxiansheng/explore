package com.sleepcompanion.app.data.entity

import androidx.room.Entity
import androidx.room.PrimaryKey

@Entity(tableName = "users")
data class User(
    @PrimaryKey val id: String,
    val username: String,
    val email: String,
    val avatarUrl: String?,
    val isOnline: Boolean = false,
    val lastActiveTime: Long = 0
)