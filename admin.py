import mysql.connector
import streamlit as st
import pandas as pd
from streamlit_extras.switch_page_button import switch_page
import subprocess
import manager
from st_pages import Page, show_pages, hide_pages

# Establishing a connection
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="mysqlpswrd4321",
    database="mini_project"
)

show_pages([
    Page("main.py", "Main"),
    Page("manager.py", "Manager"),
    Page("admin.py", "Admin")
])

hide_pages([

    'Manager',
    'Admin'
])
mycursor = db.cursor()
print("Connection Established")


def main():
    # Search by SRN
    search_srn = st.text_input("Search by SRN:")
    if search_srn:
        # Query to get details based on SRN
        query_details = f"""
        SELECT
            S.SRN AS Student_SRN,
            S.Name AS Student_Name,
            S.Email AS Student_Email,
            M.manager_ID,
            M.manager_name,
            M.manager_email,
            MR.Rating AS Manager_Rating,
            MR.Feedback AS Manager_Feedback,
            I.start_date AS Internship_Start_Date,
            I.end_date AS Internship_End_Date,
            I.Title AS Internship_Title,
            I.Type AS Internship_Type,
            C.company_name,
            C.website_link
        FROM
            Student S
        JOIN
            manager_srn_map MMap ON S.SRN = MMap.SRN
        JOIN
            Manager M ON MMap.manager_ID = M.manager_ID
        JOIN
            Internship I ON S.SRN = I.SRN
        JOIN
            Company C ON I.company_name = C.company_name
        LEFT JOIN
            Manager_Review MR ON M.manager_ID = MR.manager_ID
        WHERE
            S.SRN = '{search_srn}'; 
        """

        # Execute the query
        mycursor.execute(query_details)
        result = mycursor.fetchall()

        if result:
            st.title("Student and Manager Information:")
            st.write(f"SRN: {result[0][0]}")
            st.write(f"Student Name: {result[0][1]}")
            st.write(f"Student Email: {result[0][2]}")
            st.write(f"Manager ID: {result[0][3]}")
            st.write(f"Manager Name: {result[0][4]}")
            st.write(f"Manager Email: {result[0][5]}")
            st.write(f"Manager Rating: {result[0][6]}")
            st.write(f"Manager Feedback: {result[0][7]}")
            st.write(f"Internship Start Date: {result[0][8]}")
            st.write(f"Internship End Date: {result[0][9]}")
            st.write(f"Internship Title: {result[0][10]}")
            st.write(f"Internship Type: {result[0][11]}")
            st.write(f"Company Name: {result[0][12]}")
            st.write(f"Company website link: {result[0][13]}")
            
            # Approval/Disapproval functionality
            action = st.radio("Action", ["Approve", "Disapprove"])

            if st.button("Submit"):
                SRN = str(result[0][0])  # Convert to standard Python integer
                if action == "Approve":
                    # Update application status to 'completed'
                    mycursor.execute("UPDATE Application SET application_status = 'completed' WHERE SRN = %s", (SRN,))
                    db.commit()
                    st.success(f"Application for SRN {SRN} Approved!")

                    # Add a back button to redirect to the admin page
                   
                elif action == "Disapprove":
                    # Update application status to 'not completed'
                    mycursor.execute("UPDATE Application SET application_status = 'not completed' WHERE SRN = %s", (SRN,))
                    db.commit()
                    st.warning(f"Application for SRN {SRN} Disapproved!")

        else:
            st.warning("No data available for the provided SRN.")
    else:
        # Radio buttons to switch between views
        view_option = st.radio("Select View Option", ["All Entries", "Pending Manager Review Status", "Pending Application Status"])

        # View for all entries with pending manager review status
        query_pending_manager_review = """
        SELECT 
            Application_ID,
            SRN AS Student_SRN
        FROM 
            Application
        WHERE
            manager_review_status = 'pending'
        """

        # View for all entries with pending application status
        query_pending_application = """
        SELECT 
            Application_ID,
            SRN AS Student_SRN
        FROM 
            Application
        WHERE
            application_status = 'pending'
        """

        # Default view (no radio button selected)
        query_default = """
        SELECT 
            Application_ID,
            SRN AS Student_SRN
        FROM 
            Application    
        """

        # Execute the query based on radio button selection
        if view_option == "Pending Manager Review Status":
            mycursor.execute(query_pending_manager_review)
            results = mycursor.fetchall()
            if not results:
                st.warning("No data available for pending manager review status.")
            else:
                st.title("Pending Manager Review Status:")
        elif view_option == "Pending Application Status":
            mycursor.execute(query_pending_application)
            results = mycursor.fetchall()
            if not results:
                st.warning("No data available for pending application status.")
            else:
                st.title("Pending Application Status:")
        else:
            # Default view (All Entries)
            st.title("Student Records")
            mycursor.execute(query_default)
            results = mycursor.fetchall()

        # Convert results to DataFrame
        df = pd.DataFrame(results, columns=["Application_ID", "Student_SRN"])

        # Display the DataFrame in Streamlit
        if not df.empty:
            st.dataframe(df)

if __name__ == "__main__":
    main()
