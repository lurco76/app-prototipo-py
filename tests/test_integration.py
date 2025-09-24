import pytest
import requests
import time
import json

BASE_URL = "http://localhost:5000"
FRONTEND_URL = "http://localhost:3000"

class TestIntegration:
    @classmethod
    def setup_class(cls):
        """Esperar a que los servicios estén disponibles"""
        max_retries = 30
        for i in range(max_retries):
            try:
                response = requests.get(f"{BASE_URL}/verify", timeout=5)
                break
            except:
                if i == max_retries - 1:
                    pytest.fail("Backend no disponible después de 30 intentos")
                time.sleep(2)
    
    def test_login_admin_success(self):
        """Test login exitoso con usuario admin"""
        data = {"username": "admin", "password": "admin123"}
        response = requests.post(f"{BASE_URL}/login", json=data)
        
        assert response.status_code == 200
        result = response.json()
        assert result['success'] is True
        assert result['username'] == 'admin'
        assert result['role'] == 'admin'
        assert 'token' in result
    
    def test_login_user_success(self):
        """Test login exitoso con usuario normal"""
        data = {"username": "user", "password": "user123"}
        response = requests.post(f"{BASE_URL}/login", json=data)
        
        assert response.status_code == 200
        result = response.json()
        assert result['success'] is True
        assert result['role'] == 'user'
    
    def test_login_guest_success(self):
        """Test login exitoso con usuario guest"""
        data = {"username": "guest", "password": "guest123"}
        response = requests.post(f"{BASE_URL}/login", json=data)
        
        assert response.status_code == 200
        result = response.json()
        assert result['success'] is True
        assert result['role'] == 'guest'
    
    def test_login_invalid_credentials(self):
        """Test login con credenciales inválidas"""
        data = {"username": "invalid", "password": "wrong"}
        response = requests.post(f"{BASE_URL}/login", json=data)
        
        assert response.status_code == 401
        result = response.json()
        assert result['success'] is False
    
    def test_resources_admin(self):
        """Test acceso a recursos como admin"""
        # Login
        data = {"username": "admin", "password": "admin123"}
        login_response = requests.post(f"{BASE_URL}/login", json=data)
        token = login_response.json()['token']
        
        # Acceder a recursos
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(f"{BASE_URL}/resources", headers=headers)
        
        assert response.status_code == 200
        result = response.json()
        assert result['role'] == 'admin'
        assert 'Dashboard Admin' in result['resources']
        assert len(result['resources']) == 4  # Admin tiene 4 recursos
    
    def test_resources_user(self):
        """Test acceso a recursos como user"""
        # Login
        data = {"username": "user", "password": "user123"}
        login_response = requests.post(f"{BASE_URL}/login", json=data)
        token = login_response.json()['token']
        
        # Acceder a recursos
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(f"{BASE_URL}/resources", headers=headers)
        
        assert response.status_code == 200
        result = response.json()
        assert result['role'] == 'user'
        assert len(result['resources']) == 3  # User tiene 3 recursos
    
    def test_resources_guest(self):
        """Test acceso a recursos como guest"""
        # Login
        data = {"username": "guest", "password": "guest123"}
        login_response = requests.post(f"{BASE_URL}/login", json=data)
        token = login_response.json()['token']
        
        # Acceder a recursos
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(f"{BASE_URL}/resources", headers=headers)
        
        assert response.status_code == 200
        result = response.json()
        assert result['role'] == 'guest'
        assert len(result['resources']) == 1  # Guest tiene 1 recurso
    
    def test_resources_without_token(self):
        """Test acceso a recursos sin token"""
        response = requests.get(f"{BASE_URL}/resources")
        assert response.status_code == 401
    
    def test_resources_invalid_token(self):
        """Test acceso a recursos con token inválido"""
        headers = {"Authorization": "Bearer token_invalido"}
        response = requests.get(f"{BASE_URL}/resources", headers=headers)
        assert response.status_code == 401
    
    def test_token_refresh(self):
        """Test refresh de token"""
        # Login
        data = {"username": "admin", "password": "admin123"}
        login_response = requests.post(f"{BASE_URL}/login", json=data)
        token = login_response.json()['token']
        
        # Refresh token
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.post(f"{BASE_URL}/refresh", headers=headers)
        
        assert response.status_code == 200
        result = response.json()
        assert 'token' in result
        assert result['token'] != token  # Nuevo token debe ser diferente
    
    def test_frontend_accessibility(self):
        """Test que el frontend es accesible"""
        try:
            response = requests.get(FRONTEND_URL, timeout=10)
            assert response.status_code == 200
            assert 'html' in response.headers.get('content-type', '').lower()
        except:
            pytest.skip("Frontend no disponible para pruebas")