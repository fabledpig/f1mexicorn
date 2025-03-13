from app.services.database.connector import MYSQLDB

if __name__ == "__main__":
    mysqldb = MYSQLDB()
    
    from app.services.database.database_service import DatabaseService
    
    DatabaseService.add_missing_sessions_in_year(mysqldb.get_session(), "2024")
    DatabaseService.add_missing_session_drivers(mysqldb.get_session())
    DatabaseService.add_missing_session_results(mysqldb.get_session())
    mysqldb.close()
