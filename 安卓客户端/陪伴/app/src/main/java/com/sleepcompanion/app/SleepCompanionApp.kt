package com.sleepcompanion.app

import android.app.Application
import androidx.room.Room
import com.sleepcompanion.app.data.AppDatabase

class SleepCompanionApp : Application() {
    
    companion object {
        lateinit var instance: SleepCompanionApp
            private set
        
        lateinit var database: AppDatabase
            private set
    }
    
    override fun onCreate() {
        super.onCreate()
        instance = this
        
        // 初始化数据库
        database = Room.databaseBuilder(
            applicationContext,
            AppDatabase::class.java,
            "sleep-companion-db"
        ).build()
    }
}