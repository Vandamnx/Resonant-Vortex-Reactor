"""
Schumann Resonance + Healing Frequency Harmonics - Starter Stub
Resonant Vortex Reactor (RVR) Project - Version 4.0.6 / 4.1

Generates the target frequency set used for "restorative molecular coherence"
tuning in the Molecular Healing Head (MHH v4.1).

Frequencies:
- Schumann fundamental: 7.83 Hz (Earth's natural resonance)
- Healing sweet spots: 432 Hz, 528 Hz, 741 Hz (commonly cited in sound healing)

Outputs:
- Matplotlib visualization (time + frequency domain)
- healing_tone_v4_stub.wav file you can actually play

Run: python schumann_harmonics_stub.py
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.fft import fft, fftfreq
from scipy.io.wavfile import write

# === Audio parameters ===
fs = 44100          # sample rate in Hz (standard CD quality)
duration = 8.0      # seconds of audio
t = np.linspace(0, duration, int(fs * duration))

# === Target frequencies from the spec ===
schumann_fundamental = 7.83
healing_sweet_spots = [432, 528, 741]   # "sweet spots" for restorative tuning

# Build composite waveform
# Schumann is dominant; healing harmonics are added at lower amplitude
signal = np.sin(2 * np.pi * schumann_fundamental * t) * 0.85
for freq in healing_sweet_spots:
    signal += 0.22 * np.sin(2 * np.pi * freq * t)

signal = signal / np.max(np.abs(signal))   # normalize to [-1, 1]

# === Visualization ===
plt.figure(figsize=(11, 7))

# Time domain (first ~0.5 seconds so you can see the waveform)
plt.subplot(2, 1, 1)
plt.plot(t[:22050], signal[:22050], color='#00B4D8', linewidth=0.9)
plt.title('Composite Signal: Schumann 7.83 Hz + Healing Harmonics (432 / 528 / 741 Hz)', fontsize=12)
plt.xlabel('Time (s)')
plt.ylabel('Amplitude')
plt.grid(True, alpha=0.3)

# Frequency spectrum (zoomed to show the important low-frequency range)
N = len(signal)
yf = fft(signal)
xf = fftfreq(N, 1/fs)[:N//2]

plt.subplot(2, 1, 2)
plt.plot(xf[:180], 2.0/N * np.abs(yf[:180]), color='#E63946', linewidth=1.1)
plt.title('Frequency Spectrum (0â180 Hz) â Note the peaks at target frequencies', fontsize=12)
plt.xlabel('Frequency (Hz)')
plt.ylabel('Amplitude')
plt.axvline(x=7.83, color='green', linestyle='--', alpha=0.85, label='Schumann 7.83 Hz')
for h in healing_sweet_spots:
    plt.axvline(x=h, color='purple', linestyle=':', alpha=0.75, linewidth=1.5)
plt.legend(loc='upper right')
plt.grid(True, alpha=0.3)

plt.tight_layout()
plt.show()

# === Save audible WAV file ===
output_filename = 'healing_tone_v4_stub.wav'
write(output_filename, fs, (signal * 32767).astype(np.int16))

print("=== Frequency Tuning Stub Complete ===")
print(f"Saved audio file: {output_filename}")
print("Play this file on any device or headphones to physically experience")
print("the exact frequency combination used in the Molecular Healing Head v4.1 tu