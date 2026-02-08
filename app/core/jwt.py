import jwt
import uuid
import time
from typing import List, Tuple, Optional
from app.core.config import settings

class JWTClaims:
    """
    在实际应用中，你可以将其定义为 Pydantic 模型或简单的数据类。
    """
    def __init__(self, payload: dict):
        self.user_id = payload.get("user_id")
        self.external_uid = payload.get("external_uid")
        self.username = payload.get("username")
        self.email = payload.get("email")
        self.scope = payload.get("scope", [])
        # 其他字段如 exp, iat, iss 等通常由 PyJWT 自动处理验证

def generate_jwt_token(
    user_id: uuid.UUID, 
    external_uid: int, 
    user_role: str, 
    username: str, 
    email: str, 
    secret_key: str, 
    duration_seconds: int
) -> str:
    """
    生成 JWT 令牌
    
    Args:
        user_id: 用户 UUID
        external_uid: 外部用户 ID
        user_role: 用户角色
        username: 用户名
        email: 邮箱
        secret_key: 密钥
        duration_seconds: 有效期（秒）
    
    Returns:
        生成的 JWT Token 字符串
    """
    
    # 计算过期时间 (当前时间 + 持续时间)
    expire_time = int(time.time()) + duration_seconds
    
    # 构建 Claims (载荷)
    payload = {
        # 自定义声明
        "user_id": str(user_id),          # UUID 需要转为字符串
        "external_uid": external_uid,
        "username": username,
        "email": email,
        "scope": [user_role],             # 角色放入数组中
        
        # 标准注册声明 (Registered Claims)
        "exp": expire_time,               # 过期时间
        "iat": int(time.time()),          # 签发时间
        "nbf": int(time.time()),          # 生效时间
        "iss": "dm-companions",           # 签发者
        "sub": str(user_id)               # 主题 (通常也是用户ID)
    }

    # 生成 Token (使用 HS256 算法)
    token = jwt.encode(payload, secret_key, algorithm="HS256")
    
    return token


def verify_jwt_token(token_string: str, secret_key: str) -> Tuple[Optional[JWTClaims], Optional[str]]:
    """
    验证 JWT 令牌并解析声明
    
    Args:
        token_string: JWT Token 字符串
        secret_key: 用于验证签名的密钥
    
    Returns:
        Tuple: (Claims对象, 错误信息)。如果验证成功，错误信息为 None。
    """
    try:
        # 1. 解码 Token
        # verify=True 会自动验证 exp, iat 等标准时间声明
        payload = jwt.decode(token_string, secret_key, algorithms=["HS256"])
        
        # 2. 检查签名算法 (模拟 Go 中的 SigningMethodHMAC 检查)
        # PyJWT 在 decode 时已经根据 algorithms 参数做了检查，这里为了逻辑完整再确认一次
        # 获取未验证的头信息来检查算法
        header = jwt.get_unverified_header(token_string)
        if header['alg'] != 'HS256':
            return None, f"意外的签名方法: {header['alg']}"

        # 3. 将载荷转换为 Claims 对象
        claims = JWTClaims(payload)
        
        return claims, None

    except jwt.ExpiredSignatureError:
        return None, "Token 已过期"
    except jwt.InvalidTokenError as e:
        return None, f"无效的 Token: {str(e)}"
    except Exception as e:
        return None, f"验证过程中发生错误: {str(e)}"
    
# --- 使用示例 ---
if __name__ == "__main__":
    # 模拟参数
    test_uuid = uuid.uuid4()
    secret = settings.AUTH_SECRETE_KEY
    
    duration = 3600  # 1小时
    
    token = generate_jwt_token(
        user_id=test_uuid,
        external_uid=12345,
        user_role="admin",
        username="john_doe",
        email="john@example.com",
        secret_key=secret,
        duration_seconds=duration
    )
    
    
    claims, error = verify_jwt_token(token, secret)
    
    if error is None:
        print("验证成功！")
        print(f"用户ID: {claims.user_id}")
        print(f"用户名: {claims.username}")
    else:
        print(f"验证失败: {error}")
    print("Generated Token:")
    print(token)