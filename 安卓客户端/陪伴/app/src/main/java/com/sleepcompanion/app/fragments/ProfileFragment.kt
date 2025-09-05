package com.sleepcompanion.app.fragments

import android.content.Intent
import android.os.Bundle
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import androidx.appcompat.app.AppCompatDelegate
import androidx.fragment.app.Fragment
import com.sleepcompanion.app.activities.LoginActivity
import com.sleepcompanion.app.databinding.FragmentProfileBinding
import com.sleepcompanion.app.utils.PreferenceManager

class ProfileFragment : Fragment() {

    private var _binding: FragmentProfileBinding? = null
    private val binding get() = _binding!!
    private lateinit var prefManager: PreferenceManager

    override fun onCreateView(
        inflater: LayoutInflater,
        container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View {
        _binding = FragmentProfileBinding.inflate(inflater, container, false)
        return binding.root
    }

    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)
        
        prefManager = PreferenceManager(requireContext())
        
        // 设置用户信息
        binding.tvUsername.text = prefManager.getUsername()
        
        // 设置夜间模式开关
        binding.switchNightMode.isChecked = prefManager.isNightMode()
        binding.switchNightMode.setOnCheckedChangeListener { _, isChecked ->
            prefManager.saveNightMode(isChecked)
            if (isChecked) {
                AppCompatDelegate.setDefaultNightMode(AppCompatDelegate.MODE_NIGHT_YES)
            } else {
                AppCompatDelegate.setDefaultNightMode(AppCompatDelegate.MODE_NIGHT_NO)
            }
        }
        
        // 设置退出登录按钮
        binding.btnLogout.setOnClickListener {
            // 清除用户数据
            prefManager.clearUserData()
            
            // 跳转到登录页面
            startActivity(Intent(requireContext(), LoginActivity::class.java).apply {
                flags = Intent.FLAG_ACTIVITY_NEW_TASK or Intent.FLAG_ACTIVITY_CLEAR_TASK
            })
        }
    }

    override fun onDestroyView() {
        super.onDestroyView()
        _binding = null
    }
}