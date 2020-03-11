import re
import sys
import urllib.request as urlRequest
import urllib.parse as urlParse
import codecs as cs
import os
import shutil


bookName = sys.argv[1].split("/")[-1]
print(bookName)
def MakeAWebpage(pathname, meme=True, default=""):
	print(pathname)
	chapterName = pathname.split("/")[-1]
	file_name = chapterName+'.html'
	headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36"}
	req = urlRequest.Request(pathname, headers = headers)
	x = urlRequest.urlopen(req)
	sourceCode = x.read()
	try:
		os.makedirs("./"+file_name)
	except OSError:
		if not os.path.isdir("./"+file_name):
			raise
	if(meme):
		html = cs.open(file_name+"/"+file_name,'w','utf-8')
		decoded=sourceCode.decode("utf-8") 
		html.write(decoded)
		html.close()
	else:
		html = cs.open(file_name+"/"+file_name+default+".html",'w','utf-8')
		decoded=sourceCode.decode("utf-8") 
		html.write(decoded)
		html.close()

def GatherCompleteSummaryPages():
	pathname='https://www.royalroad.com/fictions/complete?page=1'
	MakeAWebpage(pathname,False,sys.argv[2])
	i=1
	fileN=bookName+"/"+sys.argv[2]+".html"
	myF=open(fileN,encoding="utf-8")
	ListeLiens=[]
	match=""
	for line in myF:
		if line.count("Last &raquo;")!=0:
			match=match+line
	lien = "https://www.royalroad.com" + match.split('\"')[15]
	maxPagination = lien.split("page=")[-1]
	lienProto = lien[0:-3]
	while (i<=int(maxPagination)):
		ListeLiens.append(lienProto+str(i))
		i=i+1
	myF.close()
	return(ListeLiens)
def GatherAllNovelNamesAndLinks(listOfIndexPages):
	bookName = ("https://www.royalroad.com/"+sys.argv[1]).split("/")[-1]
	BookNames,BookLink=[],[]
	for page in listOfIndexPages:
		MakeAWebpage(page,False,sys.argv[2]+page.split("page")[-1])
		myF=open(bookName+'/'+sys.argv[2]+page.split("page")[-1]+'.html',encoding="utf-8")
		listOfRelevantLines=""
		flag=False
		for line in myF:
			motif="<div class=\"fiction-list-item row\">"
			if (line.count(motif)!=0)|flag:
				listOfRelevantLines=listOfRelevantLines+line+"IReallyLovePelicans"
				flag=True
				if (line.count("</div>")!=0):
					flag=False
		listOfRelevantLines="".join(listOfRelevantLines.split("IReallyLovePelicans"))
		myF.close()
		tempFile = open(bookName+"/temp"+page.split("page")[-1]+".html", 'w+', encoding='utf-8')
		tempFile.write(listOfRelevantLines)
		for line in tempFile:
			if (line.count("class=\"font-red-sunglo bold\">")!=0):
				BookName=line.split("class=\"font-red-sunglo bold\">")[1]
				BookName=BookName.split('<')[0]
				BookNames=BookNames.append(BookName)
				BookLink=BookLink.append(line.split('"')[1])
		tempFile.close()
		os.remove(bookName+"/temp"+page.split("page")[-1]+".html")
	return([BookNames,BookLink])
# Download the webpage

bookName = sys.argv[1].split("/")[-1]
MakeAWebpage("https://www.royalroad.com/"+sys.argv[1],False,sys.argv[2])
motif=sys.argv[1]+"/chapter"
fileN=bookName+'/'+sys.argv[1].split("/")[2]+".html"
# Test the page retriever
completeSummaryPages = GatherCompleteSummaryPages()
print(completeSummaryPages)
BookNames,BookLinks=GatherAllNovelNamesAndLinks(completeSummaryPages)
print(BookNames,BookLinks)
#print(completeSummaryPages)
# Get all the links
inputFile = open(fileN,encoding="utf-8")
linkRegex = re.compile("<a href=\".*" + motif + ".*?\"")

ListeLiensClean=[]
for line in inputFile:
    match = re.findall(linkRegex, line)
    if  len(match) == 1:
        # Get rids of the "<a href=" and of the last quote
        # TODO add the start of the link (http://...) after doing the check to compute all the count and split faster
        lien = "https://www.royalroad.com" + match[0][9:-1]
        if (lien.count('/') > 5):
            if (lien.split('/')[6] == "chapter"):
                ListeLiensClean.append(lien)

inputFile.close()

#########################@

i=1
bookName = sys.argv[1].split('/')[2]
html_doc = ""
for lien in ListeLiensClean:
	MakeAWebpage(lien, False, str(i))
	html_doc=html_doc + "<a href=" + "\"" + bookName + str(i) + ".html\">" + bookName + " " + str(i) + "</a><br/>" + "\r\n"
	i = i + 1
html_doc2=""
html_doc = html_doc + html_doc2
tocHTML = cs.open(bookName+"/toc.html", 'w', 'utf-8')
tocHTML.write(html_doc)
tocHTML.close()
###

html_doc = ""
html_doc2=""
motif="div class=\"chapter-inner chapter-content\""
motif2='div>'
i=i-1
while i>0:
	html_doc = ""
	token=False
	meme=cs.open(bookName+"/"+"Chapter"+str(i)+".html",'r+','utf-8')
	lines=meme.readlines()
	meme.close()
	for line in lines:
		if token:
			if line.count(motif2)!=0:
				break
		if token:
			html_doc=html_doc+line+"\r\n"
		if line.count(motif)!=0:
			token=True
	html_doc=html_doc+html_doc2
	meme2=cs.open(bookName+"/"+"Chapter"+str(i)+".html",'w','utf-8')
	meme2.write(html_doc)
	meme2.close()
	i=i-1
#meme=open("My_soup.html","w")
#meme.write(soup.prettify())
#meme.close()