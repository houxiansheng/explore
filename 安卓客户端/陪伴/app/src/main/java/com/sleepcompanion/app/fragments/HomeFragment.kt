package com.sleepcompanion.app.fragments

import android.content.Intent
import android.os.Bundle
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import androidx.fragment.app.Fragment
import com.sleepcompanion.app.activities.ChatActivity
import com.sleepcompanion.app.activities.SleepMusicActivity
import com.sleepcompanion.app.databinding.FragmentHomeBinding
import com.sleepcompanion.app.utils.PreferenceManager

class HomeFragment : Fragment() {

    private var _binding: FragmentHomeBinding? = null
    private val binding get() = _binding!!
    private lateinit var prefManager: PreferenceManager

    override fun onCreateView(
        inflater: LayoutInflater,
        container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View {
        _binding = FragmentHomeBinding.inflate(inflater, container, false)
        return binding.root
    }

    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)
        
        prefManager = PreferenceManager(requireContext())
        
        // 设置用户名
        binding.tvWelcome.text = "晚上好，${prefManager.getUsername()}"
        
        // 设置点击事件
        binding.cardChat.setOnClickListener {
            startActivity(Intent(requireContext(), ChatActivity::class.java))
        }
        
        binding.cardSleepTips.setOnClickListener {
            // TODO: 跳转到睡眠小贴士页面
        }
        
        binding.cardSleepStories.setOnClickListener {
            // TODO: 跳转到睡前故事页面
        }
        
        binding.cardSleepMusic.setOnClickListener {
            startActivity(Intent(requireContext(), SleepMusicActivity::class.java))
        }
    }

    override fun onDestroyView() {
        super.onDestroyView()
        _binding = null
    }
}