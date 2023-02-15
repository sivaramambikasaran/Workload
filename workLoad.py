import pandas as pd
import pdfkit

UG_COURSE_LIMIT = 3
# 4 semesters  constitute a cycle
COURSE_PER_CYCLE = 6
NUM_PREFERENCES = 3
NUM_TIE_RULES = 3
YEAR_ = 2023
SEM_ = 'ODD'


class faculty:
    """Class for professor data, this holds the information needed for calculating the workload.
    Also this stores the provisional allotment
    """

    def __init__(self, data):
        # Information of a professor
        self.name = data[0]
        self.smail = data[1]
        self.ug_course_count_left = UG_COURSE_LIMIT
        self.pg_course_count_left = COURSE_PER_CYCLE
        # This will hold the courses alloted  (filled either through provisional allotment)
        self.current_allotment = []
        self.ug_sem = 1
        self.pg_sem = 1
        self.course_count = 0
        self.priority_key = 100

    def add_preferences(self, data):
        self.course_preferences = data  # this is just the current cycle
        pass

    def set_priority(self, id):
        self.priority_key = id

    def work_load_history(self, ug_count, pg_count):
        # data[3] - UG courses taught in previous cycle data data[4] PG courses taught in a cycle
        self.ug_course_count_left = UG_COURSE_LIMIT - ug_count
        self.pg_course_count_left = COURSE_PER_CYCLE - (pg_count + ug_count)
        self.course_count = pg_count + ug_count
        # This will have courses of 4 semesters initially, post allotment this increases on provisional allotment

    def can_accommodate_ug(self):
        if self.course_count < COURSE_PER_CYCLE and self.ug_course_count_left > 0 and self.ug_sem == 1:
            return True
        return False

    def can_accommodate_pg(self):
        if self.course_count == COURSE_PER_CYCLE and self.pg_sem == 1:
            return False
        return True

    def hist_ug(self):
        #       self.ug_course_count_left = UG_COURSE_LIMIT - ug_count
        #       self.pg_course_count_left = COURSE_PER_CYCLE - (pg_count + ug_count)
        #       self.course_count = pg_count + ug_count
        self.ug_course_count_left -= 1
        self.pg_course_count_left -= 1
        self.course_count += 1

    def hist_pg(self):
        #       self.ug_course_count_left = UG_COURSE_LIMIT - ug_count
        #       self.pg_course_count_left = COURSE_PER_CYCLE - (pg_count + ug_count)
        #       self.course_count = pg_count + ug_count
        self.pg_course_count_left -= 1
        self.course_count += 1

    def allot_course_ug(self, course_):
        self.current_allotment.append(course_)
        self.ug_sem = 0

    def allot_course_pg(self, course_):
        self.current_allotment.append(course_)
        self.pg_sem = 0

    def print_faculty_details(self):
        print(self.name)


class course:
    """Class for course data, this holds the information needed for calculating the workload.
    Also this stores the provisional allotment
    """

    def __init__(self, code, name):
        self.course_code = code
        self.course_name = name
        self.preference = []
        # any number of preference can be added It is stored as array of arrays
        for i in range(NUM_PREFERENCES):
            # this stores a list of list with each list having a faculty
            self.preference.append([])
        self.faculty_list = []
        self.is_ug_course = True
        self.course_history = {}

    def add_requirement(self, x):
        self.course_faculty_required = x

    def assign_faculty(self, faculty):
        self.course_faculty_required -= 1
        self.faculty_list.append(faculty)

    def set_as_pg(self):
        self.is_ug_course = False

    def isUG_course(self):
        return self.is_ug_course

    def print_course(self):
        print(self.course_code + " : " + self.course_name + "_" +
              str(self.is_ug_course) + "_" + str(self.course_faculty_required))
        resultList = list(self.course_history.items())
        # printing the resultant list of a dictionary
        print(resultList)

    def get_requirement(self):
        return self.course_faculty_required

    def tie_rule_1(self, fac1, fac2):
        # Number of UG courses left in cycle (NOTICE the reverse order)
        if fac1.ug_course_count_left < fac2.ug_course_count_left:
            return fac2, fac1
        if fac1.ug_course_count_left > fac2.ug_course_count_left:
            return fac1, fac2
        return None

    def tie_rule_2(self, fac1, fac2):
        a = 0
        b = 0
        if self.course_history.get(fac1.smail) != None:
            a = self.course_history[fac1.smail]
        if self.course_history.get(fac2.smail) != None:
            b = self.course_history[fac2.smail]
        # Number of times the same course is taught in previous cycle (NOTICE the reverse order)
        if a < b:
            return fac1, fac2
        if a > b:
            return fac2, fac1
        return None

# Adding more ties can be done but the final TIE rule must return a single value
    def tie_rule_3(self, fac1, fac2):
        # Priority key stores an unique rank based on the time the data was submitted (This breaks all ties)
        if fac1.priority_key > fac2.priority_key:
            return fac2, fac1
        return fac1, fac2
    # The below tie is used along with bubble sort to sort and allot
    # Add ties as and when needed

    def tie_settle_ug(self, fac1, fac2):
        if self.tie_rule_1(fac1, fac2) != None:
            return self.tie_rule_1(fac1, fac2)
        if self.tie_rule_2(fac1, fac2) != None:
            return self.tie_rule_2(fac1, fac2)
        return self.tie_rule_3(fac1, fac2)
        # if fac1.tie_rule_X(fac2) != None:
        #  return fac1.tie_rule_x(fac2)   ====> can be added at the bottom to add more Ties (for an xth tie)

    # for PG only two ties are needed
    def tie_settle_pg(self, fac1, fac2):
        if self.tie_rule_2(fac1, fac2) != None:
            return self.tie_rule_2(fac1, fac2)
        return self.tie_rule_3(fac1, fac2)
        # if fac1.tie_rule_X(fac2) != None:
        #  return fac1.tie_rule_x(fac2)   ====> can be added at the bottom to add more Ties (for an xth tie)


# Course list is stored as a database


# Compute faculty requirement csv

# Routine to have the courses as dictionary or keep it in the list
# Create Course objects

        # print(course_list_master_data[course_list_[0]].course_name)
       # course_list_master_data[str(course_list_[i])].print_course()
# Compute workload history using different csv
# use a loop to compute number of courses in ug and pg


# def update_course_history():
#     # workload_hist = pd.read_csv('work_load_ODD_2022.csv')
#     # After each year, the courses are allotted, a function is written to store that in a
#     # csv file named as : work_load_ODD/EVEN_YYYY.csv
#     # As of now, just a single year data is considered
#     # Keep the vectors ug_count_ and pg_count_ equivalent to faculty_on_roll
#     # For each course add course_history{} dict
#     # iterate through each sheet and add to each course who taught if key is there then add value if not add key and 1
#     workload_history_file = ['./data/work_load_ODD_21.csv',
#                              './data/work_load_EVEN_21.csv', './data/work_load_ODD_22.csv', './data/work_load_EVEN_22.csv']
#     for i_ in range(0, len(workload_history_file)):
#         workload_hist = pd.read_csv(workload_history_file[i_])
#         # faculty_list_master_data[].hist_ug
#         for i in range(0, len(workload_hist.index)):
#             course_fac_list = list(workload_hist.iloc[i])
#             course_code_ = course_fac_list[0]
#             course_fac_list.remove(course_code_)
#             course_fac_list = [x for x in course_fac_list if x == x]
#             for cfl in course_fac_list:
#                 # this is to update faculty object
#                 if course_list_master_data[course_code_].isUG_course():
#                     faculty_list_master_data[cfl].hist_ug()
#                 else:
#                     faculty_list_master_data[cfl].hist_pg()
#                 # this is done to update the course objects
#                 if course_list_master_data[course_code_].course_history.get(cfl) == None:
#                     tmp = 1
#                     course_list_master_data[course_code_].course_history.update({
#                                                                                 cfl: tmp})
#                 else:
#                     tmp = course_list_master_data[course_code_].course_history[cfl] + 1
#                     course_list_master_data[course_code_].course_history.update({
#                                                                                 cfl: tmp})


# STEP 1 : Produce a provisional allotment for UG courses


# Step 2 : Intervention of in charge (Manual checkup) -- Need to upload modifications
# Additional check on additions or deletions
def finalize_allotment_ug():
    pass

# Step 3 : Provisional allotment for PG courses
# Allotment algorithm


# def compute_provisional_allotment_pg():
#     # Allotment does in Number of preferences
#     for i in range(0, NUM_PREFERENCES):
#        # Does for each current courses
#         for j in range(0, len(current_course_pg)):
#             # order the faculty
#             if current_course_pg[j].get_requirement() > 0:
#                 course_tmp_pref = [
#                     x for x in current_course_pg[j].preference[i] if x.can_accommodate_pg()]
#                 n = len(course_tmp_pref)
#                 for i_ in range(n):
#                     for j_ in range(0, n-i-1):
#                         course_tmp_pref[j_], course_tmp_pref[j_ + 1] = course_tmp_pref[j_].tie_settle_pg(
#                             course_tmp_pref[j_], course_tmp_pref[j_+1], current_course_pg[j])
#                 # Once the faculty is sorted out they are assigned to the course
#                 for ctp in course_tmp_pref:
#                     if current_course_pg[j].get_requirement() > 0:
#                         current_course_pg[j].assign_faculty(ctp)


# Step 4 : Intervention of in charge (Manual Checkup)
# Additional check on additions or deletions

def finalize_allotment_pg():
    pass

# Step 5 : Course work load generated as csv  -- Need to upload modifications
# TODO : provide in PDF file


class allotment:
    def __init__(self) -> None:
        self.faculty_list_master_data = {}
        self.course_list_master_data = {}
        # After provisional UG allotment the app shows the remaining faculty (checkpoint for In charge)
        self.faculty_on_roll = set()

        # Database of courses offered in the department
        # The course code, name offered in a cycle and distinction as UG and PG course
        self.current_course_ug = set()
        self.current_course_pg = set()

    def show_course_fac_preference_table(self):
        # As of now, the preference for each course printed in the order of filling the preference form
        print(f"Faculty count ", len(self.current_course_ug))
        output_sheet = []
        for course_ in self.current_course_ug:
            for i in range(0, NUM_PREFERENCES):
                tmp = []
                tmp.append(course_.course_code)
                tmp.append("Option " + str(i+1))
                for x in course_.preference[i]:
                    tmp.append(x)
                output_sheet.append(tmp)
        # df = pd.DataFrame(output_sheet)
        return output_sheet

    def generate_allotment(self):
        output_sheet = []
        for course_ in self.current_course_ug:
            tmp = []
            tmp.append(course_.course_code)
            tmp.append(course_.course_name)
            for x in course_.faculty_list:
                tmp.append(x)
            output_sheet.append(tmp)
        print(output_sheet)
        for course_ in self.current_course_pg:
            tmp = []
            tmp.append(course_.course_code)
            tmp.append(course_.course_name)
            for x in course_.faculty_list:
                tmp.append(x)
            output_sheet.append(tmp)
        df = pd.DataFrame(output_sheet)
        # File name needs to taken as input
        #df.to_csv('work_load_ODD_2023.csv')
        return df

    def compute_provisional_allotment_ug(self):
        # provides the course taught history from other files
        # update_course_history()
        # Each course has preferences setup -->
        # extract_preferences()
        # Allotment algorithm
        # Allotment does in Number of preferences
        for i in range(0, NUM_PREFERENCES-1):
        # Does for each current courses
            for ccug in self.current_course_ug:
                # order the faculty
                if ccug.get_requirement() > 0:
                    course_tmp_pref = []
                    for x in ccug.preference[i]:
                        if (self.faculty_list_master_data[x].can_accommodate_ug()):
                            course_tmp_pref.append(self.faculty_list_master_data[x])
                    n = len(course_tmp_pref)
                    print(n)
                    print(i, [[x.smail, x.priority_key] for x in course_tmp_pref])
                    for i_ in range(n-1):
                        for j_ in range(0, n-i_-1):
                            course_tmp_pref[j_], course_tmp_pref[j_ + 1] = ccug.tie_settle_ug(
                                course_tmp_pref[j_], course_tmp_pref[j_+1])
                    # Once the faculty is sorted out they are assigned to the course
                    print(i, [x.smail for x in course_tmp_pref])
                    for ctp in course_tmp_pref:
                        if ccug.get_requirement() > 0 and ctp.ug_sem==1:
                            ccug.assign_faculty(ctp.smail)
                            ctp.allot_course_ug(ccug)
                            print(ccug.course_name,ctp.smail)
    
    def extract_preferences(self,dat_file):
            # Course preference form
        self.faculty_on_roll = set()
        course_pref_data = pd.read_csv(dat_file)
        # Safe to sort the file
        course_pref_data = course_pref_data.sort_values(by=['Time stamp'])
        # Get the faculty on roll
        tmp_faculty_on_roll = list(course_pref_data['Mail id'])
        tmp_fac_roll = list(course_pref_data['Mail id'])
        self.faculty_on_roll = set(tmp_faculty_on_roll)
        prep_t = 1
        for froll in tmp_faculty_on_roll:
            self.faculty_list_master_data[froll].priority_key = prep_t
            prep_t += 1

        # iterating the columns
        cpd = list(course_pref_data.columns)
        print(cpd)
        assert NUM_PREFERENCES + \
            2 == len(cpd), "Preference Mismatch between file and definition"
        for i in range(3, len(cpd)):
            pref_c_to_f = list(course_pref_data[cpd[i]])
            for k in range(0, len(tmp_fac_roll)):
                self.course_list_master_data[pref_c_to_f[k]
                                        ].preference[i-3].append(tmp_fac_roll[k])

    def update_requirements(self, dat_file):
        faculty_requirement = pd.read_csv(dat_file)
        course_list_ = list(faculty_requirement['Course'])
        # TODO : update current_course_ug/pg based on requirement
        course_req_ = list(faculty_requirement[' Requirement'])
        if len(self.current_course_pg) + len(self.current_course_pg) == 0:
            for i in range(len(course_list_)):
                print(course_list_[i])
                self.course_list_master_data[course_list_[
                    i]].add_requirement(course_req_[i])
                if self.course_list_master_data[course_list_[i]].isUG_course():
                    self.current_course_ug.add(
                        self.course_list_master_data[course_list_[i]])
                else:
                    self.current_course_pg.add(
                        self.course_list_master_data[course_list_[i]])

    def set_faculty(self):
        flmd = pd.read_csv('./data/facultyList.csv')
        tmp_fac_name = flmd['Faculty Name']
        tmp_fac_mail = flmd['Mail id']
        for i in range(len(tmp_fac_mail)):
            self.faculty_list_master_data.update(
                {tmp_fac_mail[i]: faculty([tmp_fac_name[i], tmp_fac_mail[i]])})

# Create Course objects and convert it to dictionary it acts as a database HP
# has course list in Course code, Course Name, UG/PG (resembles a table in a database) Primary KEY - COURSE COD
    def set_courses(self):
        clmd = pd.read_csv('./data/courseList.csv')
        clmd = clmd.drop_duplicates(keep='first')
        clmd['Course Name'] = clmd['Course Name'].apply(str.lower)
        clmd['Course Name'] = clmd['Course Name'].apply(str.capitalize)
        # clmd.to_csv('courseList.csv', index=False)
        # Now the course list has unique courses and the course name is uniform
        tmp_course_list1 = list(clmd['Course code'])
        tmp_course_list2 = list(clmd['Course Name'])
        tmp_course_list3 = list(clmd['Course Type'])
        for i in range(0, len(tmp_course_list1)):
            self.course_list_master_data.update(
                {tmp_course_list1[i]: course(tmp_course_list1[i], tmp_course_list2[i])})
            if tmp_course_list3[i] != 'UG':
                self.course_list_master_data[tmp_course_list1[i]].set_as_pg()
# Convert pandas to HTML and then to pdf
# https://stackoverflow.com/questions/50807744/apply-css-class-to-pandas-dataframe-using-to-html
# https://www.pythonforbeginners.com/basics/convert-csv-to-pdf-file-in-python#:~:text=After%20obtaining%20the%20csv%20file,string%20to%20a%20pdf%20file.

    def get_tab_course_fac(self):
        output_sheet = []
        for course_ in self.current_course_ug:
            for x in course_.faculty_list:
                output_sheet.append(
                    [course_.course_name + " (" + course_.course_code + ")", self.faculty_list_master_data[x].name])
        output_sheet.sort(key=lambda x: x[0])
        # df_cf.columns = ['Course code', 'Course name', 'Faculty']
        df_cf = pd.DataFrame(output_sheet, columns=[
                             'Course', 'Faculty'], index=pd.Index(range(1, len(output_sheet)+1)))
        df_cf = df_cf.reindex(index=pd.Index(range(1, len(output_sheet)+1)))
        pd.set_option('colheader_justify', 'center')   # FOR TABLE <th>
        print("PRINT DONE")
        html_string = '''
        <html>
        <head><title>Course Allotment Aug-Nov 2023</title></head>
        <link rel="stylesheet" type="text/css" href="df_style.css"/>
        <body>
            {table}
        </body>
        </html>.
        '''
        # OUTPUT AN HTML FILE
        with open('allotment_1.html', 'w') as f:
            f.write(html_string.format(table=df_cf.to_html(classes='mystyle')))
        pdfkit.from_file('allotment_1.html', 'output_file_1.pdf',
                         options={"enable-local-file-access": ""})
        output_sheet.sort(key=lambda x: x[1])
        # df_cf.columns = ['Course code', 'Course name', 'Faculty']
        df_cf = pd.DataFrame(output_sheet, columns=[
                             'Course', 'Faculty'], index=pd.Index(range(1, len(output_sheet)+1)))
        df_cf = df_cf.reindex(columns=['Faculty', 'Course'])
        html_string = '''
        <html>
        <head><title>Course Allotment Aug-Nov 2023</title></head>
        <link rel="stylesheet" type="text/css" href="df_style.css"/>
        <body>
            {table}
        </body>
        </html>.
        '''
        # OUTPUT AN HTML FILE
        with open('allotment_2.html', 'w') as f:
            f.write(html_string.format(table=df_cf.to_html(classes='mystyle')))
        pdfkit.from_file('allotment_2.html', 'output_file_2.pdf',
                         options={"enable-local-file-access": ""})
