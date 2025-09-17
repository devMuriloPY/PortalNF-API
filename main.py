from flask import Flask, jsonify, request
from dotenv import load_dotenv
import os

# Carregar variáveis do arquivo .env
load_dotenv()

app = Flask(__name__)

def verify_api_key():
    """Verifica se a chave da API está correta"""
    api_key = request.headers.get('X-API-Key')
    expected_key = os.getenv('API_KEY')
    
    if not api_key or api_key != expected_key:
        return False
    return True

@app.route('/api/portal-info', methods=['GET'])
def get_portal_info():
    """Endpoint que retorna as informações do PortalNF"""
    
    # Verificar autenticação
    if not verify_api_key():
        return jsonify({
            'error': 'Unauthorized',
            'message': 'API key is required and must be valid'
        }), 401
    
    # Retornar JSON com dados do .env
    response = {
        "version": os.getenv('PORTAL_VERSION'),
        "releaseDate": os.getenv('PORTAL_RELEASE_DATE'),
        "changelog": os.getenv('PORTAL_CHANGELOG'),
        "installerUrl": os.getenv('PORTAL_INSTALLER_URL'),
        "installerType": os.getenv('PORTAL_INSTALLER_TYPE'),
        "sha256": os.getenv('PORTAL_SHA256'),
        "mandatory": os.getenv('PORTAL_MANDATORY', 'false').lower() == 'true',
        "minSupported": os.getenv('PORTAL_MIN_SUPPORTED')
    }
    
    return jsonify(response)

@app.route('/health', methods=['GET'])
def health_check():
    """Endpoint de health check"""
    return jsonify({
        'status': 'healthy',
        'message': 'API is running'
    })

@app.errorhandler(404)
def not_found(error):
    return jsonify({
        'error': 'Not Found',
        'message': 'Endpoint not found'
    }), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        'error': 'Internal Server Error',
        'message': 'Something went wrong'
    }), 500

if __name__ == '__main__':
    # Verificar se todas as variáveis necessárias estão definidas
    required_vars = [
        'API_KEY', 'PORTAL_VERSION', 'PORTAL_RELEASE_DATE', 
        'PORTAL_CHANGELOG', 'PORTAL_INSTALLER_URL', 
        'PORTAL_INSTALLER_TYPE', 'PORTAL_SHA256', 
        'PORTAL_MANDATORY', 'PORTAL_MIN_SUPPORTED'
    ]
    
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    
    if missing_vars:
        print(f"ERRO: As seguintes variáveis estão faltando no arquivo .env: {', '.join(missing_vars)}")
        exit(1)
    
    
    # Usar porta do ambiente ou padrão 5000
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)
