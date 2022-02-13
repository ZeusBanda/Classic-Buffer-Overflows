# Classic-Buffer-Overflows<br/>

Python scripts needed to perform a buffer overflow from a previously known vulnerable application or proof of concept. There will also be a small description instructing how to use the files.<br/>
For this particular application I also use WinDbg to build out from the PoC to getting a meterpreter shell. <br/>
The naming covention I am using is as follows<br/>
SX[ShortDescription].py<br/>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;where SX is the step number, followed by a short description.

## S1PoCFuzz.py
This is a fuzzer that sends an arbitrary amount of data to a web based application that causes a crash.<br/>
Usage: ./S1PoCFuzz.py {IP} {Port} {Data} <br/>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;where data is an interger that represents the number of bytes that cause a crash.<br/>
<br/>
In our WinDbg debugger we see that we have overwriten every register except the ESP using the r command. <br/>
We can see what the ESP register points to by using the following command:<br/>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;dds esp<br/>
![alt tag](https://github.com/ZeusBanda/Classic-Buffer-Overflows/blob/main/WinDbg-Images/S1Fuzz.png)

## S2FindOffset.py
This script along with our debugger will help us find offset that writes to the EIP.<br/>
First we generate an array of characters using the following command:<br/>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;msfvenom-pattern_create l- {data}<br/>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;where data represents the number of bytes that caused the crash.<br/>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Next we make sure to send the character array to the vulnerable application.<br/>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;This is shown on line 16 of this script.<br/>
Usage ./S2FindOffset.py {IP} {Port}<br/>
<br/>
From our debugger, we see that the EIP is overwritten by 33794332
![alt tag](https://github.com/ZeusBanda/Classic-Buffer-Overflows/blob/main/WinDbg-Images/S2EIP.png)
Next we use find the offset that will overwrite the EIP by using the following command<br/>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;msfvenom-pattern_offset -l {data} -q {eip}<br/>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; where -l {data} is the amount of data that caused the application to crash and -q {eip} is the area we want to overwrite.
![alt tag](https://github.com/ZeusBanda/Classic-Buffer-Overflows/blob/main/WinDbg-Images/S2Offset.png)
## S3ChangeEIP.py
Now that we know where our EIP is, we want to verify it and find a suitable location for our reverse shell.<br/>
usage ./S3ChangeEIP.py {IP} {port} {offset}<br/>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Where offset is the interger that obtained from the msfvenom-find_offset command<br/>
<br/>
In our WinDbg debugger we see that we have overwriten ESP with 42424242, or the hex representation of BBBB, using the r command. <br/>
We can see what the ESP register points to with the following command:<br/>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;dds esp -14 L10<br/>
![alt tag](https://github.com/ZeusBanda/Classic-Buffer-Overflows/blob/main/WinDbg-Images/S3EIPOverwrite.png)
This command shows us that our before our ESP is 041dee6c. The lines before our ESP show us that there is some 41s and some 42s.<br/>
These 42s represent our EIP, but more importantly we see that our ESP points to 44s which can be used to house our shellcode.<br/>
By chainging the value of L 10 to something higher we can see more bytes after our ESP. <br/>
This can be important because some application may not have enough memory for our shellcode.<br/>
I will cover a few strategies later to overcome this limitation.
