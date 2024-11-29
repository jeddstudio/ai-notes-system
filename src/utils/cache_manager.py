from typing import Dict, Any, Optional
import hashlib
import json
from datetime import datetime, timedelta

class CacheManager:
    def __init__(self, cache_duration: int = 3600):  # Default 1 hour cache
        self._cache: Dict[str, Dict[str, Any]] = {}
        self.cache_duration = timedelta(seconds=cache_duration)
    
    def _get_cache_key(self, content: str, language: str) -> str:
        """Generate a unique cache key for the content and language"""
        combined = f"{content}:{language}"
        return hashlib.md5(combined.encode()).hexdigest()
    
    def get(self, content: str, language: str) -> Optional[Dict[str, Any]]:
        """Get cached result if it exists and is not expired"""
        cache_key = self._get_cache_key(content, language)
        
        if cache_key in self._cache:
            cache_entry = self._cache[cache_key]
            if datetime.utcnow() - cache_entry["timestamp"] < self.cache_duration:
                return cache_entry["data"]
            else:
                # Remove expired cache entry
                del self._cache[cache_key]
        
        return None
    
    def set(self, content: str, language: str, data: Dict[str, Any]) -> None:
        """Cache the result with timestamp"""
        cache_key = self._get_cache_key(content, language)
        self._cache[cache_key] = {
            "data": data,
            "timestamp": datetime.utcnow()
        }