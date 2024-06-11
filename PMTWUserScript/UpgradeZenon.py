import xml.etree.ElementTree as ET

# <GestureTapAndHoldFunction>&lt;No function linked&gt;</GestureTapAndHoldFunction> <GestureTapAndHoldFunction/>
# <GestureTapFunction>&lt;No function linked&gt;</GestureTapFunction> <GestureTapFunction/>
# <GestureDoubleTapFunction>&lt;No function linked&gt;</GestureDoubleTapFunction> <GestureDoubleTapFunction/>
# <Function>&lt;No function linked&gt;</Function> <Function></Function>

# tree = ET.parse(r'C:\Users\CNMIZHU7\Downloads\Test1.XML')
# elements = tree.findall("Apartment/Picture/*[@NODE='zenOn(R) embedded object']")
# for el in elements:
#     if el.find("GestureTapAndHoldFunction") != None:
#         print(el.tag, el.attrib["TYPE"], el.find("Name").text, el.find("GestureTapAndHoldFunction").text)
#         # 2 - Dynamic text; 10 - Button; 11 - Switch; 24 - Combobox; 28 - Diagram; 14 - Clock; 25 - Listcontrol
#         if el.attrib["TYPE"] == "2" or el.attrib["TYPE"] == "10" or el.attrib["TYPE"] == "11" or el.attrib["TYPE"] == "28" or el.attrib["TYPE"] == "14" or el.attrib["TYPE"] == "25":
#             el.find("GestureTapAndHoldFunction").text = ""

#     if el.find("GestureDoubleTapFunction") != None:
#         print(el.tag, el.attrib["TYPE"], el.find("Name").text, el.find("GestureDoubleTapFunction").text)
#         # 2 - Dynamic text; 10 - Button; 11 - Switch; 24 - Combobox; 28 - Diagram; 14 - Clock; 25 - Listcontrol
#         if el.attrib["TYPE"] == "2" or el.attrib["TYPE"] == "10" or el.attrib["TYPE"] == "11" or el.attrib["TYPE"] == "28" or el.attrib["TYPE"] == "14" or el.attrib["TYPE"] == "25":
#             el.find("GestureDoubleTapFunction").text = ""

# tree.write(r'C:\Users\CNMIZHU7\Downloads\Test1_New.XML')


with open(r'C:\Users\CNMIZHU7\Downloads\Test.XML', 'r+', encoding='utf16') as file:
    content = file.read()
    new_content = content.replace('&lt;No function linked&gt;', '')
 
with open(r'C:\Users\CNMIZHU7\Downloads\Test_New.XML', 'w', encoding='utf16') as file:
    file.write(new_content)