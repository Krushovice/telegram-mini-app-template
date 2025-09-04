import hmac, hashlib, urllib.parse
from typing import Optional


def validate_init_data(
    init_data_raw: str,
    bot_token: str,
) -> Optional[dict]:
    if not init_data_raw:
        return None
    pairs = urllib.parse.parse_qsl(
        init_data_raw,
        keep_blank_values=True,
    )
    data = dict(pairs)
    received_hash = data.pop("hash", None)
    if not received_hash:
        return None

    data_check_string = "\n".join(f"{k}={v}" for k, v in sorted(data.items()))
    secret_key = hashlib.sha256(bot_token.encode()).digest()
    computed = hmac.new(
        secret_key,
        data_check_string.encode(),
        hashlib.sha256,
    ).hexdigest()
    if not hmac.compare_digest(computed, received_hash):
        return None
    return data  # здесь user, query_id, auth_date и пр.
