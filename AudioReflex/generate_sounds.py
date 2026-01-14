
import wave
import struct
import math

def generate_sound(file_name, duration_ms, frequency):
    """ Generates a WAV file with a simple sine wave tone. """
    sample_rate = 44100
    num_samples = int(sample_rate * duration_ms / 1000)
    max_amplitude = 32767  # 16-bit audio

    with wave.open(file_name, 'w') as wav_file:
        wav_file.setnchannels(1)  # Mono
        wav_file.setsampwidth(2)  # 16-bit
        wav_file.setframerate(sample_rate)

        for i in range(num_samples):
            angle = 2 * math.pi * frequency * i / sample_rate
            sample = int(max_amplitude * math.sin(angle))
            wav_file.writeframes(struct.pack('<h', sample))

if __name__ == '__main__':
    print("Generating sound files...")
    # Game sounds
    generate_sound('target.wav', 200, 440)
    generate_sound('success.wav', 150, 880)
    generate_sound('failure.wav', 300, 220)
    # UI sounds
    generate_sound('navigate.wav', 50, 1200)
    generate_sound('select.wav', 100, 700)
    generate_sound('back.wav', 100, 500)
    print("Sound files generated: target.wav, success.wav, failure.wav, navigate.wav, select.wav, back.wav")
