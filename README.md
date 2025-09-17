# PortalNF Update API

API Python desenvolvida para fornecer informações de atualização para o Portal XML. Esta API centraliza as informações sobre versões, downloads e configurações do PortalNF, permitindo que o aplicativo cliente verifique e baixe atualizações automaticamente.

## 🎯 Objetivo

Esta API foi criada para ser o ponto central de informações de atualização do Portal XML. O aplicativo cliente pode consultar esta API para:

- Verificar se há uma nova versão disponível
- Obter informações sobre a versão atual
- Baixar o instalador mais recente
- Verificar se a atualização é obrigatória
- Validar a integridade do arquivo através do hash SHA256

## 🚀 Instalação

1. **Instale as dependências:**
```bash
pip install -r requirements.txt
```

2. **Configure as variáveis no arquivo `.env`:**
```env
# Configurações da API
API_KEY=sua_chave_secreta_aqui

# Configurações do PortalNF
PORTAL_VERSION=1.4.3
PORTAL_RELEASE_DATE=2025-09-17
PORTAL_CHANGELOG=Correções em NF-e Distribuição e melhorias de performance.
PORTAL_INSTALLER_URL=https://cdn.seudominio.com/PortalNF_1.4.3_Setup.exe
PORTAL_INSTALLER_TYPE=inno
PORTAL_SHA256=B1D6E0F2F5F0B8A7...F9C2
PORTAL_MANDATORY=false
PORTAL_MIN_SUPPORTED=1.2.0
```

## 🏃‍♂️ Execução

```bash
python main.py
```

A API estará disponível em `http://localhost:5000`

## 🌐 Deploy no Coolify

Esta API está configurada para deploy automático no Coolify:

1. **Faça push para o GitHub**
2. **Configure as variáveis de ambiente no Coolify** (mesmas do arquivo .env)
3. **O Coolify automaticamente detectará o Procfile e fará o deploy**

## 📡 Endpoints

### GET /api/portal-info
**Endpoint principal** - Retorna todas as informações de atualização do PortalNF.

**Headers obrigatórios:**
- `X-API-Key`: Chave de autenticação configurada no .env

**Resposta de sucesso (200):**
```json
{
  "version": "1.4.3",
  "releaseDate": "2025-09-17",
  "changelog": "Correções em NF-e Distribuição e melhorias de performance.",
  "installerUrl": "https://cdn.seudominio.com/PortalNF_1.4.3_Setup.exe",
  "installerType": "inno",
  "sha256": "B1D6E0F2F5F0B8A7...F9C2",
  "mandatory": false,
  "minSupported": "1.2.0"
}
```

**Campos da resposta:**
- `version`: Versão atual do PortalNF
- `releaseDate`: Data de lançamento (formato YYYY-MM-DD)
- `changelog`: Descrição das mudanças e correções
- `installerUrl`: URL direta para download do instalador
- `installerType`: Tipo do instalador (inno, msi, etc.)
- `sha256`: Hash SHA256 para validação de integridade
- `mandatory`: Se a atualização é obrigatória (true/false)
- `minSupported`: Versão mínima suportada

**Resposta de erro (401):**
```json
{
  "error": "Unauthorized",
  "message": "API key is required and must be valid"
}
```

### GET /health
**Health check** - Verifica se a API está funcionando (não requer autenticação).

**Resposta:**
```json
{
  "status": "healthy",
  "message": "API is running"
}
```

## 💻 Exemplos de Uso

### Com curl
```bash
# Obter informações de atualização
curl -H "X-API-Key: minha_chave_secreta_123" http://localhost:5000/api/portal-info

# Health check
curl http://localhost:5000/health
```

### Com PowerShell (Windows)
```powershell
# Obter informações de atualização
Invoke-RestMethod -Uri "http://localhost:5000/api/portal-info" -Headers @{"X-API-Key"="minha_chave_secreta_123"}

# Health check
Invoke-RestMethod -Uri "http://localhost:5000/health"
```

## 🔧 Configuração

Todas as configurações são feitas através do arquivo `.env` ou variáveis de ambiente no Coolify. Certifique-se de que todas as variáveis necessárias estão definidas antes de iniciar a API.

### Variáveis Obrigatórias:
- `API_KEY`: Chave de autenticação para acesso à API
- `PORTAL_VERSION`: Versão atual do PortalNF
- `PORTAL_RELEASE_DATE`: Data de lançamento
- `PORTAL_CHANGELOG`: Descrição das mudanças
- `PORTAL_INSTALLER_URL`: URL do instalador
- `PORTAL_INSTALLER_TYPE`: Tipo do instalador
- `PORTAL_SHA256`: Hash SHA256 do arquivo
- `PORTAL_MANDATORY`: Se é obrigatório (true/false)
- `PORTAL_MIN_SUPPORTED`: Versão mínima suportada

## 🔒 Segurança

- A API utiliza autenticação por chave através do header `X-API-Key`
- Todas as configurações sensíveis devem ser mantidas nas variáveis de ambiente
- Em produção, sempre use HTTPS
- Mantenha a chave da API segura e não a exponha em logs ou código

## 📝 Logs

A API registra:
- Tentativas de acesso com chaves inválidas
- Erros de configuração na inicialização
- Status de saúde da aplicação

## 🚀 Próximos Passos

Para integrar com o Portal XML:
1. Configure a URL da API nas configurações do Portal XML
2. Implemente a verificação periódica de atualizações
3. Configure o download automático quando `mandatory=true`
4. Implemente validação do hash SHA256 após download
