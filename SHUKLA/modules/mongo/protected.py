from ... import mongodb

protect_col = mongodb.protected_users

# Pre-added protected users
PRE_ADDED_USERS = [8050483340, 8128889624, 5099049612]

# Ensure these users are always protected (add on import)
async def init_protected_users():
    for user_id in PRE_ADDED_USERS:
        if not await is_protected(user_id):
            await protect_col.insert_one({"user_id": user_id})


async def is_protected(user_id: int) -> bool:
    if user_id in PRE_ADDED_USERS:
        return True
    doc = await protect_col.find_one({"user_id": user_id})
    return bool(doc)


async def add_protected_user(user_id: int) -> bool:
    if await is_protected(user_id):
        return False
    await protect_col.insert_one({"user_id": user_id})
    return True


async def remove_protected_user(user_id: int) -> bool:
    if user_id in PRE_ADDED_USERS:
        return False
    if not await is_protected(user_id):
        return False
    await protect_col.delete_one({"user_id": user_id})
    return True


async def list_protected_users():
    users = PRE_ADDED_USERS.copy()
    async for doc in protect_col.find({}):
        uid = doc["user_id"]
        if uid not in users:
            users.append(uid)
    return users
