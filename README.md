# Vuln_Webapp
    This is a simple vuln web appliaction created with flask 
# Installation:
    git clone https://github.com/0xheg3zy/Vuln_Webapp
    cd Vuln_Webapp
    pip3 install -r requirements.txt
    python app.py
# Running Via docker:
    cd Vuln_Webapp
    docker build -t vuln_app_image .
    docker run -d -p 80:80 --name vuln_app_container vuln_app_image
# Demo For The Vulns , it's reason and the mitigation for it
#    Idor:
#    ![alt text](https://github.com/0xheg3zy/Vuln_Webapp/blob/main/vuln_reason/idor.png)
       payload used : /idor/user/5
       The vuln is lead to sensitive data leak and some times lead to ato
       Reason for vulernability is
            The developer doesn't check if the returned data is belongs to that user or not
        The mitigation is:
            id = session['id']
            the user now can see it's data only as the id now is come from the session and he can't edit it
    
#    Xss:
#    ![alt text](https://github.com/0xheg3zy/Vuln_Webapp/blob/main/vuln_reason/dom_xss.png)
        payload used : <img src=x onerror=alert(1)>
        Reason for vulernability is 
            The developer put the user input into the page (reflected or dom) or store it in database directly without validation (stored)
            Simple mitigation for that is :
                1)using innerText instead of innerHTML#
                2)DOMPurify lib include it in your front code to encode special chars with html encoding
                in php you can use :
                    htmlentities() to encode chars with html encoding
                    filter_var() function

#    Sqli:
#    ![alt text](https://github.com/0xheg3zy/Vuln_Webapp/blob/main/vuln_reason/sqli.png)
        payload used : ' or 1=1 limit 4,1--
        It leads to database takeover and some times lead to rce using dumpfile function (MYSQL)
        Reason for vulnerability is :
            the developer put the user input into the query directly without validation
        Simple mitigation for that is:
            1)using parameterarized query
            2)using orm such as flask_sqlalchemy
            In php you can use:
                parameterarized query
                mysqli_real_escape_string(), htmlspecialchars() ,filter_var() functions

#   SSTI:
#   ![alt text](https://github.com/0xheg3zy/Vuln_Webapp/blob/main/vuln_reason/ssti.png)
    payload used : {{4*'5'}}
    It leads to rce , information disclosure (configuration info , env variables)
    Reason for vulernability is instead of the developer read template from ssti.html , it create a variable and put the user input into the template string which can be malicious
    Simple mitigation for that is : 
        1)use render_template (this function is escape special chars automatically) instead of render_template_string
        2)always input vaildation is the mitigation for any vuln or bug


#    SSRF:
#    ![alt text](https://github.com/0xheg3zy/Vuln_Webapp/blob/main/vuln_reason/ssrf.png)
    payload used : file:///etc/passwd
    It leads to internal port scan , rce (ssh keys reading) with file:// protocol , information disclosure (configuration info , env variables)
    Reason for vulernability is the url is user input and no validation , so the user can do port scanning , reading files (file:///etc/passwd) , rce using gopher protocol
    Simple mitigation for that is :
        1)check on the url the user enter [white list]
        2)disable some URL schemas such as file:///, dict://, ftp://, and gopher://


#    Local file inclusion:
#    ![alt text](https://github.com/0xheg3zy/Vuln_Webapp/blob/main/vuln_reason/lfi(arbitary_file_read).png)
    payload used : /lfi/index?page=../../../../../../../../../etc/passwd
    It leads to reading any file on system , rce via excuting php code (log poisoning)(php filter chains)
    Reason for vulernability is the page name is controlled by user and no validation on , so he can read any file or do more
     Simple mitigation for that is :
        1)check on the page name [white list] (pages you have on website)
        2)path traversal validation 
        In php:
            1)avoid using include , include_once , require , require_once and similar functions with value can be controlled by user


#    Logic bugs:
#    ![alt text](https://github.com/0xheg3zy/Vuln_Webapp/blob/main/vuln_reason/logic_bug.png)
    payload used : curl 'http://localhost/logic/purchase' -X POST --data-raw 'quantity=10&price=0.1'
    It leads to a lot of things depend on functionality of application , can lead to get a lot of goods with price of one , etc
    Reason for vunlerability (in our example) is the the price is controlled by user , quantity can be a negative number 
    Simple mitigation for that is :
        1)price should be gotten from database and can't be changed
        2)quantity should be a int and bigger than zero


#    weak secret_key session:
#    ![alt text](https://github.com/0xheg3zy/Vuln_Webapp/blob/main/vuln_reason/weak_session_secret.png)
    payload used : flask-unsign --unsign --cookie 'put_cookie_here' --wordlist /usr/share/wordlists/rockyou.txt --no-literal-eval
    It leads to priesc , ato and more
    Reason for vunlerability the secret key used in session signing is weak and can be cracked 
    Simple mitigation for that is :
        1)make it a random value and store it as a environment variable 
        1.1)os.urandom(32) for generating key , os.environ("SECRET") to get the value stored in the environment variable
