package com.sleepcompanion.app.activities

import android.content.Intent
import android.os.Bundle
import android.os.Handler
import android.os.Looper
import androidx.appcompat.app.AppCompatActivity
import com.sleepcompanion.app.R
import com.sleepcompanion.app.utils.PreferenceManager

class SplashActivity : AppCompatActivity() {
    
    private val SPLASH_DELAY = 2000L // 2秒
    
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_splash)
        
        // 延迟后跳转到主页面或登录页面
        Handler(Looper.getMainLooper()).postDelayed({
            val prefManager = PreferenceManager(this)
            val isLoggedIn = prefManager.isLoggedIn()
            
            val intent = if (isLoggedIn) {
                Intent(this, MainActivity::class.java)
            } else {
                Intent(this, LoginActivity::class.java)
            }
            
            startActivity(intent)
            finish()
        }, SPLASH_DELAY)
    }
}