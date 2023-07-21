#import Necessary module
import pandas as pd
import numpy as np
import streamlit as st
from PIL import Image
import plotly.express as pt
import os
from pathlib import Path
from streamlit_option_menu import option_menu
import time
import openpyxl as openExcel
import datetime as dt
import xlsxwriter
import dateutil.relativedelta as REL
import shutil
import chardet
import json


#---------------------------------------
#create session
if "Session_ID_SLT" not in st.session_state:
    st.session_state["Session_ID_SLT"]=dt.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")

 #---------------------------------------
#set sesstion details to push log file
if "Log_Person_DT" not in st.session_state:
    st.session_state["Log_Person_DT"]=None

if "Log_Login_Person" not in st.session_state:
    st.session_state["Log_Login_Person"]=None

if "Log_Login_In" not in st.session_state:
    st.session_state["Log_Login_In"]=None

if "Log_Login_Out" not in st.session_state:
    st.session_state["Log_Login_Out"]=None

if "Log_Procced_File" not in st.session_state:
    st.session_state["Log_Procced_File"]=None

if "Log_Any_Error" not in st.session_state:
    st.session_state["Log_Any_Error"]="No"

if "Log_Error_Line" not in st.session_state:
    st.session_state["Log_Error_Line"]=None

if "Log_Error_Details" not in st.session_state:
    st.session_state["Log_Error_Details"]=None

#---------------------------------------------

#set sesstion_state
if "Log_System" not in st.session_state:
    st.session_state["Log_System"]="NO"

if "dic_saved_files" not in st.session_state:
    st.session_state["dic_saved_files"]={}

if "dic_move_files" not in st.session_state:
    st.session_state["dic_move_files"]={}



#UserName
dic_UserPass = {
    "Name":["admin","Ashish"],
    "Password":["admin","Ashish123"]
}
# Variable initialization
project_name  = "Welcome to IQ Pharma ELT Solution: " # :wrench: 
project_title = "IQ Pharma"
icon_title    = ":bar_chart:"

# Variable for path setting :  Current folder/CSS Path/themse
current_folder_path =Path.cwd()
css_file_path = current_folder_path / "styles" / "css_style.css"
logo_file_path = current_folder_path / "assets" / "logo.png"
path_UAT_Dir =  current_folder_path / "UAT" /""
path_PRD_Dir =  current_folder_path / "PRD"/""
logo_about = current_folder_path / "about" / "abt.png"
var_DT = dt.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")


#page setting
st.set_page_config(
                    page_title=project_title,
                    page_icon=icon_title,
                    layout="wide"
)

#---------------------------------------
#file saving code

def fx_saved_log_data(var_Log_Name,var_Login_Person,var_Login_In,var_Login_Out, \
    Procced_File,var_Any_Error,var_Error_Line,var_Error_Details):
    
    #Created dic data
    dic = {
    var_Log_Name:[
        {"Login_Person"     : var_Login_Person}, \
        {"Login_In"         : var_Login_In}, \
        {"Login_Out"        : var_Login_Out}, \
        {"Procced_File"     : Procced_File}, \
        {"Any_Error"        : var_Any_Error}, \
        {"Error_Line"       : var_Error_Line}, \
        {"Error_Details"    : var_Error_Details} \
    ]
    }
 
    if os.path.exists(os.path.join(current_folder_path,"Log_File.json")):

        with open("Log_File.json","r") as file:
            read_dic = json.load(file)

        read_dic[var_Log_Name] =[ \
            {"Login_Person"     : var_Login_Person}, \
            {"Login_In"         : var_Login_In}, \
            {"Login_Out"        : var_Login_Out}, \
            {"Procced_File"     : Procced_File}, \
            {"Any_Error"        : var_Any_Error}, \
            {"Error_Line"       : var_Error_Line}, \
            {"Error_Details"    : var_Error_Details} \
                ]

        with open("Log_File.json","w") as file1:
            json.dump(read_dic,file1)

    else:

        with open("Log_File.json","w") as file:
            json.dump(dic,file)
        

def fx_get_log_data():
    try:

        with open('Log_File.json', 'r') as fcc_file:
            fcc_data = json.load(fcc_file)
        return json.dumps(fcc_data, indent=4,sort_keys=False)
    
    except Exception as e:
        st.info("Due to invalid operation ( Might be log file is not available), python can't process ahead." +"\n\n" +  str(e))
    finally:
        pass

#----------------------------------------------------


#Reading css file
with open(css_file_path) as css_file:
    st.markdown("<style> {} </style>".format(css_file.read()),unsafe_allow_html=True)

# Set logo
image = Image.open(logo_file_path)

#make center to logo
st.markdown(
    """
    <style>
        [data-testid=stSidebar] [data-testid=stImage]{
            text-align: center;
            display: block;
            margin-left: auto;
            margin-right: auto;
            width: 30%;
        }
    </style>
    """, unsafe_allow_html=True
)

# with st.sidebar:
#     st.image(image)

# st.sidebar.subheader("Login to access ELT Solution : ")
# Code to handle login request
st.sidebar.markdown("""
                        <span style='color:black;
                        font-weight: bold;
                        background-color: rgb(230, 231, 237);
                        font-size: 120%;
                        border: 1px solid;
                        box-shadow: 5px 10px;
                        padding: 10px;
                        border-radius: 25px'> 
                        Login to access ELT Solution : 
                        </span>
                        """,unsafe_allow_html=True
           )  


st.sidebar.markdown("---")  
get_userName = st.sidebar.text_input('User Name : :lock:',
                        max_chars=50,
                        placeholder="Enter your name...",
                        key="U_Name"
                        )
get_password = st.sidebar.text_input("User Password : :lock:",
                        max_chars=50,
                        placeholder="Enter your password...",
                        type="password",key="U_PASS"
                        )

get_reponse_submit = st.sidebar.button("Submit")
st.sidebar.markdown("---")
# st.sidebar.write('| :copyright:2023 |')

if get_reponse_submit:
    if (get_userName.upper() in [I.upper() for I in list(dic_UserPass["Name"])]) &  \
        ( get_password.upper() in [I.upper() for I in list(dic_UserPass["Password"]) ]):
        st.sidebar.success(f"Welcome : {get_userName} ...:+1:")
        st.session_state["Log_System"]="YES"
        st.session_state["Log_Login_Person"]=get_userName
        st.session_state["Log_Person_DT"]=get_userName +"_" + st.session_state["Session_ID_SLT"]
        st.session_state["Log_Login_In"]=var_DT
        st.session_state["Log_Login_Out"]=var_DT
        fx_saved_log_data(st.session_state["Log_Person_DT"], \
                          st.session_state["Log_Login_Person"], \
                          st.session_state["Log_Login_In"], \
                          st.session_state["Log_Login_Out"], \
                          st.session_state["Log_Procced_File"], \
                          st.session_state["Log_Any_Error"], \
                          st.session_state["Log_Error_Line"], \
                          st.session_state["Log_Error_Details"]            
                          )

    else:
        st.sidebar.success("Your Name/Password is not valid...:-1:")
        st.session_state["Log_System"]="NO"
        

#------------------------------------------------------------------------
st.write('<style>div.block-container{padding-top:0rem;}</style>', unsafe_allow_html=True)
#login person details :
with st.container():
    log_col1,log_col2,log_col3 = st.columns([2,1,1])
    log_col3.markdown(f"""
                        <span style='color:black;
                        font-weight: italic;
                        background-color: rgb(200, 218, 201);
                        font-size: 110%;
                        border-radius: 5px'> 
                        Login Person: {get_userName.capitalize()}
                        </span>
                        """,unsafe_allow_html=True
           )  

list_menu = ["HOME", "ELT PROCESS","DATA LOG","ABOUT" ]
list_Icon_menu = ["house","project","archive","book"]
selected_Menu_Item = option_menu(
                        menu_title=None,
                        options=list_menu,
                        default_index=0,
                        menu_icon=list_Icon_menu,
                        orientation="horizontal",
                        styles={
                        "container": {"padding": "1!important", "background-color": "grey"},
                        "icon": {"color": "orange", "font-size": "15px"}, 
                        "nav-link": {"font-size": "15px", "text-align": "left", "margin":"0px", "--hover-color": "#eee"},
                        "nav-link-selected": {"background-color": "orange"}
                                }


                            )
if selected_Menu_Item=="HOME":
    st.write("---")
    col1,col2 = st.columns((1.1,1))
    col1.subheader(project_name)
    col2.image(image)
    st.write("---")
    # st.subheader(project_name)
    st.write('#')
    st.subheader('Dear Preformist Team,')
    st.write('''
                IQPharma Technologies is pleased to submit our proposal in response to Preformist Reporting RFP. 
                We analyzed your requirements and developed a proposal tailored to meet your specific needs. 
                We understand that as a global organization, Preformist has multiple business units generating transparency reporting obligations. 
                Collecting spend data and ensuring all relevant transparency reporting requirements are met, can be a cumbersome and unwieldy process.
                This can lead to uncertainty about the completeness of reporting and expose Preformist to regulatory risks in multiple jurisdictions.    
                As we presented last week, our proposal focuses on three key areas, assessment, implementation, and ongoing operation. 
                We will deploy our considerable consulting resources to perform a thorough assessment to identify sources of spend data and identify 
                any gaps in transparency reporting. Once a complete picture is available, we will implement our technology solution, making the key 
                data connections that will enable us to manage your reporting program.  Upon implementation of our technology solution, we will provide 
                the human capital and expertise needed to operate your system, by interacting with Preformist stakeholders in all required languages.

                IQPHARMA TECHNOLOGIES is the largest global provider of commercial compliance consulting, software, and services. Our experience with transparency reporting is unmatched by any competitor. Our reach is truly global in terms of staff and physical presences in the US, Latin America, Europe, and Asia. Our experts are amongst the longest tenured from various transparency-focused organizations. Our ongoing investment in technology is driven by a clear vision focused on consumer-grade usability, seamless data interoperability, and the application of machine learning & artificial intelligence in across our products

            ''')
    if not (st.session_state["Log_Login_In"]) is None:
        st.session_state["Log_Login_Out"]=var_DT

elif selected_Menu_Item=="ELT PROCESS":
    login_flag =st.session_state["Log_System"]
    if login_flag=="NO":
        st.write(" Please login to see ETL Process.")
        if not (st.session_state["Log_Login_In"]) is None:
            st.session_state["Log_Login_Out"]=var_DT
    else:
        with st.expander("**Source Input...**"):
            # This code to take HCP Master Input
            st.write("#")
            st.markdown("""
                        <span style='color:black;
                        font-weight: italic;
                        background-color: rgb(230, 231, 237);
                        font-size: 100%;
                        border: 1px solid;
                        box-shadow: 1px 3px;
                        padding: 5px;
                        border-radius: 10px'> 
                        Select input sources to process the data. :ice_cube:
                        </span>
                        """,unsafe_allow_html=True
           )
           # This code to take Mapping Input 
           # Make one Master dictionary for holding all df frame
            dic_Master_DF ={}

#Error line 101       
            st.write("---")
            file_Mapping = st.file_uploader("(1) Upload Mapping File... ",
            accept_multiple_files=False,type=".xlsx")
            st.write("---")

            # This code to take Rep Master Input
            st.write("---")
            file_HCP_Master = st.file_uploader("(2) Upload HCP Master File... ",
            accept_multiple_files=False,type=".xlsx")
            #dictionary to hold data
            if file_HCP_Master is not None:
                dic_Master_DF["HCP_MASTER"]=file_HCP_Master            
 

            # This code to take Digital Banner Ads Input1
            st.write("---")
            file_Digital_Banner = st.file_uploader("(3) Upload Digital Banner Ads MTD Files... ",
            accept_multiple_files=True,type=".csv")
            st.write("---")
            #dictionary to hold data
            if file_Digital_Banner is not None:
                dic_Master_DF["MTD_WEEKLY_FILES"]=file_Digital_Banner

            # This code to take DMD Input2
            st.write("---")
            file_DMD = st.file_uploader("(4) Upload DMD File... ",
            accept_multiple_files=False,type=".csv")
            st.write("---")
            #dictionary to hold data
            if file_DMD is not None:
                dic_Master_DF["DMD"]=file_DMD

            # This code to take VMS Attendee Input
            st.write("---")
            file_Doximity = st.file_uploader("(5) Upload Doximity File... ",
            accept_multiple_files=False,type=".csv")
            st.write("---") 
            #dictionary to hold data
            if file_Doximity is not None:
                dic_Master_DF["DOXIMITY"]=file_Doximity  

            # This code to take Mtandi Sample Input
            st.write("---")
            file_Mtandi_Sample = st.file_uploader("(6) Upload Mtandi Sample File... ",
            accept_multiple_files=False,type=".csv")
            st.write("---")
            #dictionary to hold data
            if file_Mtandi_Sample is not None:
                dic_Master_DF["MTANDI_SAMPLES"]=file_Mtandi_Sample  

            # This code to take Mtandi Time People Input
            st.write("---")
            file_Mtandi_Time_People = st.file_uploader("(7) Upload Mtandi Time People File... ",
            accept_multiple_files=False,type=".csv")
            st.write("---")
            #dictionary to hold data
            if file_Mtandi_Time_People is not None:
                dic_Master_DF["DTP_TIME_PEOPLE"]=file_Mtandi_Time_People        

            # This code to take Mtandi Patient Saving Coupons Input
            st.write("---")
            file_Patient_Sav_Cou = st.file_uploader("(8) Upload Patient Saving Coupons File... ",
            accept_multiple_files=False,type=".xlsx")
            st.write("---")
            #dictionary to hold data
            if file_Patient_Sav_Cou is not None:
                dic_Master_DF["PATIENT_SAVING_COUPON"]=file_Patient_Sav_Cou  

            # This code to take Rep Email Activity Input
            st.write("---")
            file_Rep_Email = st.file_uploader("(9) Upload Rep Email Activity File... ",
            accept_multiple_files=False,type=".xlsx")
            st.write("---")
            #dictionary to hold data
            if file_Rep_Email is not None:
                dic_Master_DF["REP_EMAIL_ACTIVITY"]=file_Rep_Email    


            # This code to take VMS Attendee Input
            st.write("---")
            file_VMS_Attendee = st.file_uploader("(10) Upload VMS Attendee File... ",
            accept_multiple_files=False,type=".xlsx")
            st.write("---")
            #dictionary to hold data
            if file_VMS_Attendee is not None:
                dic_Master_DF["VMS_ATTENDEE"]=file_VMS_Attendee 

            # Push button
            st.write("#")

#Error line 102
            #-------------------------------------
            #This function will show progress bar along with operation
            #-------------------------------------
            def fx_show_progress_after_process(sht_name,df,df_ORG_data,delete_col_Flg="No",hdr_name="None", \
                                                fld_name="Validate_Field",list_delete_dup="DEA_Num"):

                """
                    When you call this function, this function will do ETL operation 

                    Args:
                            sheet Name: Mapping sheetname
                            df : Mapping
                            df_ORD_data      : Actual data
                            delete_col_Flg   : Flagging to delete particular column
                            hdr_name =       : Header name which you want
                            field name       : on which need to find max number
                            list_Delete_List : field which need to consider to delete duplicates
                     Return:
                        will be final_proceed data
                """
                #write code to do dataframe operation
                #------------------------------------
                df_original = df_ORG_data.copy()
                df_original=df_original.drop_duplicates()

                # this code is added to handle delete requirment of header.
                if delete_col_Flg=="Yes":
                    df_original=df_original.drop(hdr_name, axis='columns')

                #get distinct header name in list
                get_dis_hdr = df[sht_name].iloc[:,0].unique()
                
                #loop to run number of time with header
                for hdr in get_dis_hdr:

                    # st.write(hdr)
                    #filter data
                    filter_df = df[sht_name][df[sht_name].Field_Name==hdr].reset_index()

                    #loop till end of the row
                    for i in range(len(filter_df)):

                        #check first field type exits 1 ..............................
                        if filter_df.loc[i,"Field Type"].lower()=="existing":
                            
                            # check operation type "remove_space"
                            if filter_df.loc[i,"Operation_Type"].lower()=="remove_space":

                                var_field_name = filter_df.loc[i,"Field_Name"]
                                df_original[var_field_name] = df_original[var_field_name].apply(lambda x:str(x).strip())

                                #check operation type "drop_duplicates_multiple_field/drop_duplicates_single_field"
                            elif (filter_df.loc[i,"Operation_Type"].lower()=="drop_duplicates_multiple_field") | (filter_df.loc[i,"Operation_Type"].lower()=="drop_duplicates_single_field"):
                                df_original.drop_duplicates(filter_df.loc[i,"Conditions/Field"][1:][0:-1].replace('"',"").split(","))                                
                                df_original = df_original.replace('nan', '')

                                #Do number formating
                            elif (filter_df.loc[i,"Operation_Type"].lower()=="format_to_number"):
                                var_field_name = filter_df.loc[i,"Field_Name"]
                                df_original[var_field_name] = df_original[var_field_name].astype('Int64')

                                #Do text formating
                            elif (filter_df.loc[i,"Operation_Type"].lower()=="format_to_text"):
                                var_field_name = filter_df.loc[i,"Field_Name"]
                                df_original[var_field_name] = df_original[var_field_name].astype('str')

                                #Do LOOKUP_IF_BLANK_ROWS
                            elif (filter_df.loc[i,"Operation_Type"].lower()=="lookup_if_blank_rows"):

                                #Operation of filter data 
                                var_field_name = filter_df.loc[i,"Field_Name"]

                                df_org_No_Blank =  df_original[df_original[var_field_name].notnull()]
                                df_org_Blank =  df_original[df_original[var_field_name].isnull()]
                                
                                # to number of blank
                                if df_org_Blank.shape[0]>=1:

                                #     #Let's create new field
                                    var_search_val = filter_df.loc[i,"Conditions/Field"].split(":")[0][1:-1].split(",")
                                    var_search_Obj = filter_df.loc[i,"Conditions/Field"].split(":")[1].split('"')[0][0:-1]

                                    var_search_fld=filter_df.loc[i,"Conditions/Field"].split(":")[1].split('"')[2:-2] 
                                    var_search_fld= [val1 for val1 in var_search_fld if val1.find(",")]

                                    var_find_obj = filter_df.loc[i,"Conditions/Field"].split(":")[2].split('"')[0][0:-1]
                                    var_find_fld = filter_df.loc[i,"Conditions/Field"].split(":")[2].split('"')[1]


                                #     #Let's create combinded column in original dataset for lookup
                                    df_org_Blank['combined_L'] = df_org_Blank[var_search_val].apply(lambda row: '_'.join(row.values.astype(str)), axis=1)

                                #   #MergeOperation
                                #   # #first filter data with serach col and match col
                                    var_getData = pd.read_excel(dic_Master_DF[var_search_Obj],sheet_name=0,index_col=False,dtype=str)
                                    var_getData['combined_R'] = var_getData[var_search_fld].apply(lambda row: '_'.join(row.values.astype(str)), axis=1)
                                    
                                #     Set Right table
                                    var_fil_Right_df = var_getData[['combined_R',var_find_fld]]

                                    #Rename column to right table to avoid same column conflict
                                    var_fil_Right_df.rename({var_find_fld: 'New_' + var_find_fld}, axis=1, inplace=True)

                                #     # # #Filter left table
                                    var_fil_left_df = df_org_Blank

                                #     #Because lower function work with str then we need to force data type as str
                                    var_fil_left_df['combined_L']=var_fil_left_df['combined_L'].astype('str')
                                    var_fil_Right_df['combined_R']=var_fil_Right_df['combined_R'].astype('str')
                                    
                                    # #Opertion
                                    df_original1=pd.merge(left=var_fil_left_df, \
                                                        right=var_fil_Right_df, \
                                                        left_on=var_fil_left_df['combined_L'].str.lower(), \
                                                        right_on=var_fil_Right_df['combined_R'].str.lower(), \
                                                        how='left')
                                    
                                    list_allFild = list(var_fil_left_df.columns)
                                    list_allFild.append('New_' + var_find_fld)
                                    list_allFild.remove('combined_L')
                                    df_original1[var_find_fld]=df_original1['New_' + var_find_fld]
                                    list_allFild.remove('New_' + var_find_fld)
                                    df_original=pd.concat([df_org_No_Blank,df_original1[list_allFild]],axis=0)
                            
                            # check operation type "IF_Condition_IN"
                            elif filter_df.loc[i,"Operation_Type"].lower()=="if_else_condition":

                                var_fld_name        = filter_df.loc[i,"Conditions/Field"][0:][0:].split("=")[0]
                                var_filter_val1     = filter_df.loc[i,"Conditions/Field"][0:][0:].split("=")[1].split(":")[0].replace('"',"")
                                var_true_val_fld    = filter_df.loc[i,"Conditions/Field"][0:][0:].split("=")[1].split(":")[1].replace('(',"").replace(')',"")
                                var_false_val_fld   = filter_df.loc[i,"Conditions/Field"][0:][0:].split("=")[1].split(":")[2].replace('(',"").replace(')',"").replace('"',"")
                                
                                #Check wheather user want field or constant value at 1 Position
                                #-----------------------------------------------------------
                                if filter_df.loc[i,"Conditions/Field"][0:].split("=")[1].split(":")[1].find("(")>=0:
                                    var_fld_Value_true=df_original[var_true_val_fld]
                                else:
                                    var_fld_Value_true= var_true_val_fld
                                
                                #Check wheather user want field or constant value 2 Position
                                if filter_df.loc[i,"Conditions/Field"][0:].split("=")[1].split(":")[2].find("(")>=0:
                                    var_fld_Value_false=df_original[var_false_val_fld]
                                else:
                                    var_fld_Value_false= var_false_val_fld
                                #-------------------------------------------------------------

                                #Let's create new field here based on condition
                                df_original[filter_df.loc[i,"Field_Name"]] = \
                                    np.where(df_original[var_fld_name]==var_filter_val1, \
                                        var_fld_Value_true,var_fld_Value_false)
                       

                        #check first field type New 2............................
                        elif filter_df.loc[i,"Field Type"].lower()=="new":

                            ## check operation type "Assigned_Value"
                            if filter_df.loc[i,"Operation_Type"].lower()=="assigned_value":
                                df_original[filter_df.loc[i,"Field_Name"]] = filter_df.loc[i,"Conditions/Field"]

                            # check operation type "IF_Condition_IN"
                            elif filter_df.loc[i,"Operation_Type"].lower()=="if_condition_in":
                                #st.write(filter_df.loc[i,"Conditions/Field"])
                                var_fld_name        = filter_df.loc[i,"Conditions/Field"][0:].split("=")[0]
                                var_filter_val1     = filter_df.loc[i,"Conditions/Field"][0:].split("=")[1].split(":")[0].replace('["',"").replace('"]',"").replace('"',"").split(",")
                                var_true_val_fld    = filter_df.loc[i,"Conditions/Field"][0:].split("=")[1].split(":")[1].replace('(',"").replace(')',"")
                                var_false_val_fld   = filter_df.loc[i,"Conditions/Field"][0:].split("=")[1].split(":")[2].replace('(',"").replace(')',"").replace('"',"")

                                #Check wheather user want field or constant value at 1 Position
                                #-----------------------------------------------------------
                                if filter_df.loc[i,"Conditions/Field"][0:].split("=")[1].split(":")[1].find("(")>=0:
                                    var_fld_Value_true=df_original[var_true_val_fld]
                                else:
                                    var_fld_Value_true= var_true_val_fld
                                
                                #Check wheather user want field or constant value 2 Position
                                if filter_df.loc[i,"Conditions/Field"][0:].split("=")[1].split(":")[2].find("(")>=0:
                                    var_fld_Value_false=df_original[var_false_val_fld]
                                else:
                                    var_fld_Value_false= var_false_val_fld
                                #-------------------------------------------------------------

                                #Let's create new field here based on condition
                                df_original[filter_df.loc[i,"Field_Name"]] = \
                                    np.where(df_original[var_fld_name].str.lower().isin([val1.lower().strip() for val1 in var_filter_val1]), \
                                        var_fld_Value_true,var_fld_Value_false)

                            # check operation type "IF_Condition_Not_IN"
                            elif filter_df.loc[i,"Operation_Type"].lower()=="if_condition_not_in":
                                #st.write(filter_df.loc[i,"Conditions/Field"])
                                var_fld_name        = filter_df.loc[i,"Conditions/Field"][0:].split("=")[0]
                                var_filter_val1     = filter_df.loc[i,"Conditions/Field"][0:].split("=")[1].split(":")[0].replace('["',"").replace('"]',"").replace('"',"").split(",")
                                var_true_val_fld    = filter_df.loc[i,"Conditions/Field"][0:].split("=")[1].split(":")[1].replace('(',"").replace(')',"")
                                var_false_val_fld   = filter_df.loc[i,"Conditions/Field"][0:].split("=")[1].split(":")[2].replace('(',"").replace(')',"").replace('"',"")

                                #Check wheather user want field or constant value at 1 Position
                                #-----------------------------------------------------------
                                if filter_df.loc[i,"Conditions/Field"][0:].split("=")[1].split(":")[1].find("(")>=0:
                                    var_fld_Value_true=df_original[var_true_val_fld]
                                else:
                                    var_fld_Value_true= var_true_val_fld
                                
                                #Check wheather user want field or constant value 2 Position
                                if filter_df.loc[i,"Conditions/Field"][0:].split("=")[1].split(":")[2].find("(")>=0:
                                    var_fld_Value_false=df_original[var_false_val_fld]
                                else:
                                    var_fld_Value_false= var_false_val_fld
                                #-------------------------------------------------------------

                                #Let's create new field here based on condition
                                df_original[filter_df.loc[i,"Field_Name"]] = \
                                    np.where(~df_original[var_fld_name].str.lower().isin([val1.lower().strip() for val1  in var_filter_val1]), \
                                        var_fld_Value_true,var_fld_Value_false)                                

                            # check operation type "IF_Condition_Contain"
                            elif filter_df.loc[i,"Operation_Type"].lower()=="if_condition_contain":
                                #st.write(filter_df.loc[i,"Conditions/Field"])
                                var_fld_name        = filter_df.loc[i,"Conditions/Field"][0:].split("=")[0]
                                var_filter_val1     = filter_df.loc[i,"Conditions/Field"][0:].split("=")[1].split(":")[0].replace('["',"").replace('"]',"").replace('"',"").split(",")
                                var_true_val_fld    = filter_df.loc[i,"Conditions/Field"][0:].split("=")[1].split(":")[1].replace('(',"").replace(')',"")
                                var_false_val_fld   = filter_df.loc[i,"Conditions/Field"][0:].split("=")[1].split(":")[2].replace('(',"").replace(')',"").replace('"',"")
                                
                                #Check wheather user want field or constant value at 1 Position
                                #-----------------------------------------------------------
                                if filter_df.loc[i,"Conditions/Field"][0:].split("=")[1].split(":")[1].find("(")>=0:
                                    var_fld_Value_true=df_original[var_true_val_fld]
                                else:
                                    if var_false_val_fld=="NULL" or var_false_val_fld==None or var_false_val_fld=="None" or var_false_val_fld=="":
                                        var_fld_Value_false= None
                                    else:
                                        var_fld_Value_false= var_false_val_fld
                                
                                #Check wheather user want field or constant value 2 Position
                                if filter_df.loc[i,"Conditions/Field"][0:].split("=")[1].split(":")[2].find("(")>=0:
                                    var_fld_Value_false=df_original[var_false_val_fld]
                                else:
                                    if var_false_val_fld=="NULL" or var_false_val_fld==None or var_false_val_fld=="None" or var_false_val_fld=="":
                                        var_fld_Value_false= None
                                    else:
                                        var_fld_Value_false= var_false_val_fld
                                #-------------------------------------------------------------

                                #Make upper to field befor opetion
                                df_original[var_fld_name] = df_original[var_fld_name].str.lower()

                                #Let's create new field here based on condition df_original[var_fld_name].str.upper()
                                df_original.loc[df_original[var_fld_name].str.contains("|".join( \
                                    [val1.lower().strip() for val1 in var_filter_val1])), \
                                        filter_df.loc[i,"Field_Name"]]=var_fld_Value_true

                                df_original.loc[~df_original[var_fld_name].str.contains("|".join( \
                                    [val1.lower().strip() for val1 in var_filter_val1])), \
                                        filter_df.loc[i,"Field_Name"]]=var_fld_Value_false

                            # check operation type "if_condition_not_contain"
                            elif filter_df.loc[i,"Operation_Type"].lower()=="if_condition_not_contain":
                                #st.write(filter_df.loc[i,"Conditions/Field"])
                                var_fld_name        = filter_df.loc[i,"Conditions/Field"][0:].split("=")[0]
                                var_filter_val1     = filter_df.loc[i,"Conditions/Field"][0:].split("=")[1].split(":")[0].replace('["',"").replace('"]',"").replace('"',"").split(",")
                                var_true_val_fld    = filter_df.loc[i,"Conditions/Field"][0:].split("=")[1].split(":")[1].replace('(',"").replace(')',"")
                                var_false_val_fld   = filter_df.loc[i,"Conditions/Field"][0:].split("=")[1].split(":")[2].replace('(',"").replace(')',"").replace('"',"")

                                #Check wheather user want field or constant value at 1 Position
                                #-----------------------------------------------------------
                                if filter_df.loc[i,"Conditions/Field"][0:].split("=")[1].split(":")[1].find("(")>=0:
                                    var_fld_Value_true=df_original[var_true_val_fld]
                                else:
                                    var_fld_Value_true= var_true_val_fld
                                
                                #Check wheather user want field or constant value 2 Position
                                if filter_df.loc[i,"Conditions/Field"][0:].split("=")[1].split(":")[2].find("(")>=0:
                                    var_fld_Value_false=df_original[var_false_val_fld]
                                else:
                                    var_fld_Value_false= var_false_val_fld
                                #-------------------------------------------------------------

                                #Make upper to field befor opetion
                                df_original[var_fld_name] = df_original[var_fld_name].str.upper()

                                #Let's create new field here based on condition
                                df_original[filter_df.loc[i,"Field_Name"]] = \
                                    np.where(~df_original[var_fld_name].str.contains([val1.upper().strip() for val1 in var_filter_val1]), \
                                        var_fld_Value_true,var_fld_Value_false)

                            # check operation type "Week Number starting from Jan
                            elif filter_df.loc[i,"Operation_Type"].lower()=="round_week_near_friday":

                                #Let's create new field
                                var_fil_format = filter_df.loc[i,"Conditions/Field"].split("=")[0][1:-1]
                                var_data_fld   = filter_df.loc[i,"Conditions/Field"].split("=")[1][1:-1]
                                df_original[filter_df.loc[i,"Field_Name"]] =  "WK-" + pd.to_datetime(df_original[var_data_fld]).dt.strftime("%W")
                               

                            # check operation type "round_date_coming_friday"
                            elif filter_df.loc[i,"Operation_Type"].lower()=="round_date_coming_friday":

                                #Let's create new field
                                var_fil_format = filter_df.loc[i,"Conditions/Field"].split("=")[0][1:-1]
                                var_data_fld   = filter_df.loc[i,"Conditions/Field"].split("=")[1][1:-1]
                                df_original[filter_df.loc[i,"Field_Name"]] =  pd.to_datetime(df_original[var_data_fld]).dt.to_period("w").dt.start_time + pd.Timedelta(4,unit='d')

                            # check operation type "Year"
                            elif filter_df.loc[i,"Operation_Type"].lower()=="find_year":

                                #Let's create new field
                                var_fil_format = filter_df.loc[i,"Conditions/Field"].split("=")[0][1:-1]
                                var_data_fld   = filter_df.loc[i,"Conditions/Field"].split("=")[1][1:-1]
                                df_original[filter_df.loc[i,"Field_Name"]] =  df_original[var_data_fld].dt.year
                                
                            # check operation type "Month"
                            elif filter_df.loc[i,"Operation_Type"].lower()=="find_month":

                                #Let's create new field
                                var_fil_format = filter_df.loc[i,"Conditions/Field"].split("=")[0][1:-1]
                                var_data_fld   = filter_df.loc[i,"Conditions/Field"].split("=")[1][1:-1]
                                df_original[filter_df.loc[i,"Field_Name"]] =  df_original[var_data_fld].dt.month

                            # check operation type "day"
                            elif filter_df.loc[i,"Operation_Type"].lower()=="find_day":

                                #Let's create new field
                                var_fil_format = filter_df.loc[i,"Conditions/Field"].split("=")[0][1:-1]
                                var_data_fld   = filter_df.loc[i,"Conditions/Field"].split("=")[1][1:-1]
                                df_original[filter_df.loc[i,"Field_Name"]] =  df_original[var_data_fld].dt.day

                            # check operation type "Lookup"
                            elif filter_df.loc[i,"Operation_Type"].lower()=="lookup":

                                #Let's create new field
                                var_search_val = filter_df.loc[i,"Conditions/Field"].split(":")[0]
                                var_search_Obj = filter_df.loc[i,"Conditions/Field"].split(":")[1].split('"')[0][0:-1]
                                var_search_fld = filter_df.loc[i,"Conditions/Field"].split(":")[1].split('"')[1]
                                var_find_obj = filter_df.loc[i,"Conditions/Field"].split(":")[2].split('"')[0][0:-1]
                                var_find_fld = filter_df.loc[i,"Conditions/Field"].split(":")[2].split('"')[1]
                                #MergeOperation

                                #first filter data with serach col and match col
                                var_getData = pd.read_excel(dic_Master_DF[var_search_Obj],sheet_name=0,index_col=False,dtype=str)
                                
                                #==========================================================
                                # This is code is handle to custome requirement
                                if sht_name=="DOXIMITY" or sht_name=="DTP_TIME_PEOPLE" or sht_name=="DMD" or sht_name=="PATIENT_SAVING_COUPON":
                                    hold_hdr = var_getData.columns
                                    var_getData1=var_getData[[list_delete_dup,fld_name]]
                                    df_groupy= var_getData1.groupby([list_delete_dup])[fld_name].aggregate(['max'])
                                    df_output_data = df_groupy.reset_index().copy()
                                    df_output_data=df_output_data.drop_duplicates(subset=[list_delete_dup])
                                    df_output_data.rename({list_delete_dup: 'Nev_'+list_delete_dup}, axis=1, inplace=True)

                                    #Joining to limit the data
                                    var_getData=pd.merge(left=var_getData, \
                                                        right=df_output_data, \
                                                        left_on=[list_delete_dup,"Validate_Field"], \
                                                        right_on=['Nev_'+list_delete_dup,"max"], \
                                                        how='inner')
                                    var_getData = var_getData[hold_hdr]
                                    var_getData=var_getData.drop_duplicates(subset=[list_delete_dup])
                                #==========================================================
                                # get right table here
                                var_fil_Right_df = var_getData[[var_search_fld,var_find_fld]]

                                #Rename column to right table to avoid same column conflict
                                var_fil_Right_df.rename({var_search_fld: 'New_'+var_search_fld}, axis=1, inplace=True)

                                # #Filter left table
                                var_fil_left_df = df_original
                                
                                #Because lower function work with str then we need to force data type as str

                                var_fil_left_df[var_search_val]=var_fil_left_df[var_search_val].astype('str')
                                var_fil_Right_df['New_'+var_search_fld]=var_fil_Right_df['New_'+var_search_fld].astype('str')

                                #Opertion
                                df_original1=pd.merge(left=var_fil_left_df, \
                                                     right=var_fil_Right_df, \
                                                     left_on=var_fil_left_df[var_search_val].str.lower(), \
                                                     right_on=var_fil_Right_df['New_'+var_search_fld].str.lower(), \
                                                     how='left')
                                list_allFild = list(var_fil_left_df.columns)
                                list_allFild.append(var_find_fld)
                                df_original=df_original1[list_allFild]
                                
                            # This operation for lookup with multiple column keys
                            elif filter_df.loc[i,"Operation_Type"].lower()=="lookup_with_multiple_key":
                                
                                #Operation of filter data 
                                var_field_name = filter_df.loc[i,"Field_Name"]

                            #     #Let's create new field
                                var_search_val = filter_df.loc[i,"Conditions/Field"].split(":")[0][1:-1].split(",")
                                var_search_Obj = filter_df.loc[i,"Conditions/Field"].split(":")[1].split('"')[0][0:-1]

                                var_search_fld=filter_df.loc[i,"Conditions/Field"].split(":")[1].split('"')[2:-2] 
                                var_search_fld= [val1 for val1 in var_search_fld if val1.find(",")]

                                var_find_obj = filter_df.loc[i,"Conditions/Field"].split(":")[2].split('"')[0][0:-1]
                                var_find_fld = filter_df.loc[i,"Conditions/Field"].split(":")[2].split('"')[1]


                            #     #Let's create combinded column in original dataset for lookup
                                df_original['combined_L'] = df_original[var_search_val].apply(lambda row: '_'.join(row.values.astype(str)), axis=1)

                            #   #MergeOperation
                            #   # #first filter data with serach col and match col
                                var_getData = pd.read_excel(dic_Master_DF[var_search_Obj],sheet_name=0,index_col=False,dtype=str)
                                var_getData['combined_R'] = var_getData[var_search_fld].apply(lambda row: '_'.join(row.values.astype(str)), axis=1)
                                
                            #     Set Right table
                                var_fil_Right_df = var_getData[['combined_R',var_find_fld]]

                             #     # # #Filter left table
                                var_fil_left_df = df_original

                            #     #Because lower function work with str then we need to force data type as str
                                var_fil_left_df['combined_L']=var_fil_left_df['combined_L'].astype('str')
                                var_fil_Right_df['combined_R']=var_fil_Right_df['combined_R'].astype('str')
                                
                                # #Opertion
                                df_original1=pd.merge(left=var_fil_left_df, \
                                                    right=var_fil_Right_df, \
                                                    left_on=var_fil_left_df['combined_L'].str.lower(), \
                                                    right_on=var_fil_Right_df['combined_R'].str.lower(), \
                                                    how='left')
                                
                                list_allFild = list(var_fil_left_df.columns)
                                list_allFild.append(var_find_fld)
                                list_allFild.remove('combined_L')
                                df_original=df_original1[list_allFild]

                # st.write(df_original)
                
                # check file is available
                if os.path.exists(path_UAT_Dir):
                    df_original.columns = map(lambda x: x.upper(),df_original.columns)
                    df_original.to_excel(os.path.join(path_UAT_Dir,sht_name + "_" + var_DT + ".xlsx"),index=False,na_rep='',sheet_name="Data",engine='xlsxwriter')
                    st.session_state.dic_move_files[sht_name] = sht_name + "_" + var_DT + ".xlsx"
                else:
                    os.makedirs("UAT")
                    df_original.columns = map(lambda x: x.upper(),df_original.columns)
                    df_original.to_excel(os.path.join(path_UAT_Dir,sht_name + "_" + var_DT + ".xlsx"),index=False,na_rep='',sheet_name="Data",engine='xlsxwriter')
                    st.session_state.dic_move_files[sht_name] = sht_name + "_" + var_DT + ".xlsx"
                


                #------------------------------------
                #add placeholder
                place_holder =st.empty()
                bar=st.progress(0)
                for x in range(100):
                    place_holder.text(f"Python is processing ...{sht_name}")
                    bar.progress(x+1)
                    # time.sleep(0.001)
                place_holder.text(f"File processing is done...{sht_name}")

#Error line 103 

            #Python function to merge data ( CSV )
            def fx_combined_dir_data(file_uploader_obj,var_header_search="Site (DCM)",lookat_hdr=["get_hdr"]):

                pos=None
                var_count=1
                df_result1=None
                list_data_hdr=lookat_hdr

                for raw_data in file_uploader_obj:                
                    df_result = pd.read_csv(raw_data)

                    #checking the value , wheather it is nan , if you test nan==nan then it will give you false
                    if df_result.iloc[0,0]==df_result.iloc[0,0]: # if it nan value ()
                        if var_count==1: # check 1st time operation
                            if str(df_result.columns[0]).lower()==var_header_search.lower(): # check if header match
                                df_result.columns=list_data_hdr
                                df_result1=df_result
                            else: # check if it header is not what expecting
                                for i,row in df_result.iterrows():
                                    if row.notnull().all():
                                        pos = i
                                        break
                                df_result.columns=list_data_hdr
                                df_result1=df_result.iloc[pos+1:,:]

                        else: # var_count 2nd or more than beyond time

                            if str(df_result.columns[0]).lower()==var_header_search.lower(): # check if header match
                                df_result.columns=list_data_hdr
                                df_result1=pd.concat([df_result1,df_result],axis=0)
                            else:  # check if it header is not what expecting
                                for i,row in df_result.iterrows():
                                    if row.notnull().all():
                                        pos = i
                                        break
                                df_result.columns=list_data_hdr
                                df_result=df_result.iloc[pos+1:,:]
                                df_result1=pd.concat([df_result1,df_result],axis=0,ignore_index=True)
                    else: # this case when nan values found
                        if var_count==1: #1st count with nan
                            if str(df_result.columns[0]).lower()==var_header_search.lower(): # check if header match
                                df_result.columns=list_data_hdr
                                df_result1=df_result
                            else: # check if it header is not what expecting
                                for i,row in df_result.iterrows():
                                    if row.notnull().all():
                                        pos = i
                                        break
                                df_result.columns=list_data_hdr
                                df_result1=df_result.iloc[pos+1:,:]
                        else: # 2nd count with nan
                            if str(df_result.columns[0]).lower()==var_header_search.lower(): # check if header match
                                df_result.columns=list_data_hdr
                                df_result1=pd.concat([df_result1,df_result],axis=0)
                            else:  # check if it header is not what expecting
                                for i,row in df_result.iterrows():
                                    if row.notnull().all():
                                        pos = i
                                        break
                                df_result.columns=list_data_hdr
                                df_result=df_result.iloc[pos+1:,:]
                                df_result1=pd.concat([df_result1,df_result],axis=0,ignore_index=True)

                    var_count+=1
                return df_result1.reset_index(drop=True)
#Error line 104 
            buttn_PD = st.button("Process Data")
            if buttn_PD:

                try:
                    
                    st.write("----------------------------------------------------------------------------")
                    place_holder = st.empty()
                    st.write("----------------------------------------------------------------------------")    
                    place_holder.text("Transformation has been started...Please wait !")
                    st.write("#")

                    #"Reading Mapping File"
                    df_Mapping = pd.read_excel(file_Mapping,sheet_name=None,index_col=False,dtype=str)

                    #Remove Action list sheet operation
                    del df_Mapping["Action_List"]
                    
                    #Loop to run number of times to operate on excel based operation
                    for sht in [sht for sht in list(df_Mapping.keys()) if sht.lower!="action_list"]:
                        if  sht=="HCP_MASTER" or sht=="REP_EMAIL_ACTIVITY" or sht=="DOXIMITY" or sht=="VMS_ATTENDEE" or  sht=="DTP_TIME_PEOPLE" or  sht=="DMD" or  sht=="MTANDI_SAMPLES" or sht=="PATIENT_SAVING_COUPON" or sht=="MTD_WEEKLY_FILES":
                            if sht=="DTP_TIME_PEOPLE" :

                                fx_show_progress_after_process(sht, \
                                    df_Mapping, \
                                    pd.read_csv(dic_Master_DF[sht],dtype=str),\
                                    delete_col_Flg="Yes", \
                                    hdr_name="Preformist_ID") # This function is having more paramer to handle the requirment
                                st.session_state.dic_saved_files[sht] = os.path.join(path_UAT_Dir,   sht + "_" + var_DT + ".xlsx")

                            elif sht=="DOXIMITY" or sht=="DMD" or sht=="MTANDI_SAMPLES":
                                fx_show_progress_after_process(sht, \
                                    df_Mapping, \
                                    pd.read_csv(dic_Master_DF[sht],dtype=str))
                                st.session_state.dic_saved_files[sht] = os.path.join(path_UAT_Dir,   sht + "_" + var_DT + ".xlsx")

                            elif sht=="PATIENT_SAVING_COUPON":
                                fx_show_progress_after_process(sht, \
                                    df_Mapping, \
                                    pd.read_excel(dic_Master_DF[sht],dtype=str,skiprows=4))
                                st.session_state.dic_saved_files[sht] = os.path.join(path_UAT_Dir,   sht + "_" + var_DT + ".xlsx")

                            elif sht=="MTD_WEEKLY_FILES":
                                    list_data_hdr=['Site (DCM)','Designated Market Area (DMA)','Placement Cost Structure',
                                                    'Campaign','Date','Impressions','Clicks','Click Rate','Media Cost',
                                                    'Cost Per Click','Effective CPM']
                                    find_hdr = "Site (DCM)"
                                    final_df = fx_combined_dir_data(file_Digital_Banner,var_header_search=find_hdr,lookat_hdr=list_data_hdr)
                                    final_df=final_df[~final_df[find_hdr].str.lower().isin(["grand total:","total",":"])]
                                    fx_show_progress_after_process(sht, \
                                        df_Mapping, \
                                        final_df)
                                    st.session_state.dic_saved_files[sht] = os.path.join(path_UAT_Dir,   sht + "_" + var_DT + ".xlsx")
                                    

                            else:
                                fx_show_progress_after_process(sht, \
                                    df_Mapping, \
                                    pd.read_excel(dic_Master_DF[sht],sheet_name=0,index_col=False,dtype=str))
                                st.session_state.dic_saved_files[sht] = os.path.join(path_UAT_Dir,   sht + "_" + var_DT + ".xlsx")
                        
                    #final message
                    place_holder.text("Transformation has been completed...")
                    st.success("All files has been proceed and can view inside output result expander .")
                    st.session_state["Log_Procced_File"] = [item_file for item_file in st.session_state.dic_saved_files.keys()]
                    if not (st.session_state["Log_Login_In"]) is None:
                        st.session_state["Log_Login_Out"]=var_DT
                    fx_saved_log_data(st.session_state["Log_Person_DT"], \
                          st.session_state["Log_Login_Person"], \
                          st.session_state["Log_Login_In"], \
                          st.session_state["Log_Login_Out"], \
                          st.session_state["Log_Procced_File"], \
                          st.session_state["Log_Any_Error"], \
                          st.session_state["Log_Error_Line"], \
                          st.session_state["Log_Error_Details"]            
                          )
                except Exception as e:

                    st.info("Due to invalid input python can't process ahead." +"\n\n" +  str(e))
                    st.session_state["Log_Any_Error"]="Yes"
                    st.session_state["Log_Error_Line"]="Line Between:103-104"
                    st.session_state["Log_Error_Details"] = str(e)
                    st.session_state["Log_Login_Out"]=var_DT
                    st.session_state["Log_Any_Error"]="Yes"
                    fx_saved_log_data(st.session_state["Log_Person_DT"], \
                            st.session_state["Log_Login_Person"], \
                            st.session_state["Log_Login_In"], \
                            st.session_state["Log_Login_Out"], \
                            st.session_state["Log_Procced_File"], \
                            st.session_state["Log_Any_Error"], \
                            st.session_state["Log_Error_Line"], \
                            st.session_state["Log_Error_Details"]            
                            )

#Error line 106
        with st.expander("**Output Result...**"):

                    #Total Proceed files
                    st.write("====================================")
                    st.write(f"Total [ {len(st.session_state.dic_saved_files)} ] files has proceed inisde UAT directory .")
                    st.write("====================================")
                    st.write("File name with directory are :")
                    for key_fl,item_file in st.session_state.dic_saved_files.items():
                        st.write("----------------------------------------------------------------------------")
                        st.write(f"File Name : {key_fl}")
                        st.write(f"Path      : {item_file}")
                        st.write("----------------------------------------------------------------------------")


                    action_btn = st.selectbox("Export data from UAT to PRD Directory.",["Yes","No"],index=1)
                    if action_btn=="Yes":
                        for key1,item1 in st.session_state.dic_saved_files.items():
                            shutil.copy2(item1,os.path.join(path_PRD_Dir, key1 + ".xlsx"))
                        if len(st.session_state.dic_saved_files)>=1:
                            st.success("Data has been moved to PRD places. Thank you !!")
                            st.session_state["Log_Login_Out"]=var_DT
                        else:
                            st.info("There is no file in queue to export production place!")
                            st.session_state["Log_Login_Out"]=var_DT
                        fx_saved_log_data(st.session_state["Log_Person_DT"], \
                                st.session_state["Log_Login_Person"], \
                                st.session_state["Log_Login_In"], \
                                st.session_state["Log_Login_Out"], \
                                st.session_state["Log_Procced_File"], \
                                st.session_state["Log_Any_Error"], \
                                st.session_state["Log_Error_Line"], \
                                st.session_state["Log_Error_Details"]            
                                )  

elif selected_Menu_Item=="DATA LOG":
    st.write("#")
    login_flag =st.session_state["Log_System"]
    if login_flag=="YES":
        st.write("Welcome back to Data Log place.Kindly click on below expander to get logs details. ")
        with st.expander("**Log Details...**"):
            st.write(fx_get_log_data())
            st.write("#")
            st.session_state["Log_Login_Out"]=var_DT
            fx_saved_log_data(st.session_state["Log_Person_DT"], \
                            st.session_state["Log_Login_Person"], \
                            st.session_state["Log_Login_In"], \
                            st.session_state["Log_Login_Out"], \
                            st.session_state["Log_Procced_File"], \
                            st.session_state["Log_Any_Error"], \
                            st.session_state["Log_Error_Line"], \
                            st.session_state["Log_Error_Details"]            
                            )
    else:
        st.write(" Please login to see Data Log details.")
        st.session_state["Log_Login_Out"]=var_DT

elif selected_Menu_Item=="ABOUT":
    st.write("#")
    col1_abt,col2_abt = st.columns(2) 
    with col1_abt:
        image_abt = Image.open(logo_about)
        change_wid_img = image_abt.resize((400,400))
        st.image(change_wid_img)

    with col2_abt:
        st.subheader("ABOUT US")
        st.write("#")
        st.write('''
        IQPHARMA TECHNOLOGIES is the largest global provider of commercial compliance consulting, 
        software, and services. Our experience with transparency reporting is unmatched by any competitor. 
        Our reach is truly global in terms of staff and physical presences in the US, Latin America,
         Europe, and Asia. Our experts are amongst the longest tenured from various transparency-focused 
         organizations. Our ongoing investment in technology is driven by a clear vision focused on 
         consumer-grade usability, seamless data interoperability, and the application of machine learning & 
         artificial intelligence in across our products.
        ''')

#Error line 107





            
   
                


