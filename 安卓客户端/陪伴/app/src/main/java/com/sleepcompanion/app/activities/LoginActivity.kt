package com.sleepcompanion.app.activities

import android.content.Intent
import android.os.Bundle
import android.widget.Toast
import androidx.appcompat.app.AppCompatActivity
import androidx.lifecycle.ViewModelProvider
import com.sleepcompanion.app.databinding.ActivityLoginBinding
import com.sleepcompanion.app.utils.PreferenceManager
import com.sleepcompanion.app.viewmodels.AuthViewModel

class LoginActivity : AppCompatActivity() {
    
    private lateinit var binding: ActivityLoginBinding
    private lateinit var viewModel: AuthViewModel
    
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        binding = ActivityLoginBinding.inflate(layoutInflater)
        setContentView(binding.root)
        
        viewModel = ViewModelProvider(this).get(AuthViewModel::class.java)
        
        setupListeners()
        observeViewModel()
    }
    
    private fun setupListeners() {
        binding.btnLogin.setOnClickListener {
            val username = binding.etUsername.text.toString().trim()
            val password = binding.etPassword.text.toString().trim()
            
            if (username.isEmpty() || password.isEmpty()) {
                Toast.makeText(this, "请填写用户名和密码", Toast.LENGTH_SHORT).show()
                return@setOnClickListener
            }
            
            viewModel.login(username, password)
        }
        
        binding.tvRegister.setOnClickListener {
            startActivity(Intent(this, RegisterActivity::class.java))
        }
        
        binding.tvForgotPassword.setOnClickListener {
            startActivity(Intent(this, ForgotPasswordActivity::class.java))
        }
    }
    
    private fun observeViewModel() {
        viewModel.loginResult.observe(this) { success ->
            if (success) {
                // 登录成功，保存登录状态并跳转到主页面
                val prefManager = PreferenceManager(this)
                prefManager.setLoggedIn(true)
                
                startActivity(Intent(this, MainActivity::class.java))
                finish()
            } else {
                Toast.makeText(this, "登录失败，请检查用户名和密码", Toast.LENGTH_SHORT).show()
            }
        }
        
        viewModel.isLoading.observe(this) { isLoading ->
            binding.progressBar.visibility = if (isLoading) android.view.View.VISIBLE else android.view.View.GONE
            binding.btnLogin.isEnabled = !isLoading
        }
        
        viewModel.errorMessage.observe(this) { message ->
            if (message.isNotEmpty()) {
                Toast.makeText(this, message, Toast.LENGTH_SHORT).show()
            }
        }
    }
}