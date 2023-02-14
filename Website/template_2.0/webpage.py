from flask import Flask, render_template

# Create a flask object
app= Flask(__name__)

# define the action for the top level route
@app.route('/')
def index():
	return '''
<html>
<head>
  <title>SNP Portal </title>
  <link href="homestyles.css" rel="stylesheet">
</head>

<!--Navigation bar for the website with anchor tags to relavant pages -->
<body>
  <header>
    <div class='nav'>
      <div class='container'>
        <img src='./logo.jpeg'>   
        <a style=float:right; href="./resources_page.html">Resources</a>
        <a style=float:right; href="./search_page.html">Search</a>
        <a style=float:right; href="./about_page.html">About</a>
        <a style=float:right; href="/Users/lynnettebhebhe/Desktop/SNP website/homepage.html">Home</a>
      </div>  
    </div>
  </header>

 <!--This division contains the header, sub-header, a form which the user will complete in the searchbar and some examples of the query information--> 
  <div class="main">
    <div class="img">
      <h1>  Type 1 Diabetes SNP Portal</h1>

    <div id="search">
      <form> 
        <br>
        <h2>Find your SNP</h2>
        <br>
        <label for="search"></label>
        <input type="text" name="SNP" id=seacrh required class="searchbar" placeholder="Search..."> 
        <button type="submit">Search</button>
        <p> Examples: 
          <a id='example' href="#search">rs72928038,</a>
          <a id='example' href="#search">HLA-DQB1,</a>
          <a id='example' href="#search">6:90267049</a></p>
      </form>
    </div>
  </div>
  <br>

  <!-- This section contains anchor tags that are links to specified pages within the website and external sources as well -->
    
  <div class='options'> 
    <a href="./about_page.html">About</a>
    <!--For advanced search we could use bolean terms--> 
    <a href="./search_page.html"> Advanced Search</a> 
    <a href="./download.html">Download</a>
    <a href="./resources_page.html">Resources</a>
  </div>  

 <!--Footer section of the website that appears on all the webpages-->
  <footer>
    <div class="footer">
      <p class="copyright">© Type 1 Diabetes SNP Portal 2023</p>
    </div>
  </footer>
      
 </body>
</html>'''

# define a route called 'protein' which accepts a protein name parameter
#@app.route('/protein/<protein_name>')
#def protein(protein_name):


# start the web server
if __name__ == '__main__':
	app.run(debug=True)