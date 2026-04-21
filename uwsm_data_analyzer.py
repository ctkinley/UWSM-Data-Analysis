# -*- coding: utf-8 -*-


# Chris Kinley
# 4/1/2026

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
pd.options.mode.chained_assignment = None  # default='warn'

# Takes a column of a dataframe and returns a list of all unique entries in the column, sorted by most frequent to least frequent
def take_unique(column):
  # If the column is composed of strings and not lists, uses the first options
  if isinstance(column[0], str):
    total_lst = []
    for i in range(len(column)):
      total_lst.append(column[i])
    unique_lst = list(set(total_lst))
    if "" in unique_lst:
      unique_lst.remove("")
    count_dict={}
    for i in unique_lst:
      count_dict[i]= total_lst.count(i)
    # sorts by most to least frequent
    count_dict = {k:v for k,v in sorted(count_dict.items(), key=lambda item: item[1], reverse=True)}
    total_lst = list(count_dict.keys())
    return total_lst
  # if the column is composed of a list of strings uses this option
  else:
    total_lst = []
    for i in range(len(column)):
      total_lst = total_lst+column[i]
    unique_lst = list(set(total_lst))
    if "" in unique_lst:
      unique_lst.remove("")
    count_dict={}
    for i in unique_lst:
      count_dict[i]= total_lst.count(i)
    # sorts by most to least frequent
    count_dict = {k:v for k,v in sorted(count_dict.items(), key=lambda item: item[1], reverse=True)}
    total_lst = list(count_dict.keys())
    return total_lst


# Applies the coding given by UWSM to the "What are the biggest challenges facing households in your community today?" column. Returns a list
def shorten_chall(lst):
  rename_dict = {"Paying for housing (rent, utilities, mortgage, taxes)":"Housing Cost", 'Covering basic expenses (groceries, gas, emergencies)':"Cost of Basics",
                 "Mental health challenges (like anxiety, depression)":"Mental Health", "Finding affordable healthcare": "Healthcare Cost",
                 "Jobs with low pay or no benefits":"Low Wages", "Child care that is affordable and available": "Affordable Child Care Access",
                 "Getting enough food":"Food Access", "Behavioral health challenges (like substance use or addiction)":"Behavioral Health",
                 "Getting to work, school, or appointments (transportation)":"Transportation", "Caring for aging parents or relatives": "Affordable Elder Care Access",
                  "Lack of stable jobs with career growth":"Job Instability", "Feeling isolated or not connected to community":"Social Isolation",
                 "Access to college or training after high school": "Education Access", "Impact of flooding and other extreme weather":"Climate Impacts",
                 "Finding affordable housing":"Affordable Housing Availability", "Language barriers":"Language Access", "High taxes":"Rising Taxes",
                 "ICE":"Immigration Enforcement", "Lack of in-home support":"Lack of in Home Support", "Gas mileage / fuel costs":"Gas Costs",
                 "Rising rents":"Rent Increases"}
  rename_dict_keys = list(rename_dict.keys())
  for i in range(len(lst)):
    if lst[i] in rename_dict_keys:
      lst[i]=rename_dict[lst[i]]
  return lst

# Adds additional ethnicity coding as requested. Returns a list
def code_ethnicity(lst):
  if lst == None:
    return ['']
  rename_dict = {"American Indian or Alaska Native":"BIPOC", 'Asian':"BIPOC",
                 "Black or African American":"BIPOC", "Hispanic":"BIPOC",
                 }
  add_lst = []
  rename_dict_keys = list(rename_dict.keys())
  if len(lst)>2:
    add_lst.append("More than one")
  for i in range(len(lst)):
    if lst[i] in rename_dict_keys:
      add_lst.append(rename_dict[lst[i]])
  add_lst=list(set(add_lst))
  return lst+add_lst

# codes location as requested, returns string
def code_location(stri):
  ok_list = ["York","Cumberland","Cumberland & York"]
  if stri in ok_list:
    return stri
  else:
    return "Outside Southern Maine"

# codes the "what type of employment" as requested, returns string
def code_job(stri):
  rename_dict =  {"32 hours":"Full-Time - 1 Job", 'a mixture of part time and self-employed':"Other",
                 "Freelance/contract":"Other", "Full-time hours (40 or more) working for more than one employer": "Full-Time - Multiple Jobs",
                 "Full-time hours (40 or more) working for one employer":"Full-Time - 1 Job", "I am election clerk working 3 times a year": "Other",
                 "Part-time hours (29 or less)":"Part-Time"
                 }
  rename_dict_keys = list(rename_dict.keys())
  if stri in rename_dict_keys:
    stri=rename_dict[stri]
  return stri

# Codes the "What supports would be most helpful for you?" question. Returns a list
def code_supports(lst):
  rename_dict =  {"Help with food or groceries":"Food", 'Help affording healthcare or mental health support':"Health/Mental Health",
                 "Help with transportation (gas, car repair, bus passes, etc.)":"Transportation", "Help with job training or education": "Job Training/Education",
                 "Help managing debt or improving credit":"Debt/Credit", "Employment navigation": "Employment",
                 "Rental assistance":"Rental Assistance", "Help navigating programs like SNAP, TANF":"SNAP/TANF Navigation",
                 }
  rename_dict_keys = list(rename_dict.keys())
  for i in range(len(lst)):
    if lst[i] in rename_dict_keys:
      lst[i]=rename_dict[lst[i]]
  return lst

# codes "What is your primary relationship with United Way of Southern Maine (UWSM)?". Returns a string
def code_connected(stri):
  rename_dict = {"Formerly Involved":"Formerly Connected", "I am closely connected (I am a UWSM volunteer, staff, or partner organization)": "Closely Connected",
                 "I am moderately connected (For example, I occasionally volunteer and/or donate to UWSM)":"Moderately Connected",
                 "I am not connected with United Way":"Not Connected"}
  rename_dict_keys = list(rename_dict.keys())
  if stri in rename_dict_keys:
    stri=rename_dict[stri]
  return stri

# codes "What is your age group?". Returns a list
def code_age(stri):
  rename_dict = {"Under 18":"Under 24", "18 - 24": "Under 24", "25 - 44": "25-64", "45 - 64":"25-64", "65 - 75":"65+", "More than 75":"65+"}
  rename_dict_keys = list(rename_dict.keys())

  if stri in rename_dict_keys:
    bob=[stri]+[rename_dict[stri]]
    return [stri]+[rename_dict[stri]]
  else:
    return [stri]

# codes "How would you consider getting involved locally to be part of the solution? (Select all that apply)". Returns a list
def code_get_involved(lst):
  rename_dict = {"Donating money to United Way of Southern Maine":"Donate", "Helping connect people to services or resources": "Connect",
                 "Speaking up or helping spread the word about important issues":"Speak Up", "Joining a group that solves community issues":"Join Group",
                 "Sharing my story or experiences to help others understand":"Share Story", "Volunteering my time or skills in local programs":"Volunteer"}
  rename_dict_keys = list(rename_dict.keys())
  for i in range(len(lst)):
    if lst[i] in rename_dict_keys:
      lst[i]=rename_dict[lst[i]]
  return lst
# codes the "What’s getting in the way of being able to cover your bills or living expenses? (Select all that apply)"
def code_getting_expenses(lst):
  rename_dict = {"I don’t have reliable transportation":"Lack of Reliable Transportation", "I’m caring for a family member": "Family Care Responsibilities",
                 "I have health issues or a disability":"Health Issues or Disability", "I don’t have the skills or training needed for a better-paying job":"Lack of Skills or Training",
                 "I’ve been turned away from jobs because of my background":"Turned Away", "I don’t have affordable child care":"Lack of Affordable Child Care",
                 "I’m not sure what opportunities are available":"Unaware of or Limited Job Opportunities"}
  rename_dict_keys = list(rename_dict.keys())
  for i in range(len(lst)):
    if lst[i] in rename_dict_keys:
      lst[i]=rename_dict[lst[i]]
  return lst
# Codes "What community are you referring to?  Please name the group, town, or city.". Returns a list
def code_which_community(stri):
  rename_dict = {"African American":["African American","BIPOC"], "Asian": ["Asian", "BIPOC"], "Everyone": ["Other"], "Foster kids":["Foster Kids", "Other"],
                 "Hispanic":["Hispanic", "BIPOC"], "Immigrant":["Immigrant"], "Indigenous":["Indigenous", "BIPOC"], "LGBTQ+":["LGBTQ+"],
                 "Low Income":["Low Income"], "Noble School": ["Youth (under 18)"], "Older adults":["Older adults(+65)"], "Parents":["Parents"],
                 "Recovery community":["Recovery community"],"Single mothers":["Single mothers"], "Town":["Town of Residence"], "White":["White"],
                 "Women":["Women"], "Youth":["Youth (under 18)"]}
  rename_dict_keys = list(rename_dict.keys())
  if stri in rename_dict_keys:
    return rename_dict[stri]
  else:
    return [stri]
# plots a singular horizontal bar chart from a given column. Pulls all the unique values and counts the number of instances. Only shows 8 most common entries
def plot_challenge(column, colors="blue", title=""):
  lst = []
  for i in column:
    lst = lst+i
  uniq = set(lst)
  chall_dict = {}
  for i in uniq:
    if i != "":
      chall_dict[i]=lst.count(i)
  chall_dict = {k:v for k,v in sorted(chall_dict.items(), key=lambda item: item[1], reverse=True)}
  x_values =shorten_chall(list(chall_dict.keys())[0:8])
  for i in range(len(x_values)):
    x_values[i] = x_values[i] + " (" + str(list(chall_dict.values())[i]) + ")"
  plt.barh(x_values, list(chall_dict.values())[0:8], color=colors)
  plt.title(title)
  plt.show()

# Plots a grouped bar chart based on two columns of a dataframe. Column a is the main column for diving the bar chart, with column b used to subdivide.
# notably plots from 0 to 1 based on the percentage of each category in column b that answered a specific answer in column a.
def plot_grouped_bar(column_a, column_b, number=7, colors="blue", title="", y_axis=""):
  # takes top 7 unique results of column a and top "number" of results of column b
  unique_col_a = take_unique(column_a)[0:7]
  unique_col_b = take_unique(column_b)[0:number]


  count_unique_col_b = {} # dictionary of unique entries of column b that corresponds with a list that holds the number of corresponding column a answers for each person who answered this b
  column_b_counts = {} # counts the number of entries of column b for each unique value
  # fills dictionaries with 0
  for i in unique_col_b:
    count_unique_col_b[i]=[0]*len(unique_col_a)
    column_b_counts[i] = 0
  # counts through column a and column b to fill the above dictionaries with the correct values
  for i in range(len(column_b)):
    for j in range(len(column_b[i])):
      if column_b[i][j] in unique_col_b:
        column_b_counts[column_b[i][j]] = column_b_counts[column_b[i][j]]+1
        for k in range(len(column_a[i])):
          if column_a[i][k] in unique_col_a:
            count_unique_col_b[column_b[i][j]][unique_col_a.index(column_a[i][k])] = count_unique_col_b[column_b[i][j]][unique_col_a.index(column_a[i][k])]+1
  # creates new dictionary that includes the count of each unique in column b in the name for the graph
  count_unique_col_b_incl_num = {}
  # fills dictionary with list that is proportion of people who answered column a for all people with the specific unique answer in b
  for i in unique_col_b:
    count_unique_col_b_incl_num[i + " (" + str(column_b_counts[i]) + ")"] = [0]*len(unique_col_a)
    for j in range(len(count_unique_col_b[i])):
      count_unique_col_b_incl_num[i + " (" + str(column_b_counts[i]) + ")"][j] = (count_unique_col_b[i][j])/(max(1,column_b_counts[i]))
  x = np.arange(len(unique_col_a))  # the label locations
  width = 0.7/len(unique_col_b)  # the width of the bars
  multiplier = 0

  # plots graph
  fig, ax = plt.subplots(layout='constrained')


  for attribute, measurement in count_unique_col_b_incl_num.items():
      offset = width * multiplier
      rects = ax.bar(x + offset, measurement, width, label=attribute)
      multiplier += 1



  # Add some text for labels, title and custom x-axis tick labels, etc.
  ax.set_ylabel(y_axis)
  ax.set_title(title)
  ax.set_xticks(x + (len(unique_col_b)-1)*width/2, unique_col_a, fontsize=36/len(unique_col_a))
  ax.legend(loc='upper right', ncols=2, fontsize=7)
  ax.set_ylim(0, 1)

  plt.show()

def main(file_name):

  # reads csv and renames columns to be more workable, Can be reverted at end of process if you wanted to export to csv.
  df = pd.read_csv(file_name)
  df = df.rename(columns={"Unique ID":"Unique ID","Survey Type":"Survey Type","Start time":"Start time",
                          "What are the biggest challenges facing households in your community today?":"biggest_challenge",
                          "Do you currently live or work in Southern Maine? (Can select more than one)":"live_maine",
                          "If an unexpected expense of $400 came up, would you be able to pay it?":"alice",
                          "Are you part of a community whose voice you feel is not being heard?":"heard",
                          "What community are you referring to?  Please name the group, town, or city. ":"which_community", "What is your age group?":"age",
                          "How do you describe your race or ethnicity? (Can select more than one)":"ethnicity",
                          "What is your primary relationship with United Way of Southern Maine (UWSM)?":"relationship",
                          "Want to get involved?":"get_involved",
                          "How would you consider getting involved locally to be part of the solution? (Select all that apply)":"how_get_involved",
                          "Which bills or everyday expenses are the hardest for your household to afford?":"hardest_expense", "What is your zip code?":"zip",
                          "Are you currently employed?":"employed", "What type of employment?":"type_employed",
                          "Can you describe more about how this financial challenge affects you or your family?":"describe_challenge",
                          "What’s getting in the way of being able to cover your bills or living expenses? (Select all that apply)":"obstacle_bills",
                          "What supports would be most helpful for you?":"helpful_support",
                          "Where would you like to be in 5 years? You can share anything that matters to you—like having a steady job, owning a home, goin":"5_years",
                          "How would you like to be part of creating change in your community? (Select all that apply)":"create_change",
                          "How long have you lived in Maine?":"duration_maine", "Would you be willing to share your story with others in the community?":"willing_share" })
  #print(df)
  #print(df["alice"])
  # fixing columns of df to use coding and apply a more consistent data structure for usage later
  df["age"] = df["age"].fillna("")
  df["age"]=df["age"].apply(lambda x:code_age(x))
  df["zip"] = "0"+df["zip"].fillna(0).astype(int).astype(str)
  for i in range(len(df["zip"])):
    if len(df["zip"][i])<5:
      df.loc[i, "zip"]="N/A"
  df["biggest_challenge"] = (df["biggest_challenge"].fillna('')).str.split(";")
  for i in df["biggest_challenge"]:
    i=shorten_chall(i)
  df["how_get_involved"] = ((df["create_change"].fillna('')+df["how_get_involved"].fillna(''))).str.split(";")
  for i in df["how_get_involved"]:
    i=code_get_involved(i)
  df["ethnicity"] = (df["ethnicity"].fillna('')).str.split(";")
  for i in df["ethnicity"]:
    i=code_ethnicity(i)

  for i in range(len(df["live_maine"])):
    df.loc[i, "live_maine"] = code_location(df.loc[i, "live_maine"])
  df["which_community"] = df["which_community"].fillna('')
  df["which_community"]=df["which_community"].apply(lambda x:code_which_community(x))

  df["hardest_expense"] =(df["hardest_expense"].fillna('')).str.split(";")
  df["obstacle_bills"] =(df["obstacle_bills"].fillna('')).str.split(";")
  for i in df["obstacle_bills"]:
    i = code_getting_expenses(i)
  df["helpful_support"] =(df["helpful_support"].fillna('')).str.split(";")
  for i in df["helpful_support"]:
    i = code_supports(df["helpful_support"])
  df["relationship"]=df["relationship"].fillna("")
  for i in range(len(df["relationship"])):
    df.loc[i, "relationship"]=code_connected(df.loc[i, "relationship"])
  df["type_employed"] = df["type_employed"].fillna('')
  for i in range(len(df["type_employed"])):
    df.loc[i, "type_employed"]=code_job(df.loc[i, "type_employed"])

  # zip codes in york and cumberland county area
  zip_code_in_area = ['04096', '04097', '04098', '04101', '04102', '04103', '04104', '04105', '04106', '04107', '04108', '04109', '04110', '04112', '04116',
                      '04260', '03901', '03902', '03903', '03904', '03905', '03906', '03907', '03908', '03909', '03910', '03911', '04001', '04002', '04003',
                      '04004', '04005', '04006', '04007', '04009', '04011', '04013', '04014', '04015', '04017', '04019', '04020', '04021', '04024', '04027',
                      '04028', '04029', '04030', '04032', '04038', '04039', '04040', '04042', '04043', '04046', '04047', '04048', '04049', '04050', '04053',
                      '04054', '04055', '04056', '04057', '04061', '04062', '04063', '04064', '04066', '04069', '04070', '04071', '04072', '04073', '04074',
                      '04075', '04076', '04077', '04078', '04079', '04082', '04083', '04084', '04085', '04087', '04090', '04091', '04092', '04093', '04094', '04095']

  # breaking the dataframe into three, one with all Southern Maine Residents, and then broken down by ALICE and non-ALICE
  tdf = df[(df["live_maine"]=="York")|(df["live_maine"]=="Cumberland")|(df["live_maine"]=="Cumberland & York")|(df["zip"].isin(zip_code_in_area))].reset_index()
  alice_df = tdf[(tdf["alice"]=="No")|(tdf["alice"]=="Maybe, with difficulty")].reset_index()
  non_alice_df=tdf[df["alice"]=="Yes"].reset_index()
  #print(alice_df["alice"])
  #print(non_alice_df["alice"])
  # Plotting the grouped bar charts of age/ethnicity and challenges. Two with all respondents and two with ALICE only
  plot_grouped_bar(tdf["biggest_challenge"], tdf["ethnicity"], title="Proportion of Respondants for each Challenge split by Ethnicity")
  plot_grouped_bar(tdf["biggest_challenge"], tdf["age"], title="Proportion of Respondants for each Challenge split by age group", number=9)
  plot_grouped_bar(alice_df["biggest_challenge"], alice_df["ethnicity"], title="Proportion of Respondants for each Challenge split by Ethnicity - ALICE")
  plot_grouped_bar(alice_df["biggest_challenge"], alice_df["age"], title="Proportion of Respondants for each Challenge split by age group - ALICE", number=9)




  # Plotting more bar charts for analysis
  plot_challenge(tdf["biggest_challenge"], title="Biggest Challenges for All Southern Maine Respondants")
  plot_challenge(alice_df["biggest_challenge"],colors="red", title="Biggest Challenges for ALICE Respondants")
  plot_challenge(non_alice_df["biggest_challenge"],colors="green", title="Biggest Challenges for non-ALICE Respondants")
  print("All")
  print(len(tdf["biggest_challenge"]))
  print("Alice")
  print(len(alice_df["biggest_challenge"]))
  print("Non-Alice")
  print(len(non_alice_df["biggest_challenge"]))
  plot_challenge(alice_df["age"],colors="red", title="Age of ALICE Respondants")
  plot_challenge(alice_df["ethnicity"],colors="red", title="Ethnicity of ALICE Respondants")
  plot_challenge(alice_df["how_get_involved"],colors="red", title="How ALICE Respondants want to get involved")
  plot_challenge(alice_df["hardest_expense"],colors="red", title="Hardest Bills for Alice Respondants")
  plot_challenge(tdf["which_community"], title="Community that is not being heard among all")
  plot_challenge(alice_df["which_community"],colors="red", title="Community that is not being heard among ALICE")

if __name__ == "__main__":
  main("UWSM Community Data 3-9-2026.xlsx - Data.csv")