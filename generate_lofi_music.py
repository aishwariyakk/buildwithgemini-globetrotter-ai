import math
import wave
import struct
import random

SAMPLE_RATE = 44100
DURATION = 42  # seconds

def note_freq(note_str):
    notes = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
    name = note_str[:-1]
    octave = int(note_str[-1])
    idx = notes.index(name)
    # A4 = 440 Hz = 69
    midi = (octave + 1) * 12 + idx
    return 440.0 * (2 ** ((midi - 69) / 12.0))

# Upbeat Lo-Fi Chords: Cmaj7, Am7, Dm7, G13
chords = [
    [note_freq('C3'), note_freq('E3'), note_freq('G3'), note_freq('B3'), note_freq('D4')],
    [note_freq('A2'), note_freq('C3'), note_freq('E3'), note_freq('G3'), note_freq('B3')],
    [note_freq('D3'), note_freq('F3'), note_freq('A3'), note_freq('C4'), note_freq('E4')],
    [note_freq('G2'), note_freq('B2'), note_freq('D3'), note_freq('F3'), note_freq('E4')],
]

def generate_lofi():
    out_path = "/config/Desktop/Session1/globetrotter-ai/lofi_beat.wav"
    total_samples = int(SAMPLE_RATE * DURATION)
    num_channels = 2
    
    bpm = 85
    beat_sec = 60.0 / bpm
    bar_sec = beat_sec * 4

    samples = [0.0] * total_samples

    # 1. Generate Warm Electric Piano / Rhodes Synth Chords
    for i in range(total_samples):
        t = i / SAMPLE_RATE
        bar_idx = int(t / bar_sec) % len(chords)
        bar_pos = t % bar_sec
        current_chord = chords[bar_idx]

        # Envelope
        chord_env = math.exp(-bar_pos * 0.8) * 0.25

        chord_val = 0.0
        for freq in current_chord:
            # Warm sine wave + soft 2nd harmonic
            sig = math.sin(2 * math.pi * freq * t) + 0.3 * math.sin(4 * math.pi * freq * t)
            chord_val += sig

        samples[i] += chord_val * chord_env

    # 2. Add Upbeat Lo-Fi Drums (Kick, Snare/Clap, Hi-Hat)
    for beat_idx in range(int(DURATION / beat_sec)):
        beat_start_time = beat_idx * beat_sec
        beat_start_sample = int(beat_start_time * SAMPLE_RATE)
        beat_in_bar = beat_idx % 4

        # Kick on 1 and 2.5
        is_kick = (beat_in_bar == 0) or (beat_in_bar == 2 and random.random() > 0.3)
        # Snare/Rimshot on 2 and 4
        is_snare = (beat_in_bar == 1 or beat_in_bar == 3)
        # Hi-hat on every 8th note
        
        # Kick sound
        if is_kick:
            dur = int(0.12 * SAMPLE_RATE)
            for k in range(min(dur, total_samples - beat_start_sample)):
                tk = k / SAMPLE_RATE
                f = 130 * math.exp(-tk * 35)
                amp = math.exp(-tk * 15) * 0.4
                samples[beat_start_sample + k] += math.sin(2 * math.pi * f * tk) * amp

        # Snare sound
        if is_snare:
            dur = int(0.15 * SAMPLE_RATE)
            for k in range(min(dur, total_samples - beat_start_sample)):
                tk = k / SAMPLE_RATE
                noise = (random.random() * 2 - 1)
                body = math.sin(2 * math.pi * 180 * tk) * math.exp(-tk * 30)
                amp = math.exp(-tk * 18) * 0.25
                samples[beat_start_sample + k] += (noise * 0.7 + body * 0.3) * amp

        # Hi-Hats (every 0.5 beat)
        for sub in [0, 0.5]:
            hh_start = beat_start_sample + int(sub * beat_sec * SAMPLE_RATE)
            dur = int(0.05 * SAMPLE_RATE)
            for k in range(min(dur, total_samples - hh_start)):
                tk = k / SAMPLE_RATE
                noise = (random.random() * 2 - 1)
                amp = math.exp(-tk * 50) * 0.12
                if hh_start + k < total_samples:
                    samples[hh_start + k] += noise * amp

    # 3. Add Subtle Analog Vinyl Crackle
    for i in range(total_samples):
        if random.random() < 0.002:
            pop = (random.random() * 2 - 1) * 0.08
            samples[i] += pop

    # Write WAV file
    with wave.open(out_path, 'w') as wf:
        wf.setnchannels(num_channels)
        wf.setsampwidth(2)  # 16-bit
        wf.setframerate(SAMPLE_RATE)
        
        packed_data = bytearray()
        for s in samples:
            # Soft clipping / limiting
            clamped = max(-0.95, min(0.95, s))
            val = int(clamped * 32767)
            # Stereo left & right
            packed_data.extend(struct.pack('<hh', val, val))
        
        wf.writeframes(packed_data)

    print(f"Generated upbeat lo-fi audio track: {out_path}")
    return out_path

if __name__ == "__main__":
    generate_lofi()
