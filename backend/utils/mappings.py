# utils/mappings.py

ROLE_TABLES = {
    "user": ["nest_users", "tribe_users", "studio_users"],
    "seller": ["nest_sellers", "tribe_sellers", "studio_sellers"]
}

def get_table_by_role_and_group(role: str, group: str):
    role = role.lower()
    group = group.lower()
    
    if role not in ROLE_TABLES:
        raise ValueError("Invalid role")

    for table in ROLE_TABLES[role]:
        if group in table:
            return table

    raise ValueError("Invalid group for given role")
