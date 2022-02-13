# Classic-Buffer-Overflows<br/>
Python scripts needed to perform a buffer overflow from a previously known vulnerable application or proof of concept. There will also be a small description instructing how to use the files.<br/>
For this particular application I also use WinDbg to build out from the PoC to getting a meterpreter shell. <br/>
The naming covention I am using is as follows<br/>
SX[ShortDescription].py<br/>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;where SX is the step number, followed by a short description.

## S1PoCFuzz.py
Usage: ./S1PoCFuzz.py {IP} {Port} {Data} <br/>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;where data is an interger that represents the number of bytes that cause a crash.<br/>
This is a fuzzer that sends an arbitrary amount of data to a web based application that causes a crash.<br/>
<br/>
In our WinDbg debugger we see that we have overwriten every register except the ESP using the r command. <br/>
We can see what the ESP register points to by using the following command:<br/>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;dds esp
![alt tag](https://github.com/ZeusBanda/Classic-Buffer-Overflows/blob/main/WinDbg-Images/S1Fuzz.png)
