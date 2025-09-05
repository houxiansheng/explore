package com.sleepcompanion.app.viewmodels

import androidx.lifecycle.LiveData
import androidx.lifecycle.MutableLiveData
import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.sleepcompanion.app.SleepCompanionApp
import com.sleepcompanion.app.data.entity.User
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.launch
import java.util.UUID

class AuthViewModel : ViewModel() {
    
    private val _loginResult = MutableLiveData<Boolean>()
    val loginResult: LiveData<Boolean> = _loginResult
    
    private val _registerResult = MutableLiveData<Boolean>()
    val registerResult: LiveData<Boolean> = _registerResult
    
    private val _isLoading = MutableLiveData<Boolean>()
    val isLoading: LiveData<Boolean> = _isLoading
    
    private val _errorMessage = MutableLiveData<String>()
    val errorMessage: LiveData<String> = _errorMessage
    
    // 模拟登录过程
    fun login(username: String, password: String) {
        _isLoading.value = true
        
        // 在实际应用中，这里应该调用API进行身份验证
        // 这里为了演示，我们模拟一个成功的登录
        viewModelScope.launch(Dispatchers.IO) {
            try {
                // 模拟网络延迟
                Thread.sleep(1000)
                
                // 假设登录成功，创建一个用户
                val userId = UUID.randomUUID().toString()
                val user = User(
                    id = userId,
                    username = username,
                    email = "$username@example.com",
                    avatarUrl = null,
                    isOnline = true,
                    lastActiveTime = System.currentTimeMillis()
                )
                
                // 保存用户到数据库
                SleepCompanionApp.database.userDao().insertUser(user)
                
                _loginResult.postValue(true)
            } catch (e: Exception) {
                _errorMessage.postValue("登录失败: ${e.message}")
                _loginResult.postValue(false)
            } finally {
                _isLoading.postValue(false)
            }
        }
    }
    
    // 模拟注册过程
    fun register(username: String, email: String, password: String) {
        _isLoading.value = true
        
        // 在实际应用中，这里应该调用API进行注册
        viewModelScope.launch(Dispatchers.IO) {
            try {
                // 模拟网络延迟
                Thread.sleep(1000)
                
                // 假设注册成功，创建一个用户
                val userId = UUID.randomUUID().toString()
                val user = User(
                    id = userId,
                    username = username,
                    email = email,
                    avatarUrl = null,
                    isOnline = true,
                    lastActiveTime = System.currentTimeMillis()
                )
                
                // 保存用户到数据库
                SleepCompanionApp.database.userDao().insertUser(user)
                
                _registerResult.postValue(true)
            } catch (e: Exception) {
                _errorMessage.postValue("注册失败: ${e.message}")
                _registerResult.postValue(false)
            } finally {
                _isLoading.postValue(false)
            }
        }
    }
    
    fun resetPassword(email: String) {
        _isLoading.value = true
        
        // 在实际应用中，这里应该调用API发送重置密码邮件
        viewModelScope.launch {
            try {
                // 模拟网络延迟
                Thread.sleep(1000)
                
                // 假设发送成功
                _errorMessage.postValue("重置密码链接已发送到您的邮箱")
            } catch (e: Exception) {
                _errorMessage.postValue("发送重置密码邮件失败: ${e.message}")
            } finally {
                _isLoading.postValue(false)
            }
        }
    }
}