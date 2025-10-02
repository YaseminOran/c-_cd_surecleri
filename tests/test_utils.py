#!/usr/bin/env python3
"""
Basit Utils Testleri - CI/CD Pipeline için
"""

import pytest
import sys
import os

# Src dizinini path'e ekle
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from utils import validate_input, format_response

class TestInputValidation:
    """Input validasyon testleri"""
    
    def test_validate_input_valid_data(self):
        """Geçerli veri validasyonu"""
        valid_data = {'value': 50}
        
        result = validate_input(valid_data)
        
        assert result['valid'] is True
        assert 'message' in result
    
    def test_validate_input_invalid_data(self):
        """Geçersiz veri validasyonu"""
        invalid_data = {'invalid': 'data'}
        
        result = validate_input(invalid_data)
        
        assert result['valid'] is False
        assert 'message' in result
    
    def test_validate_input_empty_data(self):
        """Boş veri validasyonu"""
        empty_data = {}
        
        result = validate_input(empty_data)
        
        assert result['valid'] is False
        assert 'message' in result
    
    def test_validate_input_none_data(self):
        """None veri validasyonu"""
        result = validate_input(None)
        
        assert result['valid'] is False
        assert 'message' in result

class TestResponseFormatting:
    """Response formatlama testleri"""
    
    def test_format_response_basic(self):
        """Temel response formatlama"""
        prediction = 0.75
        input_data = {'value': 60}
        
        result = format_response(prediction, input_data)
        
        assert 'prediction' in result
        assert 'status' in result
        assert result['status'] == 'success'
        assert result['prediction'] == prediction
    
    def test_format_response_low_prediction(self):
        """Düşük tahmin response formatlama"""
        prediction = 0.2
        input_data = {'value': 20}
        
        result = format_response(prediction, input_data)
        
        assert result['prediction'] == prediction
        assert result['status'] == 'success'
    
    def test_format_response_high_prediction(self):
        """Yüksek tahmin response formatlama"""
        prediction = 0.9
        input_data = {'value': 90}
        
        result = format_response(prediction, input_data)
        
        assert result['prediction'] == prediction
        assert result['status'] == 'success'
    
    def test_format_response_contains_timestamp(self):
        """Response timestamp kontrolü"""
        prediction = 0.5
        input_data = {'value': 50}
        
        result = format_response(prediction, input_data)
        
        assert 'timestamp' in result
        assert result['timestamp'] is not None