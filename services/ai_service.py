import google.generativeai as genai
from config import Config
import json
import os

class AIService:
    def __init__(self):
        genai.configure(api_key=Config.GEMINI_API_KEY)
        self.model = genai.GenerativeModel('gemini-2.0-flash')

    def analyze_video(self, video_path):
        """
        Uploads video to Gemini and generates metadata.
        Automatically compresses videos >500 MB.
        """
        from utils.video_compressor import compress_video
        
        # Check file size
        file_size_mb = os.path.getsize(video_path) / (1024 * 1024)
        print(f"Video file size: {file_size_mb:.2f} MB")
        
        # Compress if too large
        compressed_path = None
        analysis_path = video_path
        
        if file_size_mb > 500:
            print(f"Video exceeds 500 MB limit. Compressing...")
            compressed_path = video_path.replace('.mp4', '_compressed.mp4').replace('.mov', '_compressed.mov').replace('.m4v', '_compressed.m4v')
            
            result = compress_video(video_path, compressed_path, target_size_mb=450)
            
            if result:
                analysis_path = compressed_path
                compressed_size = os.path.getsize(compressed_path) / (1024 * 1024)
                print(f"Using compressed video for analysis: {compressed_size:.2f} MB")
            else:
                raise Exception("Failed to compress video. Cannot process files >500 MB.")
        
        try:
            print(f"Uploading {analysis_path} to Gemini...")
            video_file = genai.upload_file(path=analysis_path)
            
            # Wait for processing with timeout
            import time
            max_wait_time = 600
            start_time = time.time()
            
            while video_file.state.name == "PROCESSING":
                elapsed = time.time() - start_time
                if elapsed > max_wait_time:
                    raise Exception(f"Video processing timeout after {max_wait_time} seconds")
                print(f"Waiting for video processing... ({elapsed:.0f}s elapsed)")
                time.sleep(10)
                video_file = genai.get_file(video_file.name)

            if video_file.state.name == "FAILED":
                raise Exception("Video processing failed.")

            prompt = """
            Analyze this video and generate the following outputs in JSON format:
            1. "title": A YouTube title, 60 chars or less, engaging, no clickbait.
            2. "description": 2-3 SEO-optimized paragraphs summarizing the video, including 5-10 hashtags.
            3. "thumbnail_prompt": A detailed prompt for generating a unique, eye-catching thumbnail image.
            
            The JSON should look like:
            {
                "title": "...",
                "description": "...",
                "thumbnail_prompt": "..."
            }
            """
            
            print("Generating analysis...")
            response = self.model.generate_content(
                [video_file, prompt],
                generation_config={"response_mime_type": "application/json"}
            )
            
            text_response = response.text.strip()
            print(f"DEBUG: Raw AI Response: {text_response}")

            if text_response.startswith('```json'):
                text_response = text_response[7:-3]
            elif text_response.startswith('```'):
                 text_response = text_response[3:-3]
            
            parsed_response = json.loads(text_response)
            
            if isinstance(parsed_response, list) and len(parsed_response) > 0:
                parsed_response = parsed_response[0]
            
            return parsed_response
            
        finally:
            # Clean up compressed file
            if compressed_path and os.path.exists(compressed_path):
                print(f"Cleaning up compressed file: {compressed_path}")
                os.remove(compressed_path)

    def generate_thumbnail(self, prompt, output_path, title=""):
        """
        Generates a UNIQUE thumbnail using DALL-E 3 with completely randomized styling.
        """
        try:
            from openai import OpenAI
            import requests
            import random
            
            if Config.OPENAI_API_KEY == 'YOUR_OPENAI_API_KEY_HERE':
                raise Exception("OpenAI API key not configured")
            
            client = OpenAI(api_key=Config.OPENAI_API_KEY)
            
            # COMPLETE RANDOMIZATION for unique thumbnails
            styles = [
                "minimalist modern design",
                "bold graphic poster style", 
                "cinematic movie poster",
                "abstract artistic composition",
                "photorealistic dramatic scene",
                "flat design illustration",
                "vintage film aesthetic",
                "neon cyberpunk style",
                "watercolor painting",
                "3D rendered scene",
                "comic book art style",
                "retro 80s aesthetic"
            ]
            
            color_schemes = [
                "vibrant saturated colors",
                "muted earth tones",
                "monochrome black and white with one accent color",
                "pastel soft colors",
                "high contrast bold colors",
                "warm sunset palette (oranges, reds, yellows)",
                "cool blue and teal tones",
                "neon bright accents on dark background",
                "natural green and brown tones",
                "purple and pink gradient"
            ]
            
            compositions = [
                "centered symmetrical composition",
                "rule of thirds layout",
                "asymmetric dynamic composition",
                "close-up dramatic shot",
                "wide establishing shot",
                "diagonal leading lines",
                "circular focal point",
                "split screen composition"
            ]
            
            # Randomly select unique characteristics
            style = random.choice(styles)
            colors = random.choice(color_schemes)
            composition = random.choice(compositions)
            
            # Enhanced prompt with randomization
            enhanced_prompt = f"""Create a YouTube thumbnail in 16:9 landscape format.

Content: {prompt}

UNIQUE STYLE FOR THIS THUMBNAIL:
- Art Style: {style}
- Color Scheme: {colors}
- Composition: {composition}
- Professional quality, eye-catching
- Leave space for text overlay
- NO text in the image itself

Make this thumbnail visually distinct and unique."""
            
            print(f"Generating UNIQUE thumbnail:")
            print(f"  Style: {style}")
            print(f"  Colors: {colors}")
            print(f"  Composition: {composition}")
            
            response = client.images.generate(
                model="dall-e-3",
                prompt=enhanced_prompt,
                size="1792x1024",
                quality="hd",
                n=1
            )
            
            image_url = response.data[0].url
            print(f"Downloading generated image...")
            
            image_response = requests.get(image_url)
            if image_response.status_code == 200:
                with open(output_path, 'wb') as f:
                    f.write(image_response.content)
                print(f"DALL-E 3 thumbnail saved")
                
                self._resize_and_compress_thumbnail(output_path)
                
                if title:
                    self._add_ultra_randomized_title_overlay(output_path, title)
            else:
                raise Exception(f"Failed to download image: {image_response.status_code}")
                
        except Exception as e:
            print(f"Error generating DALL-E thumbnail: {e}")
            self._create_fallback_thumbnail(prompt, output_path, title)

    def _add_ultra_randomized_title_overlay(self, image_path, title):
        """
        Adds COMPLETELY randomized title text - different every time.
        """
        from PIL import Image, ImageDraw, ImageFont
        import random
        
        img = Image.open(image_path)
        draw = ImageDraw.Draw(img)
        
        # Random font size (40-120)
        font_size = random.randint(40, 120)
        
        # Extended font options
        font_options = [
            ("impact.ttf", "Impact"),
            ("arial.ttf", "Arial"),
            ("arialbd.ttf", "Arial Bold"),
            ("comic.ttf", "Comic Sans"),
            ("verdanab.ttf", "Verdana Bold"),
            ("times.ttf", "Times New Roman"),
            ("georgia.ttf", "Georgia"),
            ("trebuc.ttf", "Trebuchet"),
            ("calibri.ttf", "Calibri"),
            ("consola.ttf", "Consolas")
        ]
        
        font = None
        font_name = "Default"
        random.shuffle(font_options)
        
        for font_file, name in font_options:
            try:
                font = ImageFont.truetype(font_file, font_size)
                font_name = name
                break
            except:
                continue
        
        if font is None:
            font = ImageFont.load_default()
        
        # EXPANDED color options (not just vibrant)
        color_options = [
            (255, 255, 255),  # White
            (0, 0, 0),        # Black
            (255, 255, 100),  # Yellow
            (255, 100, 255),  # Magenta
            (100, 255, 255),  # Cyan
            (255, 150, 0),    # Orange
            (150, 255, 100),  # Lime
            (255, 200, 0),    # Gold
            (200, 50, 50),    # Red
            (50, 150, 255),   # Blue
            (150, 50, 200),   # Purple
            (255, 180, 200),  # Pink
            (100, 100, 100),  # Gray
        ]
        text_color = random.choice(color_options)
        
        # Wrap text
        max_width = 1150
        words = title.split()
        lines = []
        current_line = []
        
        for word in words:
            test_line = ' '.join(current_line + [word])
            bbox = draw.textbbox((0, 0), test_line, font=font)
            if bbox[2] - bbox[0] <= max_width:
                current_line.append(word)
            else:
                if current_line:
                    lines.append(' '.join(current_line))
                current_line = [word]
        if current_line:
            lines.append(' '.join(current_line))
        
        lines = lines[:2]
        
        # 9 position options (3x3 grid)
        position_options = [
            30,   # Top
            150,  # Top-mid
            280,  # Mid-top
            400,  # Center
            520,  # Mid-bottom
            600,  # Bottom
        ]
        y_start = random.choice(position_options)
        
        # Random alignment
        alignment = random.choice(['left', 'center', 'right'])
        
        # Random text effects
        effects = ['shadow', 'outline', 'glow', 'none']
        effect = random.choice(effects)
        
        print(f"Text styling: {font_name} {font_size}px, {alignment}, RGB{text_color}, Effect: {effect}")
        
        # Draw text with effect
        for i, line in enumerate(lines):
            bbox = draw.textbbox((0, 0), line, font=font)
            text_width = bbox[2] - bbox[0]
            
            if alignment == 'center':
                x = (1280 - text_width) // 2
            elif alignment == 'right':
                x = 1280 - text_width - 50
            else:
                x = 50
            
            y = y_start + (i * (font_size + 20))
            
            # Apply effect
            if effect == 'shadow':
                draw.text((x + 5, y + 5), line, fill=(0, 0, 0), font=font)
            elif effect == 'outline':
                for offset_x in range(-3, 4):
                    for offset_y in range(-3, 4):
                        draw.text((x + offset_x, y + offset_y), line, fill=(0, 0, 0), font=font)
            elif effect == 'glow':
                for offset in range(1, 8):
                    alpha = int(255 * (1 - offset/8))
                    draw.text((x, y), line, fill=(255, 255, 255, alpha), font=font)
            
            # Draw main text
            draw.text((x, y), line, fill=text_color, font=font)
        
        img.save(image_path, 'JPEG', quality=95)
        print(f"Added ultra-randomized title overlay")

    def _create_fallback_thumbnail(self, prompt, output_path, title):
        """Fallback thumbnail generator"""
        from PIL import Image, ImageDraw, ImageFont
        import random
        
        # Random gradient colors
        color1 = (random.randint(20, 100), random.randint(20, 100), random.randint(20, 100))
        color2 = (random.randint(100, 200), random.randint(50, 150), random.randint(50, 200))
        
        img = Image.new('RGB', (1280, 720), color=color1)
        draw = ImageDraw.Draw(img)
        
        # Gradient
        for i in range(720):
            r = int(color1[0] + (color2[0] - color1[0]) * i / 720)
            g = int(color1[1] + (color2[1] - color1[1]) * i / 720)
            b = int(color1[2] + (color2[2] - color1[2]) * i / 720)
            draw.line([(0, i), (1280, i)], fill=(r, g, b))
        
        img.save(output_path, 'JPEG', quality=90)
        print(f"Generated fallback thumbnail")

    def _resize_and_compress_thumbnail(self, image_path, target_size=(1280, 720), max_size_mb=2):
        """Resizes and compresses thumbnail"""
        from PIL import Image
        
        img = Image.open(image_path)
        img = img.resize(target_size, Image.Resampling.LANCZOS)
        img.save(image_path, 'JPEG', quality=90, optimize=True)
        
        file_size_mb = os.path.getsize(image_path) / (1024 * 1024)
        
        if file_size_mb <= max_size_mb:
            return
        
        # Compress further if needed
        quality = 85
        while quality > 20:
            img.save(image_path, 'JPEG', quality=quality, optimize=True)
            new_size_mb = os.path.getsize(image_path) / (1024 * 1024)
            
            if new_size_mb <= max_size_mb:
                print(f"Compressed to {new_size_mb:.2f} MB (quality={quality})")
                return
            
            quality -= 10
        
        print(f"Warning: Could not compress below {max_size_mb} MB")
