# OFFFileFixer
Code solution to the COSC363 Challenge Problem 1
<h1>Challenge Problem 1 Solution</h1>
<p>This is a code solution to the first challenge problem: Identify errors in OFF files caused by vertices of faces not being defined in counter clockwise order.</p>
<p>Note that off files must be in the format given in Sphere2.off as the program must read the file.</p>
<h2>How it works</h2>
<p>For each defined face it calculates the wind of its vertices. This indicates whether they have been declared in counter clockwise order. Using this we can create a list of incorrectly defined line indices. We can then fix these by going through all the permutations and testing the wind until one that results in a CC order occurs. Then the file is rewritten to correct this mistake.</p>
