import pytest
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'backend'))

from app import hash_password, generate_token, verify_token

class TestAuth:
    def test_hash_password(self):
        """Test que la función de hash funciona correctamente"""
        password = "test123"
        hashed = hash_password(password)
        assert hashed is not None
        assert len(hashed) == 64  # SHA256 produce 64 caracteres hex
        assert hashed != password
    
    def test_generate_token(self):
        """Test que se genera un token JWT válido"""
        username = "testuser"
        role = "user"
        token = generate_token(username, role)
        assert token is not None
        assert isinstance(token, str)
        assert len(token) > 0
    
    def test_verify_token_valid(self):
        """Test que se verifica correctamente un token válido"""
        username = "testuser"
        role = "admin"
        token = generate_token(username, role)
        payload = verify_token(token)
        
        assert payload is not None
        assert payload['username'] == username
        assert payload['role'] == role
    
    def test_verify_token_invalid(self):
        """Test que se rechaza un token inválido"""
        invalid_token = "token_invalido"
        payload = verify_token(invalid_token)
        assert payload is None
    
    def test_password_consistency(self):
        """Test que el mismo password siempre produce el mismo hash"""
        password = "consistent_test"
        hash1 = hash_password(password)
        hash2 = hash_password(password)
        assert hash1 == hash2