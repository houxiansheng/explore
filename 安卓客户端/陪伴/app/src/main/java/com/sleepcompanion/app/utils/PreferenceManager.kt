package com.sleepcompanion.app.utils

import android.content.Context
import android.content.SharedPreferences

class PreferenceManager(context: Context) {
    
    private val sharedPreferences: SharedPreferences = context.getSharedPreferences(
        PREF_NAME, Context.MODE_PRIVATE
    )
    
    fun setLoggedIn(isLoggedIn: Boolean) {
        sharedPreferences.edit().putBoolean(KEY_IS_LOGGED_IN, isLoggedIn).apply()
    }
    
    fun isLoggedIn(): Boolean {
        return sharedPreferences.getBoolean(KEY_IS_LOGGED_IN, false)
    }
    
    fun saveUserId(userId: String) {
        sharedPreferences.edit().putString(KEY_USER_ID, userId).apply()
    }
    
    fun getUserId(): String {
        return sharedPreferences.getString(KEY_USER_ID, "") ?: ""
    }
    
    fun saveUsername(username: String) {
        sharedPreferences.edit().putString(KEY_USERNAME, username).apply()
    }
    
    fun getUsername(): String {
        return sharedPreferences.getString(KEY_USERNAME, "") ?: ""
    }
    
    fun saveNightMode(isNightMode: Boolean) {
        sharedPreferences.edit().putBoolean(KEY_NIGHT_MODE, isNightMode).apply()
    }
    
    fun isNightMode(): Boolean {
        return sharedPreferences.getBoolean(KEY_NIGHT_MODE, false)
    }
    
    fun clearUserData() {
        sharedPreferences.edit()
            .remove(KEY_IS_LOGGED_IN)
            .remove(KEY_USER_ID)
            .remove(KEY_USERNAME)
            .apply()
    }
    
    companion object {
        private const val PREF_NAME = "sleep_companion_prefs"
        private const val KEY_IS_LOGGED_IN = "is_logged_in"
        private const val KEY_USER_ID = "user_id"
        private const val KEY_USERNAME = "username"
        private const val KEY_NIGHT_MODE = "night_mode"
    }
}