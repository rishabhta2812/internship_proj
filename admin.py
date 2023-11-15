import mysql.connector
import streamlit as st
import pandas as pd

# Establishing a connection
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="mysqlpswrd4321",
    database="mini_project"
)

mycursor = db.cursor()
print("Connection Established")

def main():
    # Checkbox to switch between views
    show_pending_manager_review = st.checkbox("Show Pending Manager Review Status")
    show_pending_application = st.checkbox("Show Pending Application Status")

    # View for all entries with pending manager review status
    query_pending_manager_review = """
    SELECT 
        S.Name AS Student_Name, 
        S.SRN AS Student_SRN, 
        M.manager_ID, 
        M.manager_name, 
        M.manager_email
    FROM 
        Student S
    INNER JOIN 
        manager_srn_map MMap ON S.SRN = MMap.SRN
    INNER JOIN 
        Manager M ON MMap.manager_ID = M.manager_ID
    INNER JOIN
        Application A ON S.SRN = A.SRN
    WHERE
        A.manager_review_status = 'pending'
    """

    # View for all entries with pending application status
    query_pending_application = """
    SELECT 
        S.Name AS Student_Name, 
        S.SRN AS Student_SRN, 
        M.manager_ID, 
        M.manager_name, 
        M.manager_email
    FROM 
        Student S
    INNER JOIN 
        manager_srn_map MMap ON S.SRN = MMap.SRN
    INNER JOIN 
        Manager M ON MMap.manager_ID = M.manager_ID
    INNER JOIN
        Application A ON S.SRN = A.SRN
    WHERE
        A.application_status = 'pending'
    """

    # Default view (no checkbox selected)
    query_default = """
    SELECT 
        S.Name AS Student_Name, 
        S.SRN AS Student_SRN, 
        M.manager_ID, 
        M.manager_name, 
        M.manager_email
    FROM 
        Student S
    INNER JOIN 
        manager_srn_map MMap ON S.SRN = MMap.SRN
    INNER JOIN 
        Manager M ON MMap.manager_ID = M.manager_ID
    """

    # Execute the queries based on checkbox state
    if show_pending_manager_review:
        mycursor.execute(query_pending_manager_review)
        results = mycursor.fetchall()
        st.title("Pending Manager Review Status:")
    elif show_pending_application:
        mycursor.execute(query_pending_application)
        results = mycursor.fetchall()
        st.title("Pending Application Status:")
    else:
        # Default view (no checkbox selected)
        st.title("Student and Manager Information")
        mycursor.execute(query_default)
        results = mycursor.fetchall()

    # Convert results to DataFrame
    df = pd.DataFrame(results, columns=mycursor.column_names)

    # Display the DataFrame in Streamlit
    st.dataframe(df)

if __name__ == "__main__":
    main()
