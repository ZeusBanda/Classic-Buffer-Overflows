# Classic-Buffer-Overflows<br/>
Python scripts needed to perform a buffer overflow from a previously known vulnerable application or proof of concept. There will also be a small description instructing how to use the files.<br/>
For this particular application I also use WinDbg to build out from the PoC to getting a meterpreter shell. <br/>
The naming covention I am using is as follows<br/>
SX[ShortDescription].py<br/>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;where SX is the step number, followed by a short description.

## S1PoCFuzz.py
Usage: ./S1PoCFuzz.py {IP} {Port} {Data} <br/>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;where data is an interger that represents the number of bytes that cause a crash.
