import mysql.connector

db = mysql.connector.connect(host="localhost", user="root", password="Ads@234892", database="eduvault")
cur = db.cursor()

uid = None

def login():
    global uid
    # print("         Welcome         ")
    print("\n         project           \n")
    u_id = input("Enter your user id: ")
    p_word = input("Enter password: ")
    cur.execute("SELECT * FROM users WHERE id = %s AND pass = %s", (u_id, p_word))
    acc = cur.fetchone()

    if acc:
        print("Login successful")
        uid = str(acc[0])
        desgn = acc[2]
        if desgn == "stu":
            stu_menu()
        elif desgn == "fct":
            fct_menu()
    else:
        print("Login failed. Try again.")
        login()

def stu_menu():
    while True:
        print("\nStudent Menu:")
        print("1 - View Details")
        print("2 - View Attendance")
        print("3 - View Subjects")
        print("4 - Apply for Leave")
        print("5 - View Assignments")
        print("6 - View Date Sheet")
        print("7 - View UMC Status")
        print("0 - Log Out")

        choice = int(input("Enter your choice: "))
        if choice == 1:
            print("1 - Student details")
            print("2 - Parent Details")
            cho = int(input("Enter your Choice : "))
            if cho == 1:
                view_student_details(uid)
            elif cho == 2:
                show_prnt_dtl(uid)
            else:
                print("Invalid Choice")
        elif choice == 2:
            view_attendance(uid)
        elif choice == 3:
            view_subjects(uid)
        elif choice == 4:
            apply_leave(uid)
        elif choice == 5:
            view_assignments()
        elif choice == 6:
            view_date_sheet()
        elif choice == 7:
            view_umc_status(uid)
        elif choice == 0:
            print("Adios Amigo")
            print("Logging out...")
            break
        else:
            print("Invalid choice.")

def fct_menu():
    while True:
        print("\nFaculty Menu:")
        print("1 - View Student Details")
        print("2 - Upload Attendance")
        print("3 - Leave Application")
        print("4 - Upload Assignments")
        print("5 - Upload Date Sheet")
        print("6 - Update UMC Status")
        print("0 - Log Out")

        choice = int(input("Enter your choice: "))
        if choice == 1:
            print("1 - Student details")
            print("2 - Parent Details")
            cho = int(input("Enter your Choice : "))
            if cho == 1:
                stu_id = input("Enter student ID: ")
                view_student_details(stu_id)
            elif cho == 2:
                stu_id = input("Enter student ID: ")
                show_prnt_dtl(stu_id)
            else:
                print("Invalid Choice")
        elif choice == 2:
            upload_attendance()
        elif choice == 3:
            view_leave_applications()
            approve_leave()
        elif choice == 4:
            upload_assignment()
        elif choice == 5:
            upload_date_sheet()
        elif choice == 6:
            update_or_remove_umc_status()
        elif choice == 0:
            print("Adios Amigo")
            print("Logging out...")
            break
        else:
            print("Invalid choice.")

def view_student_details(uid):
    try:
        cur.execute(f"SELECT * FROM stu_details WHERE uid = {uid}")
        stu_dt = cur.fetchone()
        if stu_dt:
            print("\nStudent Details:")
            print(f"UID : {stu_dt[0]}")
            print(f"First Name : {stu_dt[1]}")
            print(f"Last name : {stu_dt[2]}")
            print(f"Section : {stu_dt[3]}")
            print(f"Gender : {stu_dt[4]}")
            print(f"Contact Number : {stu_dt[5]}")
            print(f"Email : {stu_dt[6]}")
            print(f"Address : {stu_dt[7]}")
            print(f"Branch : {stu_dt[8]}")
        else:
            print("Student details not found.")
    except mysql.connector.Error as err:
        print(f"Error fetching student details: {err}")


def show_prnt_dtl(uid):
    cur.execute(f"SELECT * FROM parent_dtl WHERE uid = {uid}")
    prnt_dt = cur.fetchone()
    print(f"UID : {prnt_dt[0]}")
    print(f"Father Name : {prnt_dt[1]}")
    print(f"Mother name : {prnt_dt[2]}")
    print(f"Father Contact : {prnt_dt[3]}")
    print(f"Mother Contact : {prnt_dt[4]}")
    print(f"Father Email : {prnt_dt[5]}")
    print(f"Mother Email : {prnt_dt[6]}")


def view_attendance(uid):
    try:
        # Fetch the branch of the student
        cur.execute("SELECT branch FROM stu_details WHERE uid = %s", (uid,))
        branch = cur.fetchone()[0]

        # Fetch subject names for the given branch from the branches table
        cur.execute("SELECT * FROM branches WHERE br_nm = %s", (branch,))
        branch_info = cur.fetchone()

        cur.execute(f"Select * from sub_att where uid ={uid}")
        att = cur.fetchone()

        if branch_info:
            print("Attendance Details:")
            for i in range(5):
                print(f"{branch_info[i + 1]} : {att[i + 1]}")

        else:
            print("No subjects found for this branch.")
    except mysql.connector.Error as err:
        print(f"Error fetching attendance: {err}")




def view_subjects(uid):
    try:
        # Fetch the branch of the student based on the uid
        cur.execute("SELECT branch FROM stu_details WHERE uid = %s", (uid,))
        branch = cur.fetchone()[0]

        # Display subjects based on the branch
        cur.execute(f"SELECT * FROM branches WHERE br_nm = '{branch}'")
        subjects = cur.fetchone()
        if subjects:
            print("Subjects:")
            print(subjects)
        else:
            print("No subjects found for this branch.")
    except mysql.connector.Error as err:
        print(f"Error fetching subjects: {err}")

def apply_leave(uid):
    try:
        reason = str(input("enter the reason : "))
        date = str(input("enter the date: (YYYY-MM-DD) "))
        cur.execute("INSERT INTO leav_app (uid, dat, reason, remark) VALUES (%s, %s, %s, 'pending')",
                    (uid, date, reason))
        db.commit()
        print("Leave application submitted successfully.")
    except mysql.connector.Error as err:
        print(f"Error submitting leave application: {err}")


def view_assignments():
    try:

        cur.execute("SELECT branch FROM stu_details WHERE uid = %s", (uid,))
        branch = cur.fetchone()[0]

        cur.execute("SELECT * FROM branches WHERE br_nm = %s", (branch,))
        b_info = cur.fetchone()

        cur.execute(f"SELECT * FROM assign WHERE br_nm = '{branch}'")
        assignments = cur.fetchone()
        if b_info:
            print(f"Assignments Details for \"{branch}\" branch")
            for i in range(5):
                print(f"{b_info[i+1]} : {assignments[i+1]}")
        else:
            print("No assignments found for this branch.")
    except mysql.connector.Error as err:
        print(f"Error fetching assignments: {err}")


def view_date_sheet():
    try:

        cur.execute(f"SELECT branch FROM stu_details WHERE uid = {uid}")
        branch = cur.fetchone()[0]

        cur.execute("SELECT * FROM branches WHERE br_nm = %s", (branch,))
        b_info = cur.fetchone()

        cur.execute(f"SELECT * FROM date_sht WHERE branch = '{branch}'")
        date_sheet = cur.fetchone()
        if date_sheet:
            print(f"Date Sheet: ({branch} Department)")
            for i in range(5):
                print(f"{b_info[i + 1]} : {date_sheet[i + 1]}")
        else:
            print("No date sheet available for this branch.")
    except mysql.connector.Error as err:
        print(f"Error fetching date sheet: {err}")


def view_umc_status(uid):
    try:
        cur.execute("SELECT * FROM umc_dtl WHERE uid = %s", (uid,))
        umc_status = cur.fetchone()
        if umc_status:
            print("UMC Status:")
            print(umc_status)
        else:
            print("UMC status not found.")
    except mysql.connector.Error as err:
        print(f"Error fetching UMC status: {err}")



# faculty functions

def upload_attendance():
    try:
        bran = input("Enter Branch: ")
        cur.execute(f"SELECT * FROM branches WHERE br_nm = '{bran}'")
        sub = cur.fetchone()

        uid_ = input("Enter UID of the Student : ")
        att = []
        for i in range(5):
            temp = input(f"enter attendance of {sub[i+1]} : ")
            att.append(temp)
        print(att)
        cur.execute(f"UPDATE sub_att SET sub1 = {att[0]},sub2 = {att[1]},sub3 = {att[2]}, sub4 = {att[3]}, sub5 = {att[4]} WHERE uid = {uid_};")
        db.commit()
        print("Attendance uploaded successfully.")
    except mysql.connector.Error as err:
        print(f"Error uploading attendance: {err}")


def view_leave_applications():
    try:
        cur.execute("SELECT * FROM leav_app")
        leave_applications = cur.fetchall()
        if leave_applications:
            print("Leave Applications:")
            for leave_app in leave_applications:
                print(leave_app)
        else:
            print("No leave applications found.")
    except mysql.connector.Error as err:
        print(f"Error fetching leave applications: {err}")

def approve_leave():
    try:
        uid_ = input("Enter UID : ")
        remark = input("Enter Remark : ")
        cur.execute("UPDATE leav_app SET remark = %s WHERE uid = %s",
                    (remark, uid_))
        db.commit()
        print("Leave approved successfully.")
    except mysql.connector.Error as err:
        print(f"Error approving leave: {err}")

def upload_assignment():
    try:
        bran = input("Enter Branch: ")
        cur.execute(f"SELECT * FROM branches WHERE br_nm = '{bran}'")
        sub = cur.fetchone()
        assignments = []
        for i in range(1, 6):
            sub_assignment = input(f"Enter assignment for {sub[i]}: ")
            assignments.append(sub_assignment)
        cur.execute("UPDATE assign SET sub1 = %s, sub2 = %s, sub3 = %s, sub4 = %s, sub5 = %s WHERE br_nm = %s",
                    (*assignments, bran))
        db.commit()
        print("Assignments updated successfully.")
    except mysql.connector.Error as err:
        print(f"Error updating assignments: {err}")


def update_or_remove_umc_status():
    action = input("Do you want to (U)pdate or (R)emove UMC status? (U/R): ").upper()
    uid = input("Enter UID: ")
    subject = input("Enter subject: ")

    if action == "U":
        try:
            cur.execute("INSERT INTO umc_dtl (uid, sub) VALUES (%s, %s)", (uid, subject))
            db.commit()
            print("UMC status updated successfully.")
        except mysql.connector.Error as err:
            print(f"Error updating UMC status: {err}")
    elif action == "R":
        try:
            cur.execute("DELETE FROM umc_dtl WHERE uid = %s AND sub = %s", (uid, subject))
            db.commit()
            print("UMC status removed successfully.")
        except mysql.connector.Error as err:
            print(f"Error removing UMC status: {err}")
    else:
        print("Invalid action. Please choose 'U' for update or 'R' for remove.")




def upload_date_sheet():
    try:
        branch = input("Enter branch : ")
        
        # Get subjects associated with the branch
        subjects = get_subjects(branch)
        if not subjects:
            print("No subjects found for this branch.")
            return

        # Initialize an empty list to store exam dates
        exam_dates = []

        # Prompt for exam dates for each subject
        for subject in subjects:
            exam_date = input(f"Enter the date for {subject}: ")
            exam_dates.append(exam_date)

        # Prepare the SQL statement with placeholders for each exam
        sql = "UPDATE date_sht SET exm1 = %s, exm2 = %s, exm3 = %s, exm4 = %s, exm5 = %s WHERE branch = %s"

        # Execute the SQL statement with the exam dates and the branch name
        cur.execute(sql, (*exam_dates, branch))
        db.commit()

        print("Date sheet uploaded successfully.")
    except mysql.connector.Error as err:
        print(f"Error uploading date sheet: {err}")





# def upload_date_sheet():
#     try:
#         branch = input("Enter branch : ")
        
#         # Get subjects associated with the branch
#         subjects = get_subjects(branch)
#         if not subjects:
#             print("No subjects found for this branch.")
#             return

#         # Initialize an empty list to store exam dates
#         exam_dates = []

#         # Prompt for exam dates for each subject
#         for subject in subjects:
#             exam_date = input(f"Enter the date for {subject}: ")
#             exam_dates.append(exam_date)

#         # Prepare the SQL statement with placeholders for each exam
#         cur.execute(f"INSERT INTO date_sht (branch, exm1, exm2, exm3, exm4, exm5) VALUES ({branch},{exam_dates[0]},{exam_dates[1]},{exam_dates[2]},{exam_dates[3]},{exam_dates[4]})")

#         # Execute the SQL statement with the branch name and exam dates
#         # cur.execute(sql, (branch, *exam_dates))
#         db.commit()

#         print("Date sheet uploaded successfully.")
#     except mysql.connector.Error as err:
#         print(f"Error uploading date sheet: {err}")


def get_subjects(branch):
    try:
        # Fetch subjects associated with the branch from the database
        cur.execute("SELECT sub1, sub2, sub3, sub4, sub5 FROM branches WHERE br_nm = %s", (branch,))
        subjects = cur.fetchone()
        if subjects:
            return subjects
        else:
            print("No subjects found for this branch.")
            return None
    except mysql.connector.Error as err:
        print(f"Error fetching subjects: {err}")
        return None

def up_dt_sh():
    branch = input("Enter branch : ")
    # Get subjects associated with the branch
    subjects = get_subjects(branch)
    if subjects:
        exams = []
        for i, subject in enumerate(subjects, start=1):  # Loop to collect details for each subject
            exam_date = input(f"Enter the date for {subject}: ")
            exams.append((subject, exam_date))

        # Call the upload_date_sheet function with branch and exam details
        upload_date_sheet(branch,)


if __name__ == "__main__":
    login()
