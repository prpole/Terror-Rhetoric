#The Rhetoric of the War on Terror

This project examines the rhetoric surrounding the "War on Terror" and traces the extent to which that rhetoric has been adopted in non-governmental discourse. By mining the transcripts of speeches by George W. Bush and Barack Obama and social media during their administrations, we will identify keywords that define each realm of communication. We will mark the relative frequency of terms like "terrorism," "military," and "protection," the terms that are covariant with them, and their context within the larger discourse. 

This analysis will happen in two parts. In the first part, Phillip will demonstrate how the administration material was selected and obtained using Python-driven web scraping techniques, then perform quantitative analysis on the selected corpus using TAPoR, Voyant Tools and NVivo to characterize the rhetoric of the Bush administration versus the Obama administration. In the second part, May will trace the way the "War on Terror" was discussed in social media during the same period, considering the terms used and the broader trends in the discourse. Our expectation is that these examinations will reveal a parallelism between the terms established by the American government and the discussion in the public sphere.

##The Bush and Obama Administrations

###1. Gathering the Data

The first step in analyzing the speeches of the Bush and Obama administrations was to select the data and obtain plaintext versions of the speeches. In order to limit the dataset to major speeches by the two Presidents, the site *presidentialrhetoric.com* was used as a datasource. This limitation was voluntarily assumed for two reasons. The first is that by limiting the dataset to *major* speeches (as *presidentialrhetoric.com* does) we ensure that we are working with the clearest articulation of rhetorical policy, thereby addressing the intent of certain usages and word pairings more directly. We determined that press releases and announcements from, for example, Jay Carney, the standing Whitehouse Press Secretary, would have a lesser degree of rhetorical intentionality because of their comparative spontaneity. As such, examining these statements for their rhetorical content would be less ingenuous and potentially more opportunistic. The second reason for limiting our selection to the content represented on *presidentialrhetoric.com* was the comparative ease of scraping the plaintext versions. While scraping the contents of this site presented its challenges, the content was clearly organized and friendly to scraping. In contrast, the press section of *whitehouse.gov* made scraping difficult because of its paging mechanism, which spoiled all of our spiders (formulated using Scrapy). In a less modest iteration of this project, other methods of scraping would be investigated more extensively. For these reasons, we obtained the HTML versions of the relevant pages from *presidentialrhetoric.com* and continued with our cleaning.

The next step was to extract the plaintext of the speeches from the collected HTML data. In this step, we used Python and the Beautiful Soup module to parse the raw HTML. We began by identifying the location of the relevant data in the HTML structure, and found that by checking for HTML tags with certain attributes we could isolate the text we wanted. The following is a representative example from the raw HTML:

`````
<p align="left" class="style2">Mrs. Ford, the Ford family; distinguished guests, including our Presidents and First Ladies; and our fellow citizens:</p>

<p align="left" class="style2">We are here today to say goodbye to a great man. Gerald Ford was born and reared in the American heartland. He belonged to a generation that measured men by their honesty and their courage. He grew to manhood under the roof of a loving mother and father -- and when times were tough, he took part-time jobs to help them out. In President Ford, the world saw the best of America -- and America found a man whose character and leadership would bring calm and healing to one of the most divisive moments in our nation's history.</p>
`````

By specifying the "align" and "class" attributes, we are able to extract this text using Beautiful Soup. Not all pages were identical, however, so we cycled through the several different formats used by *presidentialrhetoric.com* using an *if* statements to check if the text field was still unpopulated (which would indicate that the relevant field had not been identified, and thus a different set of attributes would be required). Using this structure, we arrived at the following code, which is compilable as "convertall.py" in the attached directory:

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

Here pulltext() is the main function, while wordlist() is a secondary function meant as the first step in compiling a concordance---by splitting the speech into an iterable of the words it contains, it would be possible to check instances of identical list items and construct a list of word occurrences in the collected speeches. Other existing tools (discussed below) made this concordance unnecessary, but the code was preserved for possible use in cleaning (splitting a speech into words in an iterable and recombining it is an easy way to get rid of white space). 

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

This was the final stage of preparation for the text of the speeches, and analysis was able to begin.

###2. Analyzing the Data

Our analysis was framed as a comparison between the Bush and Obama administrations. The purpose of this choice was to see to what extent change in administration corresponded to change in rhetorical strategy. From here, the examination occurred in three phases. First, we compared word frequencies in the use of "terror" and its stem words. Next, we compared the words that are covariant with "terror" and its stem words in each administration.

####2.1 Frequency

Using NVivo, we traced the frequency of "terror" and its stem words (i.e. "terrorism," "terrorist," "terrorists," etc.). This took the form of a simple word frequency count. The results were both startling in their degree and consistent with our expectations in their nature. 

![Fig. 1 - Bush Graph] (http://pp2454.github.io/BushTerrorGraph.jpg?raw=true)

Though the average use of "terror" and its stem words peaks early, usage is consistent and frequent throughout the Bush administration. Spikes continue to more than quadruple the average occurrence per speech throughout the administration's term. Obama's use of the term is much less pronounced:

![Fig. 2 - Obama Graph] (http://pp2454.github.io/ObamaTerrorGraph.jpg?raw=true)

Unlike the frequent and consistent use of "terror" in the Bush administration, the Obama administration uses the term infrequently and inconsistently. With one major exception (May 23, 2013, a speech given to the National Defense University), spikes are low, rarely exceeding a count of three. 

The following table summarizes the numeric difference between the two administrations' rhetoric:

![Fig. 3 - Table] (http://pp2454.github.io/TerrorTable.jpg?raw=true)

The Bush administration mentions "terror" or one of its stem words more than twice as often as the Obama administration does. The average occurrences per speech for the Bush administration is nearly five times that of the Obama administration. Based on frequency, it would appear that the Obama administration has indeed made a substantive change in rhetorical strategy with regard to "terror."


####2.2 Covariants

In order to track words that frequently occur as part of the rhetoric of the "War on Terror," we used NVivo's Cluster Analysis tools to consider words that tended to occur together in relation to each other. Here are the words that cluster with the Bush administrations' use of "terrorrists" and its stem words ("terrorist," "terrorist's," and "terrorists'"):

![Fig. 4 - Bush Terrorists Cluster] (http://pp2454.github.io/BushTerroristsCluster.jpg?raw=true)

The most striking feature of this graph is the extent to which mentions of terrorists as people often come clustered with words of construction and care. "Terrorists" is in a sub-cluster with "world," "hoping," "longing," and "caring." This would seem to imply a frequent invocation of terrorism in close proximity to the things that are claimed to be under threat. A clearly analogous feature can be seen in the top of the figure: "enemy" and "freedom" are directly correlated, implying a codependence of the threat and the thing threatened. Invocation of impending loss is a major strategy in the Bush administration's discussion of terrorists as people. A somewhat different strategy accompanies mentions of "terror" in the abstract:

![Fig. 5 - Bush Terror Cluster] (http://pp2454.github.io/BushTerrorCluster.jpg?raw=true)

Here the association of the threat with the thing threatened gives way to a more general reference to ideological constructs. "Terror" and "believe" are closely related, perhaps as a way of undercutting the possible validity of the actions of those dubbed terrorists. 

Unfortunately, Obama's use of "terror" is too infrequent to appear on his cluster tree. Instead, we traced the terms of the militarism that have marked his administration---the terms of the wars inherited from Bush's "War on Terror." The first term is "protects":

![Fig. 6 - Obama Protects Cluster] (http://pp2454.github.io/ObamaProtectsCluster.jpg?raw=true)

The results are again startlingly different. "Protects" and its stems ("protect," "protection," etc.) are associated with heavy abstraction, and with a very small number of terms---only "systems" and "times." Both gesture toward a sense of community that transcends national borders, feeding into the administration's optimistic rhetoric involving globalization and the international community. The American-exceptionalist logic of the Bush administration was largely submerged in the rhetorical shift that came with the new guard, and this shift would appear to affect the way that terms of safety are invoked.

The next term is "Military":

![Fig. 7 - Obama Military Cluster] (http://pp2454.github.io/ObamaMilitaryCluster.jpg?raw=true)

The term "military" itself is already a notable change from the Bush administration. Rather than focusing on the perceived enemy or the perceived threat, the Obama administration appeals to the state of the Americans serving in the military. This appears to be a shift that corresponds with the changing public opinion of the war---Obama was, to a great extent, elected on promises of changing the militarism of the preceding administration, and his rhetoric mirrors that. The association of "peace" and "security," however, reveals the extent to which a change in rhetoric is separated from a change in policy. "Peace" would imply a cessation of hostilities, but "security" is the term used to justify maintaining a military presence in Iraq and Afghanistan. It is still a military word, but one that emphasizes the safety that would appear to result from hostility. "Needs" would appear to fit in with this framework, deferring to a sense of the necessity of maintaining a military presence for the sake of "peace" and "security." "Words" is a peculiar outlier; at this point, explanation for this peculiar binary would require more in-depth study.

Both the Obama and Bush administrations use militaristic rhetoric in close proximity with the things they use to justify military action. For Bush, this expresses itself as an association of terrorism with the thing that terrorism is said to threaten. This strategy works both with reference to specific threats, but also abstractly in a more ideological sense. For Obama, the usage is somewhat different. In the first place, "terrorism" itself has dropped entirely out of the equation. Additionally, the terms are almost all conceptual. Individual terrorists give way to entire militaries; the lone agent gives way to the entire global community. This split would seem to reflect the more basic ideological divisions of the two premiers. The Bush administration was more isolationist in terms of cooperation and more invasive in military matters; the Obama administration is feeding off the widespread dissatisfaction with those policies, and as such focuses on global community and the alleged bare minimum of involvement. The extent to which this affects the underlying associations of words is remarkable.

###3. Conclusions

In general, our expectations were confirmed. The Obama administration largely abandoned the rhetorical figure of the terrorist, but only to replace it with a larger military force. The specific threats and fear-mongering of the Bush administration have become the elusive optimism and appeal to the global community of Obama's speeches. Underlying the current premier, though, is a reluctance to abandon military action, which is also evident in his rhetorical strategies. The dubious claims that the current foreign wars are protecting American citizens remains in full force. The difference is that it is wrapped in a veneer of hope and the hanging promise of change.

This is an extremely modest iteration of what we hope will be a larger project. In an expanded version of this first part, a larger corpus would be necessary as well as more sophisticated tagging of speeches according to topic. It would also be useful to dig deeper into semantic analysis, considering the words that precede and follow iterations of these words. More keywords could also be identified and examined. We hope, though, that this has provided a beginning.

In the next section, May will continue this discussion in the context of social media and the public sphere.
