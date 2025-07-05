create_rw_list_breweries = '''CREATE TABLE IF NOT EXISTS rw_list_breweries (
    id SERIAL PRIMARY KEY,
    data JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
'''

insert_rw_list_breweries = """
    INSERT INTO rw_list_breweries (data) 
    VALUES %s;
"""

create_tables = {
    'rw_list_breweries': create_rw_list_breweries
}

insert_queries = {
    'rw_list_breweries': insert_rw_list_breweries
}