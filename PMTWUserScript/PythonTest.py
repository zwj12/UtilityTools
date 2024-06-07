import xml.etree.ElementTree as ET

tree = ET.parse(r'C:\Users\CNMIZHU7\Downloads\Test.XML')
elements = tree.findall("Apartment/Picture/*[@NODE='zenOn(R) embedded object']")
for el in elements:
    if el.find("GestureTapAndHoldFunction") != None and (el.attrib["TYPE"] == "2" or el.attrib["TYPE"] == "10"):
        print(el.tag, el.attrib["TYPE"], el.find("Name").text, el.find("GestureTapAndHoldFunction").text)
        el.find("GestureTapAndHoldFunction").text = ""

tree.write(r'C:\Users\CNMIZHU7\Downloads\Test_New.XML')