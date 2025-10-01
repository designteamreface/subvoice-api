from http.server import BaseHTTPRequestHandler
import json
import base64
import requests
from urllib.parse import parse_qs
import os

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            # Get content length
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            
            # Parse JSON data
            data = json.loads(post_data.decode('utf-8'))
            
            # Extract parameters
            api_key = data.get('api_key')
            text = data.get('text', '')
            voice_id = data.get('voice_id')
            stability = float(data.get('stability', 0.5))
            style = float(data.get('style', 0.3))
            
            # Validate required parameters
            if not api_key:
                self.send_error_response(400, 'API key is required')
                return
            
            if not text:
                self.send_error_response(400, 'Text is required')
                return
            
            if not voice_id:
                self.send_error_response(400, 'Voice ID is required')
                return
            
            # Generate audio using ElevenLabs API
            result = self.text_to_speech(api_key, text, voice_id, stability, style)
            
            if result['success']:
                self.send_success_response(result)
            else:
                self.send_error_response(500, result['error'])
                
        except Exception as e:
            self.send_error_response(500, f'Internal server error: {str(e)}')
    
    def do_OPTIONS(self):
        # Handle CORS preflight
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
    
    def send_success_response(self, result):
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        
        response = {
            'success': True,
            'audio_base64': result['audio_base64'],
            'timestamps': result['timestamps']
        }
        
        self.wfile.write(json.dumps(response).encode('utf-8'))
    
    def send_error_response(self, status_code, message):
        self.send_response(status_code)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        
        response = {
            'success': False,
            'error': message
        }
        
        self.wfile.write(json.dumps(response).encode('utf-8'))
    
    def text_to_speech(self, api_key, text, voice_id, stability, style):
        """
        Generate speech using ElevenLabs API
        """
        try:
            url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}/with-timestamps"
            
            payload = {
                "text": text,
                "model_id": "eleven_turbo_v2_5",
                "voice_settings": {
                    "stability": stability,
                    "style": style,
                    "use_speaker_boost": True
                },
                "generation_config": {
                    "chunk_length_schedule": [120, 160, 250, 290]
                }
            }
            
            headers = {
                "xi-api-key": api_key,
                "Content-Type": "application/json"
            }
            
            response = requests.post(url, json=payload, headers=headers, timeout=30)
            
            if response.status_code == 200:
                response_dict = response.json()
                audio_base64 = response_dict["audio_base64"]
                
                # Extract timestamps
                timestamps = {}
                if 'alignment' in response_dict:
                    timestamps = {
                        'characters': response_dict['alignment']['characters'],
                        'character_start_times_seconds': response_dict['alignment']['character_start_times_seconds'],
                        'character_end_times_seconds': response_dict['alignment']['character_end_times_seconds']
                    }
                else:
                    # Fallback for older API versions
                    timestamps = {
                        'characters': response_dict.get('characters', []),
                        'character_start_times_seconds': response_dict.get('character_start_times_seconds', []),
                        'character_end_times_seconds': response_dict.get('character_end_times_seconds', [])
                    }
                
                return {
                    'success': True,
                    'audio_base64': audio_base64,
                    'timestamps': timestamps
                }
            else:
                return {
                    'success': False,
                    'error': f"ElevenLabs API error: {response.status_code}, {response.text}"
                }
                
        except requests.exceptions.Timeout:
            return {
                'success': False,
                'error': 'Request timeout - ElevenLabs API took too long to respond'
            }
        except requests.exceptions.RequestException as e:
            return {
                'success': False,
                'error': f'Network error: {str(e)}'
            }
        except Exception as e:
            return {
                'success': False,
                'error': f'Unexpected error: {str(e)}'
            }
