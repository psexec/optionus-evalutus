# optionus-evalutus

Simple Python code for pricing options based on the Binomial method. Will likely add more methods later on.

I derived two general formulas for the cases u = 1/d, and p=1/2 to calculate the option value at t=0. These are towards end of file.

## TODO:

* Comment and refactor, stop naming variables like a mathematician.
* Implement a search to see if the payoff function is 0 at any step k - in which case the payoff will be 0 for all subsequent steps k+1,k+2,..,N for puts, and for all 1,..,k-1 for calls. Should speed things up.
* Stop initialising two separate arrays for share values.
* Implement support for diagram output. Planned to do TikZ but will probably do DOT and export as png/svg.
* Remove redundant functions
