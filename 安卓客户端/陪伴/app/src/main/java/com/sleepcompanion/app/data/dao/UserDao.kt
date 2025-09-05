package com.sleepcompanion.app.data.dao

import androidx.lifecycle.LiveData
import androidx.room.*
import com.sleepcompanion.app.data.entity.User

@Dao
interface UserDao {
    @Query("SELECT * FROM users")
    fun getAllUsers(): LiveData<List<User>>
    
    @Query("SELECT * FROM users WHERE id = :userId")
    fun getUserById(userId: String): LiveData<User>
    
    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insertUser(user: User)
    
    @Update
    suspend fun updateUser(user: User)
    
    @Delete
    suspend fun deleteUser(user: User)
    
    @Query("UPDATE users SET isOnline = :isOnline, lastActiveTime = :lastActiveTime WHERE id = :userId")
    suspend fun updateUserStatus(userId: String, isOnline: Boolean, lastActiveTime: Long)
}