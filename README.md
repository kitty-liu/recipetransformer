# recipetransformer

Instruction(python 2.7):
1. put project2.py, project2_preprocess.py, ingredients.py and tools.txt in the same folder.
2. run project2.py  (terminal command: python project2.py )
3. Then the program asks for two user-inputs:
   - A recipe link(URL). 
  
     NOTE: if you use an IDE(like pycharm) to run, a white space is required after the URL. Otherwise a
     browser opens and the program still waits for an input. The whole process to enter a URL is typing a URL, pressing space,
     and hitting enter. If you run the program via terminal, the extra whitespace is not required.
   - A type of transformation.
  
     Choose one of the following options: vegetarian, nonvegetarian, vegan, nonvegan, healthy, nonhealthy, altmethod, easy,
     chinese, italian

Required library:
1. NLTK(https://www.nltk.org/install.html): 

  - MAC OS:
    - Install NLTK: run sudo pip install -U nltk
    - Install Numpy (optional): run sudo pip install -U numpy
    - Test installation: run python then type import nltk
  
  
  - Windows: 
    - Install Python 2.7: http://www.python.org/downloads/ (avoid the 64-bit versions)
    - Install Numpy (optional): http://sourceforge.net/projects/numpy/files/NumPy/ (the version that specifies python2.7)
    - Install NLTK: http://pypi.python.org/pypi/nltk
    - Test installation: Start>Python35, then type import nltk
  
  
  
2. Pattern:
   - If you have pip: pip install pattern
   - More ways to install: https://www.clips.uantwerpen.be/pages/pattern
   
   
   
3. Requests:
   - If you have pip: pip install requests[security]
   - More ways to install: http://docs.python-requests.org/en/master/user/install/
   - If you're on OS X and running into 'Connection reset by peer issues', make sure you also have pyOpenSSL installed
  
  
  
4. BeautifulSoup:
   - If you’re using a recent version of Debian or Ubuntu Linux: $ apt-get install python-bs4
   - If you can’t install it with the system packager, you can install it with easy_install or pip:
    
      $ easy_install beautifulsoup4

      $ pip install beautifulsoup4
   - More ways to install & Q&A: https://www.crummy.com/software/BeautifulSoup/bs4/doc/
   

