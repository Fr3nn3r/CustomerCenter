from outreach.database import engine

def check_connection():
    try:
        with engine.connect() as conn:
            print('✅ Connection successful!')
    except Exception as e:
        print(f'❌ Connection failed: {e}')

if __name__ == '__main__':
    check_connection()
