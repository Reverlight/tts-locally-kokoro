#!/usr/bin/env python3
"""
High-Quality Local English TTS using Kokoro-82M
No API keys, no external services - everything runs locally
"""

import sys
from pathlib import Path
from typing import Optional, Dict, Tuple

try:
    from kokoro import KPipeline
    import soundfile as sf
    import torch
except ImportError:
    print("❌ Missing dependencies. Install with:")
    print("   pip install kokoro soundfile torch")
    sys.exit(1)


class KokoroTTS:
    """
    High-quality local text-to-speech using Kokoro model
    
    Features:
    - 54+ voices across 8 languages
    - Fast synthesis on CPU/GPU
    - Offline mode after initial download
    - No API keys required
    """
    
    VOICES = {
        # American Female
        'af_bella': 'American Female - Bella (default)',
        'af_heart': 'American Female - Heart',
        'af_jessica': 'American Female - Jessica',
        'af_kore': 'American Female - Kore',
        'af_nicole': 'American Female - Nicole',
        'af_nova': 'American Female - Nova',
        'af_river': 'American Female - River',
        'af_sarah': 'American Female - Sarah',
        'af_sky': 'American Female - Sky',
        
        # American Male
        'am_adam': 'American Male - Adam',
        'am_michael': 'American Male - Michael',
        'am_oakley': 'American Male - Oakley',
        'am_onyx': 'American Male - Onyx',
        
        # British Female
        'bf_alice': 'British Female - Alice',
        'bf_emma': 'British Female - Emma',
        'bf_isabella': 'British Female - Isabella',
        
        # British Male
        'bm_fable': 'British Male - Fable',
        'bm_george': 'British Male - George',
        'bm_lewis': 'British Male - Lewis',
    }
    
    def __init__(self, lang_code: str = 'a', output_dir: str = 'audio_output'):
        """
        Initialize Kokoro TTS pipeline
        
        Args:
            lang_code: 'a' for American English, 'b' for British English
            output_dir: Directory to save generated audio files
        """
        self.lang_code = lang_code
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        
        # Detect device
        self.device = 'cuda' if torch.cuda.is_available() else 'cpu'
        
        try:
            self.pipeline = KPipeline(lang_code=lang_code)
            print(f"✅ Kokoro TTS initialized (device: {self.device})")
        except Exception as e:
            print(f"❌ Failed to initialize Kokoro: {e}")
            raise
    
    def list_voices(self) -> Dict[str, str]:
        """Return dictionary of available voices"""
        return self.VOICES.copy()
    
    def generate(
        self,
        text: str,
        voice: str = 'af_bella',
        speed: float = 1.0,
        output_file: Optional[str] = None,
        verbose: bool = True
    ) -> Optional[Tuple[str, int]]:
        """
        Generate speech from text
        
        Args:
            text: Text to convert to speech
            voice: Voice to use (see VOICES dict)
            speed: Speech speed (0.5-2.0, where 1.0 is normal)
            output_file: Output filename (auto-generated if None)
            verbose: Print progress messages
        
        Returns:
            (filepath, sample_rate) tuple or None on error
        """
        # Validate inputs
        if not text or not text.strip():
            print("❌ Text cannot be empty")
            return None
        
        if voice not in self.VOICES:
            print(f"❌ Unknown voice: {voice}")
            print(f"Available voices: {', '.join(self.VOICES.keys())}")
            return None
        
        if not (0.5 <= speed <= 2.0):
            print(f"❌ Speed must be between 0.5 and 2.0 (got {speed})")
            return None
        
        # Generate filename if not provided
        if output_file is None:
            # Use first 20 chars of text + voice name
            text_slug = text[:20].replace(' ', '_').replace('\n', '_')
            output_file = f"speech_{voice}_{text_slug}.wav"
        
        # Ensure .wav extension
        if not output_file.endswith('.wav'):
            output_file += '.wav'
        
        filepath = self.output_dir / output_file
        
        try:
            if verbose:
                print(f"🎙️  Generating: {text[:60]}...")
                print(f"   Voice: {self.VOICES[voice]}")
                print(f"   Speed: {speed}x")
            
            # Generate audio
            samples, sample_rate = self.pipeline(
                text,
                voice=voice,
                speed=speed
            )
            
            # Save audio
            sf.write(str(filepath), samples, sample_rate)
            
            if verbose:
                # Calculate duration
                duration = len(samples) / sample_rate
                print(f"✅ Saved: {filepath}")
                print(f"   Duration: {duration:.1f}s, Sample rate: {sample_rate}Hz")
            
            return (str(filepath), sample_rate)
        
        except Exception as e:
            print(f"❌ Error generating speech: {e}")
            return None
    
    def generate_batch(
        self,
        texts: list,
        voice: str = 'af_bella',
        speed: float = 1.0,
        prefix: str = 'batch'
    ) -> list:
        """
        Generate multiple audio files
        
        Args:
            texts: List of text strings
            voice: Voice to use for all
            speed: Speed for all
            prefix: Prefix for output filenames
        
        Returns:
            List of (filepath, sample_rate) tuples
        """
        results = []
        print(f"\n🔄 Generating {len(texts)} audio files with {self.VOICES[voice]}...\n")
        
        for i, text in enumerate(texts, 1):
            output_file = f"{prefix}_{i:03d}.wav"
            result = self.generate(
                text,
                voice=voice,
                speed=speed,
                output_file=output_file,
                verbose=True
            )
            if result:
                results.append(result)
            print()
        
        return results
    
    def demo(self):
        """Run a demonstration with multiple voices"""
        print("\n" + "="*70)
        print("KOKORO TTS - LOCAL HIGH-QUALITY TEXT-TO-SPEECH DEMO")
        print("="*70 + "\n")
        
        demo_text = (
            "Welcome to Kokoro, a lightweight yet powerful text-to-speech model. "
            "This audio was generated completely locally, without any API keys or "
            "external services. Kokoro delivers high quality audio comparable to "
            "much larger models."
        )
        
        # Demo with different voices
        demo_voices = [
            'af_bella',   # Default female
            'am_michael', # Male
            'af_sarah',   # Alternative female
        ]
        
        print(f"Demo text: {demo_text}\n")
        
        for voice in demo_voices:
            if voice in self.VOICES:
                self.generate(
                    demo_text,
                    voice=voice,
                    speed=1.0,
                    output_file=f"demo_{voice}.wav"
                )
                print()


def main():
    """Example usage"""
    
    # Initialize TTS
    tts = KokoroTTS(output_dir='audio_output')
    
    # Run demo
    tts.demo()
    
    # Example 1: Single text with different voices
    print("\n" + "="*70)
    print("EXAMPLE 1: Single Text, Multiple Voices")
    print("="*70 + "\n")
    
    text = "Kokoro is lightweight and efficient for local text-to-speech synthesis."
    
    for voice in ['af_nicole', 'am_adam', 'bf_emma']:
        tts.generate(text, voice=voice, output_file=f"example1_{voice}.wav")
        print()
    
    # Example 2: Different speeds
    print("\n" + "="*70)
    print("EXAMPLE 2: Different Speech Speeds")
    print("="*70 + "\n")
    
    text = "Listen to this text spoken at different speeds."
    
    for speed in [0.8, 1.0, 1.2, 1.5]:
        tts.generate(
            text,
            voice='af_bella',
            speed=speed,
            output_file=f"example2_speed_{speed}.wav"
        )
        print()
    
    # Example 3: Batch processing
    print("\n" + "="*70)
    print("EXAMPLE 3: Batch Processing Multiple Texts")
    print("="*70 + "\n")
    
    texts = [
        "First paragraph of content.",
        "Second paragraph with different information.",
        "Third and final paragraph.",
    ]
    
    tts.generate_batch(texts, voice='af_sarah', prefix='example3_paragraph')
    
    # Show available voices
    print("\n" + "="*70)
    print("AVAILABLE VOICES")
    print("="*70 + "\n")
    
    print("American Voices:")
    for code, name in sorted(tts.list_voices().items()):
        if code.startswith('af_') or code.startswith('am_'):
            print(f"  {code:15} - {name}")
    
    print("\nBritish Voices:")
    for code, name in sorted(tts.list_voices().items()):
        if code.startswith('bf_') or code.startswith('bm_'):
            print(f"  {code:15} - {name}")
    
    print("\n✅ All examples completed! Check ./audio_output/ for files.\n")


if __name__ == '__main__':
    main()
