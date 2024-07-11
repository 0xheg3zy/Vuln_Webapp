# Vuln_Webapp
    This is a simple vuln web appliaction created with flask 

# Demo For The Vulns , it's reason and the mitigation for it
    Idor:
    ![alt text](https://github.com/0xheg3zy/Vuln_Webapp/blob/main/vuln_reason/dom_xss.png?raw=true)
       The vuln is lead to sensitive data leak and some times lead to ato
       Reason for vulernability is
            The developer doesn't check if the returned data is belongs to that user or not
        The mitigation is:
            id = session['id']
            the user now can see it's data only as the id now is come from the session and he can't edit it
    
    Xss:
    ![plot](vuln_reason/dom_xss.png)
        Reason for vulernability is 
            The developer put the user input into the page (reflected or dom) or store it in database directly without validation (stored)
            Simple mitigation for that is :
                1)using innerText instead of innerHTML#
                2)DOMPurify lib include it in your front code to encode special chars with html encoding
                in php you can use :
                    htmlentities() to encode chars with html encoding
                    filter_var() function

    Sqli:
    ![plot](vuln_reason/sqli.png)
        It leads to database takeover and some times lead to rce using dumpfile function (MYSQL)
        Reason for vulnerability is :
            the developer put the user input into the query directly without validation
        Simple mitigation for that is:
            1)using parameterarized query
            2)using orm such as flask_sqlalchemy
            In php you can use:
                parameterarized query
                mysqli_real_escape_string(), htmlspecialchars() ,filter_var() functions

    SSTI:
    ![plot](vuln_reason/ssti.png)
    It leads to rce , information disclosure (configuration info , env variables)
    Reason for vulernability is instead of the developer read template from ssti.html , it create a variable and put the user input into the template string which can be malicious
    Simple mitigation for that is : 
        1)use render_template (this function is escape special chars automatically) instead of render_template_string
        2)always input vaildation is the mitigation for any vuln or bug


    SSRF:
    ![plot](vuln_reason/ssrf.png)
    It leads to internal port scan , rce (ssh keys reading) with file:// protocol , information disclosure (configuration info , env variables)
    Reason for vulernability is the url is user input and no validation , so the user can do port scanning , reading files (file:///etc/passwd) , rce using gopher protocol
    Simple mitigation for that is :
        1)check on the url the user enter [white list]
        2)disable some URL schemas such as file:///, dict://, ftp://, and gopher://


    Local file inclusion:
    ![plot](vuln_reason/lfi(arbitary_file_read).png)
    It leads to reading any file on system , rce via excuting php code (log poisoning)(php filter chains)
    Reason for vulernability is the page name is controlled by user and no validation on , so he can read any file or do more
     Simple mitigation for that is :
        1)check on the page name [white list] (pages you have on website)
        2)path traversal validation 
        In php:
            1)avoid using include , include_once , require , require_once with value can be controlled by user


    Logic bugs:
    ![plot](vuln_reason/logic_bug.png)
    It leads to a lot of things depend on functionality of application , can lead to get a lot of goods with price of one , etc
    Reason for vunlerability (in our example) is the the price is controlled by user , quantity can be a negative number 
    Simple mitigation for that is :
        1)price should be gotten from database and can't be changed
        2)quantity should be a int and bigger than zero


    weak secret_key session:
    ![plot](vuln_reason/weak_session_secret.png)
    It leads to priesc , ato and more
    Reason for vunlerability the secret key used in session signing is weak and can be cracked 
    Simple mitigation for that is :
        1)make it a random value and store it as a environment variable 
        1.1)os.urandom(32) for generating key , os.environ("SECRET") to get the value stored in the environment variable
