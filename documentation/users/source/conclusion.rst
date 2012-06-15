Conclusion
==========

What this was intended to tell you
----------------------------------

This was intended to be a slightly more comprehensive set of help than what the online-help commands will give you. Hopefully it will provide some idea of the motivations as well as the usage so that the running of the program doesn't seem so obscure.

What you should do next
-----------------------

The most obvious thing is to run a test and see what happens. I would also recommend looking at the data and then poking around in the logcat files to see if there's anything that jumps out at you as being anomalous. I particularly recommend finding the test with the lowest ttr time, the test with the longest ttr time, and any failed recoveries (if there are any) that will be indicated in the `*_data.csv` file by the word `None`.

This is the first draft of this document. If there's anything in particular that seems obscure or under-explained, feel free to file an issue on the `bitbucket repository <https://bitbucket.org/allion_software_developers/timetorecovery/issues?status=new&status=open>`_.
