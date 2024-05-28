import os
 
languageCodes=["cn", "ko", "ja", "de", "it", "fr", "es", "en"]

folder_path = r"C:\Users\CNMIZHU7\Downloads\MultiLanguageRename"
file_names = []
for file_name in os.listdir(folder_path):
    if os.path.isfile(os.path.join(folder_path, file_name)):
        file_names.append(file_name)

# for languageCode in languageCodes:
#     for file_name in file_names:
#         if(file_name.lower().endswith(f"{languageCode}.png") and len(file_name)<=22):
#             key = file_name[0:12]
#             for file_name_second in file_names:
#                 if(file_name_second.startswith(key) and file_name_second.lower().endswith(f"{languageCode}.png") and file_name_second!=file_name):
#                     os.remove(os.path.join(folder_path, file_name_second))
#                     os.rename(os.path.join(folder_path, file_name), os.path.join(folder_path, file_name_second))

for file_name in file_names:
    if(len(file_name)>22):
        newfilenameprefix = file_name[:-7]
        newfilenamepostfix = file_name[-4:]
        key = file_name[0:12]
        os.remove(os.path.join(folder_path, file_name))
        for file_name_second in file_names:
            if(file_name_second.startswith(key) and file_name_second!=file_name):        
                newfilename = file_name_second.replace(key,newfilenameprefix)[:-4]
                newfilename = newfilename + newfilenamepostfix
                if newfilename[-6:-4] == "cn":
                    newfilename = newfilename[:-6] + "zh-cn" + newfilenamepostfix
                os.rename(os.path.join(folder_path, file_name_second), os.path.join(folder_path, newfilename))
