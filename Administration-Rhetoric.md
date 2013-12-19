#War Rhetoric in Non-Governmental Discourse

This project examines the rhetoric surrounding the "War on Terror" and traces the extent to which that rhetoric has been adopted in non-governmental discourse. By mining the texts produced by the premiers of United States and the United Kingdoms (from the Bush and Blair administrations to the present), we will identify keywords that define each realm of communication, focusing on terms “terrorism,” "security," "protection" and their stem words, which have defined the many American wars of the century so far. We will mark the relative frequency of these terms, the terms that are covariant with them, and their context within the larger discourse. This rhetorical analysis will happen in two parallel parts. In the first part, Phillip R. Polefrone will show how the textual material was selected and obtained using Python-driven web scraping techniques, then perform quantitative analysis on the selected corpus using TAPoR, Voyant Tools and NVivo to characterize the rhetoric of the Bush administration versus the Obama administration. In the second part, May Hany El Maraashly will trace the way the "War on Terror" was discussed in social media during the same period, considering the terms used and the broader trends in the discourse. Our expectation is that these examinations will show a parallelism between the terms established by the American government and the discussion in the public sphere.

##Phillip's Part

###1. Gathering the Data

The first step in analyzing the speeches of the Bush and Obama administrations was to select the data and obtain plaintext versions of the speeches. In order to limit the dataset to major speeches by the sitting premier, the site *presidentialrhetoric.com* was used as a datasource. This limitation was voluntarily assumed for two reasons. The first is that by limiting the dataset to *major* speeches as *presidentialrhetoric.com* does, we ensure that we are working with the clearest articulation of rhetorical policy, thereby addressing the intent of certain usages and word pairings more directly. We determined that press releases and announcements from, for example, Jay Carney, the standing Whitehouse Press Secretary, would have a lesser degree of rhetorical intentionality because of their comparative spontaneity. As such, examining these statements for their rhetorical content would be less ingenuous and potentially more opportunistic. The second reason for limiting our selection to the content represented on *presidentialrhetoric.com* was the ease of scraping the plaintext versions. While scraping the contents of this site presented its challenges, the content was clearly organized and friendly to scraping. In contrast, the press section of *whitehouse.gov* made scraping difficult because of its paging mechanism, which spoiled all of our spiders (formulated using Scrapy). In a less modest iteration of this project, other methods of scraping would be investigated. For these reasons we obtained the HTML versions of the relevant pages from *presidentialrhetoric.com* and continued with our cleaning.

The next step was to extract the plaintext of the speeches from the collected HTML data. In this step, we used Python and the Beautiful Soup module to parse the raw HTML. We began by identifying the location of the relevant data in the HTML structure, and found that by checking for HTML tags with certain attributes we could isolate the text we wanted. The following is a representative example from the raw HTML:

`````
<p align="left" class="style2">Mrs. Ford, the Ford family; distinguished guests, including our Presidents and First Ladies; and our fellow citizens:</p>

<p align="left" class="style2">We are here today to say goodbye to a great man. Gerald Ford was born and reared in the American heartland. He belonged to a generation that measured men by their honesty and their courage. He grew to manhood under the roof of a loving mother and father -- and when times were tough, he took part-time jobs to help them out. In President Ford, the world saw the best of America -- and America found a man whose character and leadership would bring calm and healing to one of the most divisive moments in our nation's history.</p>
`````

By specifying the "align" and "class" attributes, we are able to extract this text using Beautiful Soup. Not all pages were identical, however, so we cycled through the several different formats used by *presidentialrhetoric.com* using an *if* statements to check if the text field was not yet populated (meaning that the relevant field had not been identified, and thus a different set of attributes would have to be specified). Using this structure, we arrived at the following code, which is compilable as "convertall.py" in the attached directory:

<pre><code>
#!/usr/bin/env python

from bs4 import BeautifulSoup
from types import *
import os

def checkfile(filename):
    content = open("TextOnly/"+filename,"r+")
    print content.read()

def pulltext(filename):    
    text = []
    soup = BeautifulSoup(open("www.presidentialrhetoric.com/speeches/"+filename,"r"))
    textversion = open("TextOnly/"+filename+".txt","w")
    for p in soup.find_all('p'):
        if p.attrs == {'align': 'left', 'class': ['style2']}:
            string = p.string
            if type(string) is not NoneType:
                try:
                    string.encode('ascii')
                    text.append(string)
                except UnicodeEncodeError:
                    pass
            else:
                pass
    for p in soup.find_all('span'):
        if p.attrs == {'class': ['style2']}:
            string = p.string
            if type(string) is not NoneType:
                try:
                    string.encode('ascii')
                    text.append(string)
                except UnicodeEncodeError:
                    pass
    if text == []:
        for p in soup.find_all('p'):
            string = p.string
            if type(string)is not NoneType:
                try:
                    string.encode('ascii')
                    text.append(string)
                except UnicodeEncodeError:
                    pass
    """for l in text:
        if type(l) is NoneType:
            del text[text.index(l)]
            return text"""
    textversion.write(''.join(text))
    textversion.close()

def wordlist(fname):
    file = open('TextOnly/'+str(fname),"r+")
    if fname != '.DS_Store':
        fcontent = open('TextOnly/'+str(fname),"r+")
        text = fcontent.read()
        fstr = text.split()
        for l in fstr:
            if str(l) == '(laughter.)' or str(l) == '(laughter)' or str(l) == '(Laughter.)' or str(l) == '(Laughter)' or str(l) == '(applause.)' or str(l) == '(applause)' or str(l) == '(Applause.)' or str(l) == '(Applause)':
                fstr.remove(l)
    return fstr

for fname in os.listdir('www.presidentialrhetoric.com/speeches'):
    if fname == ".DS_Store":
        pass
    else:
        try:
            pulltext(fname)
        except Exception:
            print 'error' + fname
</code></pre>

Here pulltext() is the main function, while wordlist() is a secondary function meant as the beginning of a concordance---by splitting the speech into an iterable of the words it contains, it would be possible to check instances of identical list items and construct a concordance of the collected speeches. Other existing tools (discussed below) made this concordance unnecessary, but the code was preserved for possible use in cleaning (splitting a speech into words in an iterable and recombining it is an easy way to get rid of white space). 

This code, when run from the root project directory, creates a folder with the plaintext versions. These files were named by date when downloaded from *presidentialrhetoric.com*, but for preparation for use in Voyant Tools the format needed to be revised from MMDDYY to YYMMDD (so that they would appear in chronological order). The following code was written to that effect, which can be run as fnamedater.py from the root project directory:

<pre><code>
from bs4 import BeautifulSoup
from types import *
import os

def checkfile(filename):
    content = open("TextOnly/"+filename,"r+")
    print content.read()
    
for fname in os.listdir('TextOnly'):
    if fname != ".DS_Store":
        file = open('TextOnly/'+fname, 'r')
        text = file.read()
        date = []
        year = fname[6:8]
        month = fname[0:2]
        day = fname[3:5]
        date.append(year)
        date.append(month)
        date.append(day)
        newfname = ''.join(date)
        newfile = open('TextOnlyDated/'+newfname+'.txt','w')
        newfile.write(text)
        newfile.close()
        file.close()
</code></pre>

This creates a new set of files in a new directory ("TextOnlyDated"), which can be compressed into a single file and uploaded to Voyant Tools or NVivo. 

This was the final stage of preparation for the text of the speeches before analysis was able to begin.

###2. Analyzing the Data

Our analysis was framed as a comparison between the Bush and Obama administrations. The purpose of this choice is to see to what extent change in administration corresponds to change in rhetorical strategies. From here, the examination occurred in three phases. First, we compared word frequencies in the use of "terror" and its stem words. Next, we compared the words that are covariant with "terror" and its stem words in each administration. Finally, we compared the contextual environment of these occurrences (prepositions, full stops, and so forth).

####2.1 Frequency

Using NVivo, we traced the frequency of "terror" and its stem words (i.e. "terrorism," "terrorist," "terrorists," etc.). This was a simple word frequency count. The results were both startling in their degree and consistent with our expectations in their nature. 

![Fig. 1 - Bush Graph] (http://pp2454.github.io/BushTerrorGraph.jpg?raw=true)

Though the average use of "terror" and its stem words peaks early, usage is consistent and frequent throughout the Bush administration. Spikes continue to more than quadruple the average occurrence per speech throughout the administration's term. Obama's use of the term is much less pronounced:

[Fig. 2: Obama Graph] (http://pp2454.github.io/ObamaTerrorGraph.jpg?raw=true)

Unlike the frequent and consistent use of "terror" in the Bush administration, the Obama administration uses the term infrequently and inconsistently. With one major exception (May 23, 2013, a speech given to the National Defense University), spikes are low, rarely exceeding a count of three. 

The following table summarizes the numeric difference between the two administrations' rhetoric:

[Fig. 3: Table] (http://pp2454.github.io/TerrorTable.jpg?raw=true)



####2.2 Covariants

####2.3 Context

###3. Conclusions


 