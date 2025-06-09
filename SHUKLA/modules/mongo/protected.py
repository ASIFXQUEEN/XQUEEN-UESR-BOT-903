# protected.py

async def get_protect_col():
    from SHUKLA.modules.mongo import mongodb  # delayed import to avoid circular import
    return mongodb.protected_users

PRE_ADDED_USERS = [8050483340, 8128889624, 5099049612]

async def is_protected(user_id: int) -> bool:
    if user_id in PRE_ADDED_USERS:
        return True
    protect_col = await get_protect_col()
    doc = await protect_col.find_one({"user_id": user_id})
    return bool(doc)

async def add_protected_user(user_id: int) -> bool:
    if await is_protected(user_id):
        return False
    protect_col = await get_protect_col()
    await protect_col.insert_one({"user_id": user_id})
    return True

async def remove_protected_user(user_id: int) -> bool:
    if user_id in PRE_ADDED_USERS:
        return False
    if not await is_protected(user_id):
        return False
    protect_col = await get_protect_col()
    await protect_col.delete_one({"user_id": user_id})
    return True

async def list_protected_users():
    users = PRE_ADDED_USERS.copy()
    protect_col = await get_protect_col()
    async for doc in protect_col.find({}):
        uid = doc["user_id"]
        if uid not in users:
            users.append(uid)
    return users
