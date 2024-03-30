import binascii
import hashlib
import hmac

SEED_MIN_ROLL = 1
SEED_MAX_ROLL = 1000000

def get_roll(secret_hash: str, round: int, client_seed: str) -> str:
  """
  secret_hash: hex-decimal string length with 128
  round: round in int
  """
  # 转型为字节
  secret = binascii.unhexlify(secret_hash)
  # 用户种子拼接轮数后转型为字节
  seed = (client_seed + "-" + str(round)).encode("utf8")
  # 生成Roll点哈希
  roll_hash =  hmac.new(secret, seed, hashlib.sha512).hexdigest()
  # 1000000 = 0xF4240
  # 截断，加速取余
  subHash = roll_hash[:7]
  # 转十六进制字符串为整数
  number = int(subHash, 16)
  # 取余
  return number % SEED_MAX_ROLL + SEED_MIN_ROLL

def get_public_hash(secret_hash: str, secret_salt: str) -> str:
  # 转型为字节
  secret = binascii.unhexlify(secret_hash)
  # 转型为字节
  salt = binascii.unhexlify(secret_salt)
  # 计算SHA256转十六进制字符串
  return hashlib.sha256(secret + salt).hexdigest()


if __name__ == "__main__":
  # 秘密哈希 十六进制，长度为偶数
  secret_hash = input("请输入秘密哈希 （十六进制，偶数长度）：")
  # 秘密盐   十六进制，长度为偶数
  secret_salt = input("请输入秘密盐 （十六进制，偶数长度）：")
  # 公开哈希 十六进制，长度为偶数
  public_hash = input("请输入公开哈希 （十六进制，偶数长度）：")
  # 用户种子 无要求
  client_seed = input("请输入用户种子：")
  # 回合 整数

  # 检查公开哈希
  # 公开哈希通过秘密哈希加盐取SHA256计算而来
  public_hash_check = get_public_hash(secret_hash, secret_salt)
  if public_hash == public_hash_check:
    print("公开哈希有效")
  else:
    print("公开哈希无效！")
    print(f"提供的公开哈希 {public_hash}")
    print(f"公开哈希应为 {public_hash_check}")
    
  while True:
    try: 
      round = int(input("请输入回合数："))
      # 获取Roll点
      # Roll点通过 秘密哈希+用户种子+轮数 
      # 取HMACSHA512再取余计算而来
      roll = get_roll(secret_hash, round, client_seed)
    
      print(f'回合数为 {round} 时的Roll点为 {roll}')

    except KeyboardInterrupt:
      print("\n程序结束。")
      break
      

