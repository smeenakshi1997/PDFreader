import cv2
import pytesseract
from pdf2image import convert_from_path
import re

pages = convert_from_path("GEMC.pdf", 500)
pytesseract.pytesseract.tesseract_cmd = ( r'/usr/bin/tesseract' )

for i in range(len(pages)):
  # save pdf as jpg
  pages[i].save('page'+ str(i) +'.jpg', 'JPEG')

all_text = []
for i in range(len(pages)):
   img = cv2.imread('page'+ str(i) +'.jpg')
   gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
 
   ret, thresh1 = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU | cv2.THRESH_BINARY_INV)

   rect_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1000,1000))

   dilation = cv2.dilate(thresh1, rect_kernel, iterations = 1)

   contours, hierarchy = cv2.findContours(dilation, cv2.RETR_EXTERNAL,
                                                 cv2.CHAIN_APPROX_NONE)

   im2 = img.copy()

   for cnt in contours:
       x, y, w, h = cv2.boundingRect(cnt)
       rect = cv2.rectangle(im2, (x, y), (x + w, y + h), (0, 255, 0), 2)

       cropped = im2[y:y + h, x:x + w]
    
       text = pytesseract.image_to_string(cropped)
       text = "".join(text).strip('\n')
       all_text.append(text)
      
for a in all_text:
    #All the items are displayed as lists. Use normal python string manipulators to break it in chunks to get relevant text.
    bid_re=re.compile(r"Bid/RA/PBP No.:((?:.*\n){1,3})")
    bid = [x.strip() for x in bid_re.findall(a)]
    print(bid)
    company_re=re.compile(r"Company Name:((?:.*\n){1,3})")
    comp_name = [x.strip() for x in company_re.findall(a)]
    print(comp_name)
    contact_re=re.compile(r"Contact No.:((?:.*\n){1,3})")
    contact = [x.strip() for x in contact_re.findall(a)]
    print(contact) #Contact list has two items. 1st one : consignee data, 2nd one : Service provider data
    contract_re=re.compile(r"Contract No:((?:.*\n){1,3})")
    contract = [x.strip() for x in contract_re.findall(a)]
    print(contract)
    generated_re=re.compile(r"Generated Date:((?:.*\n){1,3})")
    gen_date = [x.strip() for x in generated_re.findall(a)]
    print(gen_date)
    start_re=re.compile(r"Start Date((?:.*\n){1,3})")
    start_date = [x.strip() for x in start_re.findall(a)]
    print(start_date)
    end_re=re.compile(r"End Date((?:.*\n){1,3})")
    end_date = [x.strip() for x in end_re.findall(a)]
    print(end_date)
    break      
