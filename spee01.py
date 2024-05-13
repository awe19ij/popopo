import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

plt.rcParams['font.family'] = 'Malgun Gothic'  
plt.rcParams['axes.unicode_minus'] = False  # 마이너스 기호 설정

import parselmouth
import numpy as np

# 음성 파일 로드
sound = parselmouth.Sound("C:\\Users\\iseo\\Desktop\\aibase04\\fast.wav")

# 피치 분석
pitch = sound.to_pitch()
pitch_values = pitch.selected_array['frequency']
pitch_times = pitch.xs()

# 피치 범위 필터링
pitch_values_filtered = np.where((pitch_values >= 150) & (pitch_values <= 300), pitch_values, np.nan)

# 강도 분석
intensity = sound.to_intensity()
intensity_values = intensity.values.T
intensity_times = intensity.xs()

# 강도 범위 필터링
intensity_values_filtered = np.where((intensity_values >= 45) & (intensity_values <= 70), intensity_values, np.nan)

# 그래프 그리기
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8))

# 피치 그래프
ax1.plot(pitch_times, pitch_values, 'o', markersize=2, label='Pitch')
ax1.plot(pitch_times, pitch_values_filtered, 'o', markersize=2, color='red', label='Highlighted Pitch (150-300 Hz)')
ax1.set_xlabel('Time (s)')
ax1.set_ylabel('Frequency (Hz)')
ax1.set_title('피치')
ax1.set_xlim([0, max(pitch_times)])
ax1.set_ylim([0, 500])
ax1.grid(True)
ax1.legend()
ax1.set_xticks(np.arange(0, max(pitch_times), 1))

# 강도 그래프
ax2.plot(intensity_times, intensity_values, linewidth=1, label='Intensity')
ax2.plot(intensity_times, intensity_values_filtered, linewidth=3, color='red', label='Highlighted Intensity (45-70 dB)')
ax2.set_xlabel('Time (s)')
ax2.set_ylabel('Intensity (dB)')
ax2.set_title('강도')
ax2.set_xlim([0, max(intensity_times)])
ax2.set_ylim([0, max(intensity_values)])
ax2.grid(True)
ax2.legend()
ax2.set_xticks(np.arange(0, max(intensity_times), 1))

plt.tight_layout()
plt.show()
