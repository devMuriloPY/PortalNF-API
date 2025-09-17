from flask import Flask, jsonify, request
from dotenv import load_dotenv
import os

# Carregar variáveis do arquivo .env
load_dotenv()

app = Flask(__name__)

def is_abs_url(u: str) -> bool:
    if not u:
        return False
    u = u.strip().lower()
    return u.startswith("http://") or u.startswith("https://")

def join_url(base: str, path: str) -> str:
    base = (base or "").rstrip("/")
    path = (path or "").lstrip("/")
    if not base:
        return "/" + path  # fallback relativo (último caso)
    return f"{base}/{path}"
def guess_base_url() -> str:
    """
    Tenta deduzir a base pública pela requisição (útil atrás de proxy).
    Respeita X-Forwarded-Proto/Host se presentes (Coolify/Nginx).
    """
    proto = (request.headers.get("X-Forwarded-Proto") or request.scheme or "http").split(",")[0].strip()
    host  = (request.headers.get("X-Forwarded-Host")  or request.host).split(",")[0].strip()
    return f"{proto}://{host}"

def build_installer_url() -> str:
    """
    Regras:
    1) Se PORTAL_INSTALLER_URL for absoluta, usa ela.
    2) Senão, monta SERVER_BASE_URL + PORTAL_INSTALLER_PATH.
       - Se SERVER_BASE_URL vazio, tenta deduzir do request.
    """
    absolute = (os.getenv("PORTAL_INSTALLER_URL") or "").strip()
    if is_abs_url(absolute):
        return absolute

    base = (os.getenv("SERVER_BASE_URL") or "").strip()
    path = (os.getenv("PORTAL_INSTALLER_PATH") or "").strip()

    if not path:
        return ""  # sem caminho, não dá pra montar

    if not base:
        base = guess_base_url()

    return join_url(base, path)

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

    if not verify_api_key():
        return jsonify({
            'error': 'Unauthorized',
            'message': 'API key is required and must be valid'
        }), 401

    installer_url = build_installer_url()

    response = {
        "version":      os.getenv('PORTAL_VERSION'),
        "releaseDate":  os.getenv('PORTAL_RELEASE_DATE'),
        "changelog":    os.getenv('PORTAL_CHANGELOG'),
        "installerUrl": installer_url,
        "installerType": (os.getenv('PORTAL_INSTALLER_TYPE') or 'inno').strip().lower(),
        "sha256":       (os.getenv('PORTAL_SHA256') or '').strip().upper(),
        "mandatory":    (os.getenv('PORTAL_MANDATORY', 'false').lower() == 'true'),
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
    # Variáveis sempre necessárias
    required_always = [
        'API_KEY', 'PORTAL_VERSION', 'PORTAL_RELEASE_DATE',
        'PORTAL_CHANGELOG', 'PORTAL_INSTALLER_TYPE',
        'PORTAL_SHA256', 'PORTAL_MANDATORY', 'PORTAL_MIN_SUPPORTED'
    ]

    missing = [v for v in required_always if not os.getenv(v)]

    # Forma A: URL absoluta
    installer_url_env = os.getenv('PORTAL_INSTALLER_URL')
    # Forma B: base + path
    server_base = os.getenv('SERVER_BASE_URL')
    installer_path = os.getenv('PORTAL_INSTALLER_PATH')

    has_absolute = bool(installer_url_env and is_abs_url(installer_url_env))
    has_basepath = bool(installer_path)  # base pode ser deduzida do request

    if not (has_absolute or has_basepath):
        # Falta pelo menos uma das formas
        missing.append('PORTAL_INSTALLER_URL (absoluta) ou PORTAL_INSTALLER_PATH')

    if missing:
        print("ERRO: Faltam variáveis no .env:")
        for m in missing:
            print(f"  - {m}")
        exit(1)

    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)
