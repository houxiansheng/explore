package com.sleepcompanion.app.activities

import android.media.MediaPlayer
import android.os.Bundle
import android.view.MenuItem
import android.widget.SeekBar
import androidx.appcompat.app.AppCompatActivity
import com.sleepcompanion.app.R
import com.sleepcompanion.app.databinding.ActivitySleepMusicBinding
import com.sleepcompanion.app.models.MusicItem
import java.util.Timer
import java.util.TimerTask

class SleepMusicActivity : AppCompatActivity() {

    private lateinit var binding: ActivitySleepMusicBinding
    private var mediaPlayer: MediaPlayer? = null
    private var timer: Timer? = null
    
    // 示例音乐列表
    private val musicList = listOf(
        MusicItem(1, "轻柔雨声", R.raw.rain, "大自然的声音，帮助放松身心"),
        MusicItem(2, "森林夜晚", R.raw.forest, "森林中的虫鸣鸟叫，营造宁静氛围"),
        MusicItem(3, "海浪声", R.raw.waves, "海浪拍打岸边的声音，带来平静"),
        MusicItem(4, "轻音乐", R.raw.soft_music, "舒缓的钢琴曲，助你入眠"),
        MusicItem(5, "白噪音", R.raw.white_noise, "均匀的白噪音，屏蔽外界干扰")
    )
    
    private var currentMusicIndex = 0

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        binding = ActivitySleepMusicBinding.inflate(layoutInflater)
        setContentView(binding.root)
        
        setupActionBar()
        setupMusicList()
        setupControls()
    }
    
    private fun setupActionBar() {
        setSupportActionBar(binding.toolbar)
        supportActionBar?.apply {
            setDisplayHomeAsUpEnabled(true)
            setDisplayShowHomeEnabled(true)
            title = "助眠音乐"
        }
    }
    
    private fun setupMusicList() {
        // 在实际应用中，这里应该使用RecyclerView显示音乐列表
        // 这里为了简化，我们直接加载第一首音乐
        loadMusic(0)
    }
    
    private fun setupControls() {
        binding.btnPlay.setOnClickListener {
            if (mediaPlayer?.isPlaying == true) {
                pauseMusic()
            } else {
                playMusic()
            }
        }
        
        binding.btnNext.setOnClickListener {
            playNextMusic()
        }
        
        binding.btnPrevious.setOnClickListener {
            playPreviousMusic()
        }
        
        binding.seekBar.setOnSeekBarChangeListener(object : SeekBar.OnSeekBarChangeListener {
            override fun onProgressChanged(seekBar: SeekBar?, progress: Int, fromUser: Boolean) {
                if (fromUser) {
                    mediaPlayer?.seekTo(progress)
                }
            }
            
            override fun onStartTrackingTouch(seekBar: SeekBar?) {}
            
            override fun onStopTrackingTouch(seekBar: SeekBar?) {}
        })
        
        binding.btnTimer.setOnClickListener {
            // 设置定时关闭
            // 在实际应用中，这里应该显示一个对话框让用户选择时间
            setTimer(30) // 30分钟后停止播放
        }
    }
    
    private fun loadMusic(index: Int) {
        currentMusicIndex = index
        val music = musicList[index]
        
        binding.tvMusicTitle.text = music.title
        binding.tvMusicDescription.text = music.description
        
        // 释放之前的MediaPlayer
        releaseMediaPlayer()
        
        // 创建新的MediaPlayer
        mediaPlayer = MediaPlayer.create(this, music.resourceId)
        mediaPlayer?.setOnCompletionListener {
            // 播放完成后自动播放下一首
            playNextMusic()
        }
        
        // 更新进度条最大值
        binding.seekBar.max = mediaPlayer?.duration ?: 0
        
        // 自动开始播放
        playMusic()
    }
    
    private fun playMusic() {
        mediaPlayer?.start()
        binding.btnPlay.setImageResource(R.drawable.ic_pause)
        
        // 启动进度条更新
        startProgressUpdate()
    }
    
    private fun pauseMusic() {
        mediaPlayer?.pause()
        binding.btnPlay.setImageResource(R.drawable.ic_play)
        
        // 停止进度条更新
        stopProgressUpdate()
    }
    
    private fun playNextMusic() {
        val nextIndex = (currentMusicIndex + 1) % musicList.size
        loadMusic(nextIndex)
    }
    
    private fun playPreviousMusic() {
        val prevIndex = if (currentMusicIndex > 0) currentMusicIndex - 1 else musicList.size - 1
        loadMusic(prevIndex)
    }
    
    private fun startProgressUpdate() {
        timer?.cancel()
        timer = Timer()
        timer?.scheduleAtFixedRate(object : TimerTask() {
            override fun run() {
                runOnUiThread {
                    if (mediaPlayer != null) {
                        binding.seekBar.progress = mediaPlayer!!.currentPosition
                        
                        // 更新时间显示
                        val currentPosition = mediaPlayer!!.currentPosition / 1000
                        val duration = mediaPlayer!!.duration / 1000
                        binding.tvCurrentTime.text = String.format("%02d:%02d", currentPosition / 60, currentPosition % 60)
                        binding.tvTotalTime.text = String.format("%02d:%02d", duration / 60, duration % 60)
                    }
                }
            }
        }, 0, 1000)
    }
    
    private fun stopProgressUpdate() {
        timer?.cancel()
    }
    
    private fun setTimer(minutes: Int) {
        // 在实际应用中，这里应该显示一个倒计时
        // 这里为了简化，我们只显示一个提示
        val milliseconds = minutes * 60 * 1000L
        
        // 创建一个定时器，在指定时间后停止播放
        Timer().schedule(object : TimerTask() {
            override fun run() {
                runOnUiThread {
                    pauseMusic()
                }
            }
        }, milliseconds)
    }
    
    private fun releaseMediaPlayer() {
        mediaPlayer?.stop()
        mediaPlayer?.release()
        mediaPlayer = null
    }
    
    override fun onOptionsItemSelected(item: MenuItem): Boolean {
        if (item.itemId == android.R.id.home) {
            finish()
            return true
        }
        return super.onOptionsItemSelected(item)
    }
    
    override fun onDestroy() {
        super.onDestroy()
        releaseMediaPlayer()
        timer?.cancel()
    }
}