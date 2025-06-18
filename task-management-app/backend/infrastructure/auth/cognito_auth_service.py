import os
import json
import base64
import urllib.request
from typing import Dict, Optional

import boto3
import jwt
from jwt.algorithms import RSAAlgorithm


class CognitoAuthService:
    """Cognitoを使用した認証サービス"""

    def __init__(self):
        self._region = os.environ.get('REGION_NAME', 'us-east-1')
        self._user_pool_id = os.environ.get('COGNITO_USER_POOL_ID')
        self._client_id = os.environ.get('COGNITO_CLIENT_ID')
        self._cognito_idp = boto3.client('cognito-idp')
        self._jwks = None

    def _get_jwks(self):
        """JWKSを取得する"""
        if self._jwks is None:
            keys_url = f'https://cognito-idp.{self._region}.amazonaws.com/{self._user_pool_id}/.well-known/jwks.json'
            with urllib.request.urlopen(keys_url) as f:
                response = f.read()
            self._jwks = json.loads(response.decode('utf-8'))['keys']
        return self._jwks

    def verify_token(self, token: str) -> Optional[Dict]:
        """JWTトークンを検証する"""
        # ヘッダーからキーIDを取得
        header = jwt.get_unverified_header(token)
        kid = header['kid']
        
        # JWKSから対応する公開鍵を見つける
        key = None
        for jwk in self._get_jwks():
            if jwk['kid'] == kid:
                key = jwk
                break
                
        if not key:
            return None
            
        # 公開鍵を作成
        public_key = RSAAlgorithm.from_jwk(json.dumps(key))
        
        try:
            # トークンを検証
            payload = jwt.decode(
                token,
                public_key,
                algorithms=['RS256'],
                audience=self._client_id,
                options={'verify_exp': True}
            )
            return payload
        except Exception as e:
            print(f"Token verification failed: {str(e)}")
            return None

    def get_user_id_from_token(self, token: str) -> Optional[str]:
        """トークンからユーザーIDを取得する"""
        payload = self.verify_token(token)
        if not payload:
            return None
        
        # CognitoのJWTからsubクレームを取得（ユーザーID）
        return payload.get('sub')
